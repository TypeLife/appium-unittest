import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import AgreementDetailPage
from pages import ChatFilePage
from pages import ChatLocationPage
from pages import ChatMorePage
from pages import ChatSelectFilePage
from pages import ChatSelectLocalFilePage
from pages import CreateGroupNamePage
from pages import FindChatRecordPage
from pages import GroupChatPage
from pages import GuidePage
from pages import MeCollectionPage
from pages import MePage
from pages import MessagePage
from pages import OneKeyLoginPage
from pages import PermissionListPage
from pages import SelectContactsPage
from pages import SelectLocalContactsPage
from pages import SelectOneGroupPage
from pages import GroupChatSetPage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(object):
    """前置条件"""

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.select_one_group_by_name(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群返回，无群创建
        if group_name in group_names:
            return
        sog.click_back()
        time.sleep(2)
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        current_mobile().hide_keyboard_if_display()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.click_submit_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        # one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        if one_key.have_read_agreement_detail():
            one_key.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def public_send_file(file_type):
        """选择指定类型文件发送"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = GroupChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csf.click_local_file()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(file_type)
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()


class MsgGroupChatFileLocationTest(TestCase):
    """
    模块：消息-群聊文件,位置

    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：消息-群聊文件,位置
    """

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_group_chat_page()
            return
        scp = GroupChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            # current_mobile().reset_app()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    @staticmethod
    def setUp_test_msg_group_chat_file_location_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0001(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
        2、点击本地文件
        3、不选择文件，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 不选择文件，判断按钮是否可点击
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0002(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
        2、点击本地文件
        3、选择任意文件，点击发送按钮"""
        # 选择html文件发送
        Preconditions.public_send_file('.html')

    def tearDown_test_msg_group_chat_file_location_0002(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0003(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
                2、点击视频文件
                3、不选择文件，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击视频选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 不选择文件，判断按钮是否可点击
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0004(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击视频按钮
            3、选择任意视频，点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击视频选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        time.sleep(2)
        # 3、选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出视频，则循环6次
        for i in range(6):
            el = local_file.select_file2("视频")
            if el:
                local_file.click_send()
                gcp.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_video()
            time.sleep(1)
        # local_file.click_back()
        # csf.click_back()
        gcp.wait_for_page_load()
        raise AssertionError("There is no video")

    def tearDown_test_msg_group_chat_file_location_0004(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0005(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击照片按钮
            3、不选择照片，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击照片选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 不选择文件，判断按钮是否可点击
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0006(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击照片按钮
            3、选择任意照片，点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击照片选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 选择一张照片发送
        local_file = ChatSelectLocalFilePage()
        local_file.wait_for_page_loads()
        el = local_file.select_file2("照片")
        if el:
            local_file.click_send()
            gcp.wait_for_page_load()
        else:
            raise AssertionError("There is no pic")

    def tearDown_test_msg_group_chat_file_location_0006(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0007(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击音乐按钮
            3、不选择音乐，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击音乐选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 不选择文件，判断按钮是否可点击
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0008(self):
        """1、在当前聊天会话页面，点击更多富媒体的文件按钮
            2、点击音乐按钮
            3、选择任意音乐，直接点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击音乐选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 选择一个音乐文件发送
        local_file = ChatSelectLocalFilePage()
        local_file.wait_for_page_loads()
        el = local_file.select_file2("音乐")
        if el:
            local_file.click_send()
            gcp.wait_for_page_load()
        else:
            raise AssertionError("There is no music")

    def tearDown_test_msg_group_chat_file_location_0008(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0009(self):
        """1、在当前文件列表页面长按任意文件
            2、选择转发，选择一个群
            3、点击确定"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_loads()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按转发
        chat_file.forward_file(".html")
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_select_one_group()

        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        if group_names:
            sog.select_one_group_by_name(group_names[0])
            sog.click_sure_forward()
            if not sog.catch_message_in_page("已转发"):
                raise AssertionError("转发失败")
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            time.sleep(1)
        else:
            raise AssertionError("没有群可转发，请创建群")

    def tearDown_test_msg_group_chat_file_location_0009(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0010(self):
        """1、在当前文件列表页面长按任意文件
            2、选择转发，选择一个群
            3、点击取消按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按转发
        chat_file.forward_file(".html")
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_select_one_group()

        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        if group_names:
            sog.select_one_group_by_name(group_names[0])
            sog.click_cancel_forward()
            sog.wait_for_page_load()
            sog.click_back()
            sc.click_back()
            time.sleep(2)
            if chat_file.is_on_this_page():
                chat_file.click_back()
            search.click_back()
            gcsp.click_back()
            time.sleep(1)
        else:
            raise AssertionError("没有群可转发，请创建群")

    def tearDown_test_msg_group_chat_file_location_0010(self):
        # 删除聊天记录
        scp = GroupChatPage()
        time.sleep(2)
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0013(self):
        """1、在当前文件列表页面长按任意文件
            2、选择转发，选择一个本地通讯录联系人
            3、点击确定"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按转发
        time.sleep(3)
        chat_file.forward_file(".html")
        # 选择联系人界面，选择一个本地联系人
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.select_local_contacts()
        time.sleep(2)
        # 选择一个联系人
        sc.click_one_contact("和飞信电话")
        # 点击确认转发
        sc.click_sure_forward()
        # 验证转发成功
        if not sc.catch_message_in_page("已转发"):
            raise AssertionError("转发失败")
        chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0013(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0014(self):
        """1、在当前文件列表页面长按任意文件
            2、选择转发，选择一个本地通讯录联系人
            3、点击取消按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按转发
        chat_file.forward_file(".html")
        # 选择联系人界面，选择一个本地联系人
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.select_local_contacts()
        time.sleep(2)
        sc.click_one_contact("和飞信电话")
        # sc.click_one_local_contacts()
        # 点击取消按钮
        sc.click_cancel_forward()
        # 确保选择联系人页面加载
        sc.wait_for_page_local_contact_load()
        sc.click_back()
        sc.click_back()
        time.sleep(2)
        if chat_file.is_on_this_page():
            chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0014(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0017(self):
        """1、在当前文件列表页面长按任意未下载文件
            2、点击收藏按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按收藏指定类型的文件
        time.sleep(3)
        chat_file.collection_file(".html")
        if not chat_file.is_toast_exist("已收藏"):
            raise AssertionError("收藏验证失败")
        chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0017(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @staticmethod
    def setUp_test_msg_group_chat_file_location_0018():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'group_chat')
    def test_msg_group_chat_file_location_0018(self):
        """1、在当前文件列表页面长按任意未下载文件
            2、点击收藏按钮
            3、查看我-收藏列表"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        # 长按收藏指定类型的文件
        time.sleep(3)
        chat_file.collection_file(".html")
        chat_file.is_toast_exist("已收藏")
        # 返回到消息页面
        time.sleep(2)
        chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)
        # 返回消息页面过程中删除聊天记录
        if gcp.is_on_this_page():
            gcp.click_setting()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(gcp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

        gcp.click_back()
        # sog = SelectOneGroupPage()
        # sog.click_back()
        # sc = SelectContactsPage()
        # sc.click_back()
        # 跳转到我页面
        me = MePage()
        me.open_me_page()
        # 查看收藏页面
        me.click_collection()
        mcp = MeCollectionPage()
        # 检查刚刚收藏的文件是否存在
        mcp.is_toast_exist(".html")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0019(self):
        """1、在当前文件列表页面长按任意文件
            2、点击删除按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        # 等待进入页面
        gcsp.wait_for_page_load()
        # 点击查看聊天内容
        gcsp.click_search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_loads()
        chat_file.delete_file(".html")
        # 返回群聊天页面
        chat_file.click_back()
        search.click_back()
        gcsp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0040(self):
        """1、在当前群聊天会话页面长按任意文件
            2、点击删除按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        # 长按刚刚发送的文件删除
        time.sleep(3)
        gcp.press_file_to_do(".html", "删除")
        # 验证删除成功
        time.sleep(3)
        if gcp.is_text_present(".html"):
            raise AssertionError("删除失败")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0041(self):
        """1、在当前群聊天会话页面长按自己十分钟内发送的文件
            2、点击撤回按钮"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        gcp = GroupChatPage()
        time.sleep(1)
        # 长按刚刚发送的文件撤回
        gcp.press_file_to_do(".html", "撤回")
        time.sleep(2)
        # gcp.click_i_know()
        # 验证撤回成功
        time.sleep(3)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("撤回失败")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0042(self):
        """1、在当前群聊天会话页面长按自己超过十分钟发送的文件
            2、点查看功能菜单"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".html")
        # 等待10分钟
        gcp = GroupChatPage()
        # 超过十分钟,长按自己发送的文件撤回，没有撤回菜单按钮
        for i in range(122):
            time.sleep(2)
            text = gcp.driver.page_source
            del text
            time.sleep(3)
            tmp = gcp.driver.current_activity
            del tmp
            print(i)
        gcp.press_file(".html")
        if gcp.is_text_present("撤回"):
            raise AssertionError("超过十分钟可以撤回")
        time.sleep(2)
        gcp.tap_coordinate([(100, 20), (100, 60), (100,100)])

    def tearDown_test_msg_group_chat_file_location_0042(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0043(self):
        """1、在当前会话窗口点击位置
            2、点击左上角的返回按钮"""
        gcp = GroupChatPage()
        gcp.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 返回会话窗口
        location_page.click_back()
        gcp.wait_for_page_load()
        gcp.click_more()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0044(self):
        """1、在当前会话窗口点击位置
            2、点击右上角的发送按钮"""
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 点击发送按钮
        if not location_page.send_btn_is_enabled():
            raise AssertionError("位置页面发送按钮不可点击")
        location_page.click_send()
        gcp.wait_for_page_load()
        gcp.click_more()
        if not gcp.is_address_text_present():
            raise AssertionError("位置信息发送不成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0045(self):
        """1、在当前会话窗口点击位置
            2、滑动500米内的位置列表，选择其他位置
            3、点击右上角的发送按钮"""
        gcp = GroupChatPage()
        gcp.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 选择其他位置
        location_page.select_other_item()
        # 点击发送按钮
        if not location_page.send_btn_is_enabled():
            raise AssertionError("位置页面发送按钮不可点击")
        location_page.click_send()
        gcp.wait_for_page_load()
        gcp.click_more()
        if not gcp.is_address_text_present():
            raise AssertionError("位置信息发送不成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0046(self):
        """1、在当前会话窗口点击位置
            2、滑动500米内的位置列表，选择其他位置
            3、点击左上角的返回按钮"""
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 选择其他位置
        location_page.select_other_item()
        # 点击返回
        location_page.click_back()
        gcp.wait_for_page_load()
        gcp.click_more()

    def tearDown_test_msg_group_chat_file_location_0046(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @staticmethod
    def public_send_location():
        """发送位置信息"""
        gcp = GroupChatPage()
        gcp.click_more()
        time.sleep(1)
        more_page = ChatMorePage()
        more_page.click_location()
        # 等待位置页面加载
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        time.sleep(1)
        # 点击发送按钮
        if not location_page.send_btn_is_enabled():
            raise AssertionError("位置页面发送按钮不可点击")
        location_page.click_send()
        gcp.wait_for_page_load()
        gcp.click_more()
        if not gcp.is_address_text_present():
            raise AssertionError("位置信息发送不成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0047(self):
        """1、长按位置消息体
            2、点击转发按钮
            3、选择任意本地通讯录联系人进行转发"""
        self.public_send_location()
        # 长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        if names:
            # slcp.select_one_member_by_name(names[0])
            scp.click_one_contact("和飞信电话")
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            raise AssertionError("WARN: There is no linkman.")

    def tearDown_test_msg_group_chat_file_location_0047(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0049(self):
        """1、长按位置消息体
            2、点击转发按钮
            3、选择任意群转发"""
        self.public_send_location()
        # 长按位置消息体转发
        gcp = GroupChatPage()
        gcp.press_message_to_do("转发")
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        if names:
            sogp.select_one_group_by_name(names[0])
            # 3、点击确定
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            raise AssertionError("WARN: There is no group.")

    def tearDown_test_msg_group_chat_file_location_0049(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX')
    def test_msg_group_chat_file_location_0050(self):
        """1、在当前页面点击位置消息体
            2、点击右下角按钮"""
        self.public_send_location()
        time.sleep(2)
        # 点击位置消息体
        gcp = GroupChatPage()
        gcp.click_addr_info()
        # 等待页面加载
        gcp.wait_for_location_page_load()
        # 点击右下角按钮
        gcp.click_nav_btn()
        #判断是否有手机导航应用
        if gcp.is_toast_exist("未发现手机导航应用", timeout=3):
            raise AssertionError("未发现手机导航应用")
        map_flag = gcp.is_text_present("地图")
        self.assertTrue(map_flag)
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        gcp.click_location_back()
        time.sleep(2)


    def tearDown_test_msg_group_chat_file_location_0050(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0051(self):
        """1、在当前会话窗口点击自己发送格式为doc的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".doc")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".doc")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0051(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0052(self):
        """1、在当前会话窗口点击自己发送格式为docx的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".docx")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".docx")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0052(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0053(self):
        """1、在当前会话窗口点击自己发送格式为ppt的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".ppt")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".ppt")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0053(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0054(self):
        """1、在当前会话窗口点击自己发送格式为pptx的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".pptx")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".pptx")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0054(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0055(self):
        """1、在当前会话窗口点击自己发送格式为pdf的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".pdf")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".pdf")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0055(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0056(self):
        """1、在当前会话窗口点击自己发送格式为xls的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".xls")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".xls")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0056(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0057(self):
        """1、在当前会话窗口点击自己发送格式为xlsx的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".xlsx")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".xlsx")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0057(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_file_location_0058(self):
        """1、在当前会话窗口点击自己发送格式为txt的文件"""
        # 先发送一个指定类型的文件
        Preconditions.public_send_file(".txt")
        # 点击发送的文件
        gcp = GroupChatPage()
        gcp.wait_for_message_down_file()
        gcp.open_file_in_chat_page(".txt")
        # 等待文件页面进行加载
        gcp.wait_for_open_file()
        time.sleep(1)
        gcp.click_back_in_open_file_page()
        time.sleep(1)

    def tearDown_test_msg_group_chat_file_location_0058(self):
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            flag = gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面,无法删除记录")
            except AssertionError as e:
                print(e)
