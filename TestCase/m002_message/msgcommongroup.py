import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import AgreementDetailPage
from pages import ChatAudioPage
from pages import ChatFilePage
from pages import ChatLocationPage
from pages import ChatMorePage
from pages import ChatSelectFilePage
from pages import ChatSelectLocalFilePage
from pages import ChatWindowPage
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
from pages import SingleChatPage
from pages.chat.ChatGroupAddContacts import ChatGroupAddContactsPage

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
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        if not names:
            raise AssertionError("No contacts, please add contacts in address book.")
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
        group_name = "agroup" + phone_number[-4:]
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

    @staticmethod
    def delete_record_group_chat():
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
            if not gcsp.is_toast_exist("聊天记录清除成功"):
                raise AssertionError("没有聊天记录清除成功弹窗")
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            if not scp.is_on_this_page():
                raise AssertionError("没有返回到群聊页面")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @staticmethod
    def build_one_new_group(group_name):
        """新建一个指定名称的群，如果已存在，不建群"""
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
        time.sleep(2)
        sc.click_select_one_group()
        # 群名
        # group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        a=0
        while a<10:
            group_names = sog.get_group_name()
            # 有群返回，无群创建
            if group_name in group_names:
                sog.click_back()
                sc.click_back()
                return
            a+=1
            sog.page_up()

        sog.click_back()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        slc = SelectLocalContactsPage()
        names = slc.get_contacts_name()
        if not names:
            raise AssertionError("No contacts, please add contacts in address book.")
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
        GroupChatPage().click_back()




class MsgCommonGroupTest(TestCase):
    """
        模块：消息-普通群

        文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
        表格：消息-普通群
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
            current_mobile().reset_app()
            Preconditions.enter_group_chat_page()


    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    @staticmethod
    def setUp_test_msg_common_group_0001():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0001(self):
        """输入框中输入字符数为空"""
        #检查是否存在语言按钮
        gcp = GroupChatPage()
        gcp.page_should_contain_audio_btn()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0002(self):
        """输入框中输入字符数大于0"""
        gcp = GroupChatPage()
        #输入信息
        gcp.input_message("哈哈")
        #点击发送
        gcp.send_message()
        #验证是否发送成功
        cwp=ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    def tearDown_test_msg_common_group_0002(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)



    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0003(self):
        """输入框中输入字符数等于5000"""
        gcp = GroupChatPage()
        # 输入信息
        info="Hello everyone, Welcome to my group, I hope my group can bring you happy."
        gcp.input_message(info)
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    def tearDown_test_msg_common_group_0003(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0004(self):
        """输入框中输入字符数大于5000"""
        gcp = GroupChatPage()
        # 输入信息
        info1 = "哈"*5001
        if len(info1)>5000:
            gcp.input_message(info1)
        #获取输入框信息
        info2=gcp.get_input_message()
        #判断输入框是否最多只能输入5000长度字符
        if len(info1) == len(info2):
            raise AssertionError("输入框能输入大于5000长度的字符")
        if len(info2)==5000:
            return True

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0005(self):
        """向上滑动发送按钮，放大发送输入框中的5000文本字符内容"""
        gcp = GroupChatPage()
        # 输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        #长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    def tearDown_test_msg_common_group_0005(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0006(self):
        """向上滑动发送按钮，缩小发送输入框中的5000文本字符内容"""
        gcp = GroupChatPage()
        # 输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    def tearDown_test_msg_common_group_0006(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0007(self):
        """在聊天会话页面，长按文本消息，使用复制功能"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #长按信息并点击复制
        gcp.press_file_to_do("哈哈","复制")
        flag=gcp.is_toast_exist("已复制")
        self.assertTrue(flag)
        #长按输入框
        gcp.press_file("说点什么...")
        time.sleep(2)
        flag2 = gcp.is_toast_exist("粘贴")
        # self.assertTrue(flag2)

    def tearDown_test_msg_common_group_0007(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                print(e)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0008(self):
        """在聊天会话页面，长按文本消息，使用删除功能"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击删除
        gcp.press_file_to_do("哈哈", "删除")
        #验证消息会消失
        flag=gcp.is_text_present("哈哈")
        self.assertFalse(flag)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0009(self):
        """在聊天会话页面，转发5000字符的文本消息"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        #搜索联系人
        sc.input_search_contact_message("和飞信")
        #选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        sc.click_sure_forward()
        flag=sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        #返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        time.sleep(2)
        sogp.click_back()
        sc.click_back()
        time.sleep(2)
        #判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))
            mess.click_element_by_text("和飞信电话")
            chat = SingleChatPage()
            chat.click_i_have_read()
            chat.wait_for_page_load()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @staticmethod
    def setUp_test_msg_common_group_0010():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0010(self):
        """
        在聊天会话页面，转发5000字符的文本消息
        """
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #断开网络
        gcp.set_network_status(1)
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 搜索联系人
        sc.input_search_contact_message("和飞信")
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))
            #判断是否有“！”
            if  not mess.is_iv_fail_status_present():
                try:
                    raise AssertionError("没有消息发送失败“！”标致")
                except AssertionError as e:
                    print(e)
            #进入新消息窗口判断消息是否发送失败
            mess.click_element_by_text("和飞信电话")
            chat = SingleChatPage()
            chat.click_i_have_read()
            chat.wait_for_page_load()
            try:
                cwp.wait_for_msg_send_status_become_to('发送失败', 10)
            except TimeoutException:
                raise AssertionError('断网情况下消息在 {}s 内发送成功'.format(10))

    def tearDown_test_msg_common_group_0010(self):
        #重新连接网络
        scp = GroupChatPage()
        scp.set_network_status(6)

    @staticmethod
    def setUp_test_msg_common_group_0011():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0011(self):
        """
        在聊天会话页面，长按文本消息，使用转发功能，搜索选择转发对象
        """
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 搜索联系人
        sc.input_search_contact_message("和飞信")
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        #删除群聊消息记录
        gcp.click_setting()
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
        self.assertTrue(gcp.is_on_this_page())
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0012(self):
        """在聊天会话页面，点击重发按钮，重新发送发送失败的消息"""
        gcp = GroupChatPage()
        #断开网络
        gcp.set_network_status(1)
        time.sleep(2)
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送失败
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        except TimeoutException:
            raise AssertionError('断网情况下消息在 {}s 内发送成功'.format(10))
        #重连网络
        gcp.set_network_status(6)
        #判断是否有重发按钮
        if not gcp.is_exist_msg_send_failed_button():
            try:
                raise AssertionError("没有重发按钮")
            except AssertionError as e:
                print(e)
        #点击重发按钮
        gcp.click_msg_send_failed_button()
        #点击确定重发
        gcp.click_resend_confirm()
        #判断信息发送状态
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息未在 {}s 内发送成功'.format(10))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0013(self):
        """在聊天会话页面，长按文本消息，使用转发功能，选择一个群作为转发对象"""
        gcp = GroupChatPage()
        cwp = ChatWindowPage()
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.click_select_one_group()
        # 选择一个群进行转发
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        if group_names:
            sog.select_one_group_by_name(group_names[0])
            sog.click_sure_forward()
            if not sog.catch_message_in_page("已转发"):
                try:
                    raise AssertionError("转发失败")
                except AssertionError as e:
                    print(e)
        else:
            try:
                raise AssertionError("没有群可转发，请创建群")
            except AssertionError as e:
                print(e)

        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present(group_names[0]))
            mess.click_element_by_text(group_names[0])
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @staticmethod
    def setUp_test_msg_common_group_0015():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0015(self):
        """在聊天会话页面，长按文本消息，使用转发功能，选择本地联系人作为转发对象"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(2)
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 删除群聊消息记录
        gcp.click_setting()
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
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))
            mess.click_element_by_text("和飞信电话")
            chat = SingleChatPage()
            chat.click_i_have_read()
            chat.wait_for_page_load()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            time.sleep(2)
            # 最后删除消息记录，返回消息页面结束用例
            mess.press_file_to_do("哈哈","删除")
            chat.click_back()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0016(self):
        """在聊天会话页面，长按文本消息，使用转发功能，选择最近聊天作为转发对象"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 长按信息并点击转发
        gcp.press_file_to_do("哈哈", "转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        # 选择最近聊天中“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        time.sleep(1)
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc.click_back()
        time.sleep(1)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))
            mess.click_element_by_text("和飞信电话")
            chat = SingleChatPage()
            if chat.is_text_present("用户须知"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            #判断是否新增一条消息记录
            if not chat.is_text_present("哈哈"):
                try:
                    raise AssertionError("没有新增一条消息记录")
                except AssertionError as e:
                    print(e)
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            chat.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0017(self):
        """在聊天会话页面，长按文本消息，使用收藏功能"""
        gcp = GroupChatPage()
        # 长按信息并点击收藏
        gcp.press_file_to_do("哈哈", "收藏")
        flag = gcp.is_toast_exist("已收藏")
        self.assertTrue(flag)
        # 删除群聊消息记录
        gcp.click_setting()
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
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc = SelectContactsPage()
        sc.click_back()
        #进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me=MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("哈哈"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp=MeCollectionPage()
        mcp.click_text("哈哈")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        mcp.click_back()
        time.sleep(2)
        #左滑收藏消息体
        mcp.press_and_move_left()
        #判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            time.sleep(2)
            if not mcp.is_text_present("没有任何收藏"):
                raise AssertionError("不可以删除收藏的消息体")
            time.sleep(1)
            mcp.click_back()
            mess.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0018(self):
        """在聊天会话页面，长按语音消息，使用收藏功能"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            #点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        gcp.press_voice_message_to_do("收藏")
        if not gcp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc = SelectContactsPage()
        sc.click_back()
        # 进入我页面
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_collection()
        time.sleep(1)
        if not me.is_text_present("秒"):
            raise AssertionError("收藏的消息内容不能正常展示出来")
        mcp=MeCollectionPage()
        mcp.click_text("秒")
        time.sleep(1)
        if not mcp.is_text_present("详情"):
            raise AssertionError("不能进入到消息展示详情页面")
        #播放语音消息
        mcp.click_collection_voice_msg()
        time.sleep(2)
        #暂停语音消息
        mcp.click_collection_voice_msg()
        mcp.click_back()
        time.sleep(2)
        # 左滑收藏消息体
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            time.sleep(2)
            if not mcp.is_text_present("没有任何收藏"):
                raise AssertionError("不可以删除收藏的消息体")

    @staticmethod
    def setUp_test_msg_common_group_0019():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0019(self):
        """未获取权限时，点击输入框右边的语音按钮，检查是否会弹出提示权限"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        flag = audio.wait_for_audio_allow_page_load()
        self.assertTrue(flag)
        audio.click_allow()
        audio.wait_until(condition=lambda d: audio.is_text_present("退出"))
        audio.click_exit()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0020(self):
        """首次使用语音功能"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        audio.click_send_bottom()
        time.sleep(1)
        audio.click_setting_bottom()
        time.sleep(1)
        # flag = audio.wait_for_audio_type_select_page_load()
        # self.assertTrue(flag)
        # 2、默认展示的选择项是否是，语音+文字模式
        # info = audio.get_selected_item()
        # self.assertIn("语音+文字", info)
        flag=audio.get_audio_and_text_icon_selected()
        self.assertTrue(flag)
        audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0021(self):
        """语音+文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(10)
        audio = ChatAudioPage()
        if not audio.is_text_present("无法识别，请重试"):
            audio.click_exit()
            raise AssertionError("不会提示‘无法识别，请重试’")
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc = SelectContactsPage()
        sc.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0022(self):
        """语音+文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        #断开网络
        gcp.set_network_status(1)
        time.sleep(10)
        audio = ChatAudioPage()
        if audio.is_text_present("我知道了"):
            audio.click_i_know()
        if not audio.is_text_present("网络不可用，请检查网络设置"):
            audio.click_exit()
            raise AssertionError("不会提示‘网络不可用，请检查网络设置’")


    def tearDown_test_msg_common_group_0022(self):
        #重新连接网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(2)
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc = SelectContactsPage()
        sc.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0023(self):
        """语音+文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(10)
        audio = ChatAudioPage()
        if not audio.is_text_present("无法识别，请重试"):
            audio.click_exit()
            raise AssertionError("不会提示‘无法识别，请重试’")
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc = SelectContactsPage()
        sc.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0028(self):
        """语音+文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(2)
        audio = ChatAudioPage()
        audio.click_exit()
        if audio.is_text_present("智能识别中"):
            raise AssertionError("不会退出语音识别模式")
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc = SelectContactsPage()
        sc.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0030(self):
        """语音转文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(10)
        audio = ChatAudioPage()
        if not audio.is_text_present("无法识别，请重试"):
            audio.click_exit()
            raise AssertionError("不会提示‘无法识别，请重试’")
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc = SelectContactsPage()
        sc.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0031(self):
        """语音转文字模式下，发送消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        time.sleep(10)
        audio = ChatAudioPage()
        if not audio.is_text_present("无法识别，请重试"):
            audio.click_exit()
            raise AssertionError("不会提示‘无法识别，请重试’")
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        sc = SelectContactsPage()
        sc.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0036(self):
        """仅语音模式发送语音消息"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        audio.click_send_bottom()
        audio.click_setting_bottom()
        if audio.wait_for_audio_type_select_page_load():
            #点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        else:
            raise AssertionError("语音模式选择页面加载失败")
        time.sleep(2)
        audio.click_exit()
        time.sleep(1)
        if gcp.is_text_present("语音录制中"):
            raise AssertionError("退出语音录制模式失败")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0039(self):
        """放大发送文本消息"""
        gcp = GroupChatPage()
        # 输入信息
        info = "哈哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #判断文本是否放大,‘哈哈’文本框信息正常宽度为163
        if not gcp.get_width_of_msg_of_text()>136:
            raise AssertionError("文本消息没有放大展示")

    def tearDown_test_msg_common_group_0039(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0040(self):
        """缩小发送文本消息"""
        gcp = GroupChatPage()
        #获取文本信息正常的宽度
        info = "哈哈"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width=gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() < width:
            raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0041(self):
        """发送一串号码到聊天会话页面"""
        gcp = GroupChatPage()
        # 输入信息
        info = "123456"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0042(self):
        """点击聊天会话页面中的一组号码数字"""
        gcp = GroupChatPage()
        gcp.click_text("123456")
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("不会弹出呼叫，复制号码窗体")
        gcp.click_text("呼叫")
        time.sleep(2)
        if gcp.is_text_present('需要使用电话权限，您是否允许？'):
            gcp.click_text("始终允许")
        time.sleep(2)
        #判断是否可以发起呼叫
        if not gcp.is_call_page_load():
            raise AssertionError("不可以发起呼叫")
        time.sleep(1)
        #点击结束呼叫按钮
        gcp.click_end_call_button()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0043(self):
        """发送一组数字：12345678900，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "12345678900"
        gcp.input_message(info)
        if gcp.is_keyboard_shown():
            gcp.hide_keyboard()
        time.sleep(1)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #判断是否被识别为号码
        gcp.click_text("12345678900")
        time.sleep(1)
        if gcp.is_text_present("呼叫"):
            raise AssertionError("12345678900被识别为号码,点击有弹窗")

    def tearDown_test_msg_common_group_0043(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0044(self):
        """发送一组数字：123456，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "123456"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("123456")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("123456不被识别为号码,点击没有弹窗")
        time.sleep(1)
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)






    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0045(self):
        """发送一组数字：18431931414，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "18431931414"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("18431931414")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("18431931414不被识别为号码,点击没有弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0046(self):
        """发送一组数字：+85267656003，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "+85267656003"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("+85267656003")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("+85267656003不被识别为号码,点击没有弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0047(self):
        """发送一组数字：67656003，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "67656003"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("67656003")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("67656003不被识别为号码,点击没有弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0048(self):
        """发送一组数字：95533，发送成功后，是否会被识别为号码"""
        gcp = GroupChatPage()
        # 输入信息
        info = "95533"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("95533")
        time.sleep(1)
        if not gcp.is_text_present("呼叫"):
            raise AssertionError("95533不被识别为号码,点击没有弹窗")
        gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0049(self):
        """点击聊天会话页面中的一组非号码数字"""
        gcp = GroupChatPage()
        # 输入非号码数字
        info = "36363"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否被识别为号码
        gcp.click_text("36363")
        time.sleep(1)
        if gcp.is_text_present("呼叫"):
            raise AssertionError("36363被识别为号码,点击有弹窗")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0050(self):
        """在聊天会话页面，点击右上角的聊天设置按钮"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0051(self):
        """聊天设置页面，添加一个群成员"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击“+”按钮
        gcsp.click_add_member()
        contacts_page = SelectLocalContactsPage()
        #未选择联系人时，右上角的确定按钮是否置灰展示
        if contacts_page.is_text_present("确定(1/499)"):
            raise AssertionError("未选择联系人时，右上角的确定按钮没有置灰展示")
        time.sleep(2)
        contacts_page.click_back()
        time.sleep(1)
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0052(self):
        """聊天设置页面，添加一个群成员"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp=ChatGroupAddContactsPage()
        contactNnames=cgacp.get_contacts_name()
        if contactNnames:
            #选择一个联系人
            cgacp.select_one_member_by_name(contactNnames[0])
        else:
            raise AssertionError("通讯录没有联系人，请添加")
        if not cgacp.sure_btn_is_enabled():
            raise AssertionError("右上角的确定按钮不能高亮展示")
        cgacp.click_sure()
        time.sleep(2)
        gcp.is_toast_exist("发出群邀请")

    def tearDown_test_msg_common_group_0052(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0053(self):
        """聊天设置页面，添加多个成员"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp = ChatGroupAddContactsPage()
        contactNnames = cgacp.get_contacts_name()
        if len(contactNnames)>1:
            # 选择多个联系人
            cgacp.select_one_member_by_name(contactNnames[0])
            cgacp.select_one_member_by_name(contactNnames[1])
        else:
            raise AssertionError("通讯录联系人数量不足，请添加")
        cgacp.click_sure()
        time.sleep(2)
        gcp.is_toast_exist("发出群邀请")

    def tearDown_test_msg_common_group_0053(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0059(self):
        """聊天设置页面，添加501个成员"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“+”按钮
        gcsp.click_add_member()
        time.sleep(2)
        cgacp = ChatGroupAddContactsPage()
        contactNnames = cgacp.get_contacts_name()
        if contactNnames:
            # 选择一个联系人
            cgacp.select_one_member_by_name(contactNnames[0])
        else:
            raise AssertionError("通讯录没有联系人，请添加")
        cgacp.click_sure()
        time.sleep(2)
        gcp.is_toast_exist("发出群邀请")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0060(self):
        """聊天设置页面，进入到成员移除页面"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击“-”按钮
        gcsp.click_del_member()
        time.sleep(1)
        if gcsp.is_text_present("移除群成员"):
            raise AssertionError("在一人情况下还可以进入移除群成员页面")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0065(self):
        """聊天设置页面，修改群名称"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        if gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有置灰展示")
        gcsp.click_edit_group_name_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0066(self):
        """聊天设置页面，修改群名称"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        #录入新群名
        gcsp.input_new_group_name("new_group_name")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0067(self):
        """聊天设置页面，修改群名片，清除旧名称"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        gcsp.input_new_group_name("aa")
        #判断是否有“X”按钮
        if gcsp.is_iv_delete_exit():
            #点击“X”按钮
            gcsp.click_iv_delete_button()
            time.sleep(1)
            #判断是否清除成功
            if not gcsp.is_text_present("设置你在群内显示的昵称"):
                raise AssertionError("旧群名片不能清除成功")
            #判断右上角的按钮是否置灰展示
            if gcsp.is_enabled_of_group_card_save_button():
                raise AssertionError("名称修改框为空时，右上角的完成按钮没有置灰展示")
        else:
            raise AssertionError("没有找到“X”按钮")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0068(self):
        """聊天设置页面，修改群名片，录入10个汉字"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        gcsp.input_new_group_name("哈哈哈哈哈哈哈哈哈哈")
        #判断按钮是否高亮展示
        if gcsp.is_enabled_of_group_card_save_button():
            gcsp.save_group_card_name()
            gcsp.is_toast_exist("修改成功")
            time.sleep(2)
            #验证上面输入的名称内容都保存
            gcsp.click_my_card()
            time.sleep(1)
            if not gcsp.get_edit_query_text()=="哈哈哈哈哈哈哈哈哈哈":
                raise AssertionError("不可以保存输入的名称内容")
            gcsp.click_edit_group_card_back()
            gcsp.click_back()
        else:
            raise AssertionError("按钮不会高亮展示")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0069(self):
        """聊天设置页面，修改群名片，录入11个汉字"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        gcsp.input_new_group_name("哈哈哈哈哈哈哈哈哈哈哈")
        time.sleep(1)
        text=gcsp.get_edit_query_text()
        if text=="哈哈哈哈哈哈哈哈哈哈哈":
            raise AssertionError("可录入11个汉字")
        else:
            if not text=="哈哈哈哈哈哈哈哈哈哈":
                raise AssertionError("录入的汉字最多不是10个")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0070(self):
        """聊天设置页面，修改群名片，录入30个英文字符"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName="h"*30
        gcsp.input_new_group_name(newName)
        time.sleep(1)
        if not gcsp.get_edit_query_text()==newName:
            raise AssertionError("录入30个英文字符不可以录入成功")
        gcsp.save_group_card_name()
        gcsp.is_toast_exist("修改成功")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0071(self):
        """聊天设置页面，修改群名片，录入31个英文字符"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName = "j" * 31
        gcsp.input_new_group_name(newName)
        time.sleep(1)
        if gcsp.get_edit_query_text() == newName:
            raise AssertionError("可以录入31个英文字符")
        if not gcsp.get_edit_query_text()=="j"*30:
            raise AssertionError("无法最多录入30个英文字符")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0072(self):
        """聊天设置页面，修改群名片，录入30个数字字符"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName = "1" * 30
        gcsp.input_new_group_name(newName)
        time.sleep(1)
        if not gcsp.get_edit_query_text() == newName:
            raise AssertionError("录入30个英文字符不可以录入成功")
        gcsp.save_group_card_name()
        gcsp.is_toast_exist("修改成功")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0073(self):
        """聊天设置页面，修改群名片，录入中文、英文、数字字符（小于等于30个字符）"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName = "aa11嗯嗯"
        gcsp.input_new_group_name(newName)
        time.sleep(1)
        if not gcsp.get_edit_query_text() == newName:
            raise AssertionError("录入30个英文字符不可以录入成功")
        gcsp.save_group_card_name()
        gcsp.is_toast_exist("修改成功")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0074(self):
        """聊天设置页面，修改群名片、录入特殊字符"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        # 点击“X”按钮
        gcsp.click_iv_delete_button()
        newName = "_(:3」∠❀)_"
        gcsp.input_new_group_name(newName)
        if not gcsp.is_toast_exist("不能包含特殊字符和表情"):
            raise AssertionError("输入特殊字符也可以录入成功")
        gcsp.click_edit_group_card_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0075(self):
        """聊天设置页面，分享群二维码"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击群二维码
        gcsp.click_QRCode()
        gcsp.wait_for_qecode_load()
        gcsp.click_qecode_download_button()
        if not gcsp.is_toast_exist("已保存"):
            raise AssertionError("群二维码保存失败")
        gcsp.click_qecode_back_button()
        gcsp.click_back()



    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0076(self):
        """聊天设置页面，分享群二维码"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群二维码
        gcsp.click_QRCode()
        gcsp.wait_for_qecode_load()
        gcsp.click_qecode_share_button()
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_back()
        gcsp.click_qecode_back_button()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0077(self):
        """聊天设置页面，分享群二维码"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群二维码
        gcsp.click_QRCode()
        gcsp.wait_for_qecode_load()
        gcsp.click_qecode_share_button()
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.select_local_contacts()
        sc.click_one_contact("和飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        gcsp.click_qecode_back_button()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0078(self):
        """聊天设置页面，转让群聊"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击群管理
        gcsp.click_group_manage()
        gcsp.wait_for_group_manage_load()
        #点击群主管理权转让
        gcsp.click_group_manage_transfer_button()
        flag = gcsp.is_toast_exist("暂无群成员")
        self.assertTrue(flag)
        gcsp.click_group_manage_back_button()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0081(self):
        """聊天设置页面，解散群聊"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击群管理
        gcsp.click_group_manage()
        gcsp.wait_for_group_manage_load()
        #点击解散群
        gcsp.click_group_manage_disband_button()
        time.sleep(1)
        if not gcsp.is_text_present("解散群后，所有成员将被移出此群"):
            raise AssertionError("不会弹出确认弹窗")
        #点击取消
        gcsp.click_cancel()
        time.sleep(1)
        if not gcsp.is_text_present("群管理"):
            raise AssertionError("点击取消，不能停留在群管理页面")
        gcsp.click_group_manage_disband_button()
        #点击确定
        gcsp.click_sure()
        if not gcsp.is_toast_exist("该群已解散"):
            raise AssertionError("没有toast提示该群已解散")
        sog = SelectOneGroupPage()
        time.sleep(2)
        if sog.is_on_this_page():
            sog.click_back()
            sc = SelectContactsPage()
            sc.click_back()
        time.sleep(2)
        msg=MessagePage()
        if not msg.is_text_present("该群已解散"):
            raise AssertionError("没有系统消息通知该群已解散")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0087(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击查找聊天内容
        gcsp.click_find_chat_record()
        #点击搜索框
        search = FindChatRecordPage()
        search.wait_for_page_load()
        search.click_edit_query()
        #判断键盘是否调起
        if not search.is_keyboard_shown():
            raise AssertionError("不可以调起小键盘")
        search.click_back()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0088(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天内容
        gcsp.click_find_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_load()
        #输入搜索信息
        search.input_search_message("哈哈")
        #判断各元素的存在
        if not search.is_element_exit("发送人头像"):
            raise AssertionError("展示结果没有发送人头像")
        if not search.is_element_exit("发送人名称"):
            raise AssertionError("展示结果没有发送人名称")
        if not search.is_element_exit("发送的内容"):
            raise AssertionError("展示结果没有发送的内容")
        if not search.is_element_exit("发送的时间"):
            raise AssertionError("展示结果没有发送的时间")
        #任意选中一条聊天记录
        search.click_record()
        time.sleep(2)
        if gcp.is_on_this_page():
            if not gcp.is_text_present("哈哈"):
                raise AssertionError("不会跳转到聊天记录对应的位置")
        else:
            raise AssertionError("不会跳转到聊天记录对应的位置")
        gcp.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)

    def tearDown_test_msg_common_group_0088(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0089(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("123")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天内容
        gcsp.click_find_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_load()
        # 输入搜索信息
        search.input_search_message("123")
        # 判断各元素的存在
        if not search.is_element_exit("发送人头像"):
            raise AssertionError("展示结果没有发送人头像")
        if not search.is_element_exit("发送人名称"):
            raise AssertionError("展示结果没有发送人名称")
        if not search.is_element_exit("发送的内容"):
            raise AssertionError("展示结果没有发送的内容")
        if not search.is_element_exit("发送的时间"):
            raise AssertionError("展示结果没有发送的时间")
        # 任意选中一条聊天记录
        search.click_record()
        time.sleep(2)
        if gcp.is_on_this_page():
            if not gcp.is_text_present("123"):
                raise AssertionError("不会跳转到聊天记录对应的位置")
        else:
            raise AssertionError("不会跳转到聊天记录对应的位置")
        gcp.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)

    def tearDown_test_msg_common_group_0089(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0090(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("abc")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天内容
        gcsp.click_find_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_load()
        # 输入搜索信息
        search.input_search_message("abc")
        # 判断各元素的存在
        if not search.is_element_exit("发送人头像"):
            raise AssertionError("展示结果没有发送人头像")
        if not search.is_element_exit("发送人名称"):
            raise AssertionError("展示结果没有发送人名称")
        if not search.is_element_exit("发送的内容"):
            raise AssertionError("展示结果没有发送的内容")
        if not search.is_element_exit("发送的时间"):
            raise AssertionError("展示结果没有发送的时间")
        # 任意选中一条聊天记录
        search.click_record()
        time.sleep(2)
        if gcp.is_on_this_page():
            if not gcp.is_text_present("abc"):
                raise AssertionError("不会跳转到聊天记录对应的位置")
        else:
            raise AssertionError("不会跳转到聊天记录对应的位置")
        gcp.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)

    def tearDown_test_msg_common_group_0090(self):
        #删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp=GroupChatSetPage()
            gcsp.wait_for_page_load()
            #点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击确认
            gcsp.click_determine()
            flag=gcsp.is_toast_exist("聊天记录清除成功")
            self.assertTrue(flag)
            #点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            #判断是否返回到群聊页面
            self.assertTrue(scp.is_on_this_page())
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0091(self):
        """聊天设置页面，查找聊天内容"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("$%&")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 点击查找聊天内容
        gcsp.click_find_chat_record()
        search = FindChatRecordPage()
        search.wait_for_page_load()
        # 输入搜索信息
        search.input_search_message("$%&")
        # 判断各元素的存在
        if not search.is_element_exit("发送人头像"):
            raise AssertionError("展示结果没有发送人头像")
        if not search.is_element_exit("发送人名称"):
            raise AssertionError("展示结果没有发送人名称")
        if not search.is_element_exit("发送的内容"):
            raise AssertionError("展示结果没有发送的内容")
        if not search.is_element_exit("发送的时间"):
            raise AssertionError("展示结果没有发送的时间")
        # 任意选中一条聊天记录
        search.click_record()
        time.sleep(2)
        if gcp.is_on_this_page():
            if not gcp.is_text_present("$%&"):
                raise AssertionError("不会跳转到聊天记录对应的位置")
        else:
            raise AssertionError("不会跳转到聊天记录对应的位置")
        gcp.click_back()
        search.click_back()
        gcsp.click_back()
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0092(self):
        """聊天设置页面，清空聊天记录"""
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            #点击取消
            gcsp.click_cancel()
            time.sleep(1)
            if not gcsp.is_text_present("群聊设置"):
                raise AssertionError("弹窗消失后不会停留在聊天设置页面")
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
            #验证聊天内容已经被清除
            if scp.is_text_present("$%&"):
                raise AssertionError("聊天内容记录没有被清除")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0094(self):
        """聊天设置页面，删除并退出群聊"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        #点击“删除并退出”按钮
        if not gcsp.is_text_present("删除并退出"):
            gcsp.page_up()
        gcsp.click_delete_and_exit()
        time.sleep(2)
        #验证弹出弹窗
        if not gcsp.is_text_present("退出后不会再接收该群消息"):
            raise AssertionError("没有弹出确认弹窗")
        #点击取消
        gcsp.click_cancel()
        time.sleep(1)
        if gcsp.is_text_present("退出后不会再接收该群信息"):
            raise AssertionError("不可以关闭弹窗")
        #点击确定
        gcsp.click_delete_and_exit()
        time.sleep(1)
        gcsp.click_sure()
        if not gcsp.is_toast_exist("已退出群聊"):
            raise AssertionError("没有toast提示已退出群聊")
        time.sleep(1)
        sog = SelectOneGroupPage()
        if sog.is_on_this_page():
            sog.click_back()
            sc = SelectContactsPage()
            sc.click_back()
        time.sleep(2)
        mess=MessagePage()
        if not mess.is_on_this_page():
            raise AssertionError("退出当前群聊没有返回到消息列表")
        mess.click_element_by_text("系统消息")
        time.sleep(1)
        if not mess.is_text_present("你已退出群"):
            raise AssertionError("没有系统消息：你已退出群")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0096(self):
        """聊天窗口，发送表情"""
        gcp = GroupChatPage()
        #点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        #判断是否可以展示表情页
        if not gcp.is_exist_expression_page():
            raise AssertionError("不可以展示表情页")
        #任意点击一个表情
        els=gcp.get_expressions()
        els[0].click()
        inputText=gcp.get_input_box().get_attribute("text")
        if not inputText==els[0].get_attribute("text"):
            raise AssertionError("被选中的表情不可以存放输入框展示")
        time.sleep(1)
        #清空输入框内容
        gcp.get_input_box().clear()
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0097(self):
        """聊天窗口，发送表情"""
        gcp = GroupChatPage()
        # 点击表情按钮
        gcp.click_expression_button()
        els = gcp.get_expressions()
        a=0
        while a<3:
            els[0].click()
            a+=1
        #判断发送按钮是否高亮
        if not gcp.is_enabled_of_send_button():
            raise AssertionError("发送按钮不可高亮展示")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    def tearDown_test_msg_common_group_0097(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0098(self):
        """聊天窗口，发送表情"""
        gcp = GroupChatPage()
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 判断是否可以展示表情页
        if not gcp.is_exist_expression_page():
            raise AssertionError("不可以展示表情页")
        #连续点击多个表情
        els = gcp.get_expressions()
        a = 0
        while a < 3:
            els[0].click()
            a += 1
        inputText = gcp.get_input_box().get_attribute("text")
        if not inputText==els[0].get_attribute("text")*3:
            raise AssertionError("被选中的表情不可以存放输入框展示")
        time.sleep(1)
        # 清空输入框内容
        gcp.get_input_box().clear()
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0099(self):
        """聊天窗口，放大发送表情"""
        gcp = GroupChatPage()
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        inputText = gcp.get_input_box().get_attribute("text")
        if not inputText == els[0].get_attribute("text"):
            raise AssertionError("被选中的表情不可以存放输入框展示")

        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

        # 判断是否缩小,一个表情文本框信息正常宽度为107
        if not gcp.get_width_of_msg_of_text() > 107:
            raise AssertionError("表情没有放大展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    def tearDown_test_msg_common_group_0099(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0100(self):
        """聊天窗口，缩小发送表情"""
        gcp = GroupChatPage()
        # 获取文本信息正常的宽度
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()
        time.sleep(2)


        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        inputText = gcp.get_input_box().get_attribute("text")
        if not inputText == els[0].get_attribute("text"):
            raise AssertionError("被选中的表情不可以存放输入框展示")

        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

        # 判断是否缩小,一个表情文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() < width:
            raise AssertionError("表情没有缩小展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    def tearDown_test_msg_common_group_0100(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0101(self):
        """聊天会话窗口的批量选择器页面展示"""
        gcp = GroupChatPage()
        # 输入信息
        dex=0
        while dex<3:
            messgage="哈哈"+str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex+=1
        gcp.press_file_to_do("哈哈0","多选")
        #显示左上角的【×】关闭按钮，有勾选消息时，左上角文案展示为： 已选择+数量
        if not gcp.is_exist_multiple_selection_back():
            raise AssertionError("没有显示【×】关闭按钮")
        #验证有勾选信息
        els=gcp.get_multiple_selection_select_box()
        if els[0].get_attribute("checked")=="true":
            if gcp.is_exist_multiple_selection_count():
                if not gcp.is_text_present("已选择"):
                    raise AssertionError("没有显示‘已选择+数量’字样")
            else:
                raise AssertionError("没有显示‘已选择+数量’字样")
            #底部删除、转发按钮，高亮展示
            if not gcp.is_enabled_multiple_selection_delete():
                raise AssertionError("勾选信息后底部删除按钮没有高亮展示")
            if not gcp.is_enabled_multiple_selection_forward():
                raise AssertionError("勾选信息后底部转发按钮没有高亮展示")
        else:
            raise AssertionError("没有勾选信息")
        #取消勾选信息
        els[0].click()
        time.sleep(1)
        #未选择任何消息时，左上角文案展示为：未选择，底部删除，转发按钮默认置灰展示
        if not gcp.is_text_present("未选择"):
            raise AssertionError("未选择任何消息时没有展示‘未选择’")
        # 底部删除、转发按钮，置灰展示
        if gcp.is_enabled_multiple_selection_delete():
            raise AssertionError("未勾选信息后底部删除按钮没有置灰展示")
        if gcp.is_enabled_multiple_selection_forward():
            raise AssertionError("未勾选信息后底部转发按钮没有置灰展示")
        gcp.click_multiple_selection_back()

    def tearDown_test_msg_common_group_0101(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0102(self):
        """下拉是否可加载历史消息"""
        gcp = GroupChatPage()
        # 输入信息
        dex = 0
        while dex < 30:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.click_back()
        time.sleep(1)
        groupName=Preconditions.get_group_chat_name()
        gcp.click_text(groupName)
        time.sleep(1)
        gcp.press_file_to_do("哈哈26", "多选")
        gcp.page_down()
        time.sleep(2)
        if not gcp.is_text_present("哈哈9"):
            raise AssertionError("下滑加载历史信息不成功")
        gcp.click_multiple_selection_back()

    def tearDown_test_msg_common_group_0102(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0103(self):
        """取消多选模式"""
        gcp = GroupChatPage()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        gcp.click_multiple_selection_back()
        if gcp.is_exist_multiple_selection_select_box():
            raise AssertionError("复选框没有消失")
        #转发操作选项直接消失
        if gcp.is_text_present("转发"):
            raise AssertionError("转发操作选项没有消失")
        #出现底部聊天输入框
        if not gcp.is_text_present("说点什么..."):
            raise AssertionError("底部聊天输入框没有出现")
        #返回到聊天会话窗口
        if not gcp.is_on_this_page():
            raise AssertionError("没有返回到聊天会话窗口")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0104(self):
        """转发默认选中项（1条）—如下消息体是不支持转发的类型（①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体）"""
        gcp = GroupChatPage()
        time.sleep(1)
        gcp.press_file_to_do("哈哈0", "多选")
        gcp.click_text("转发")
        time.sleep(2)
        if not gcp.is_text_present("选择联系人"):
            raise AssertionError("不符合UI设计")
        scp=SelectContactsPage()
        scp.click_back()
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0105(self):
        """转发默认选中项（1条）—如下消息体是不支持转发的类型（①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体）"""
        gcp = GroupChatPage()
        time.sleep(1)
        gcp.press_file_to_do("哈哈0", "多选")
        time.sleep(1)
        gcp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        sc.click_cancel_forward()
        sc.click_back()
        sc.click_back()
        time.sleep(1)
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0106(self):
        """转发默认选中项（1条）—当消息体是支持转发的类型——网络正常转发"""
        gcp = GroupChatPage()
        gcp.press_file_to_do("哈哈0", "多选")
        time.sleep(1)
        gcp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        sc.click_sure_forward()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0108(self):
        """转发默认选中项（1条）—删除"""
        gcp = GroupChatPage()
        gcp.press_file_to_do("哈哈0", "多选")
        time.sleep(1)
        #点击删除
        gcp.click_multiple_selection_delete()
        #点击确定
        gcp.click_multiple_selection_delete_sure()
        flag = gcp.is_toast_exist("删除成功")
        self.assertTrue(flag)
        if gcp.is_text_present("哈哈0"):
            raise AssertionError("删除掉的消息体没有删除成功")

    def tearDown_test_msg_common_group_0108(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0109(self):
        """转发默认选中项（1条）—取消删除"""
        gcp = GroupChatPage()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        time.sleep(1)
        # 点击删除
        gcp.click_multiple_selection_delete()
        # 点击取消
        gcp.click_multiple_selection_delete_cancel()
        #验证选中的消息体还是选中状态
        els = gcp.get_multiple_selection_select_box()
        if not els[0].get_attribute("checked")=="true":
            raise AssertionError("选中的消息体不是选中状态")
        time.sleep(1)
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0110(self):
        """取消默认选中项"""
        gcp = GroupChatPage()
        gcp.press_file_to_do("哈哈0", "多选")
        els=gcp.get_multiple_selection_select_box()
        if els:
            els[0].click()
        else:
            raise AssertionError("没有找到复选框")
        time.sleep(1)
        if not gcp.is_text_present("未选择"):
            raise AssertionError("标题没有变化为“未选择”")
        #验证删除和转发按钮是否置灰
        if gcp.is_enabled_multiple_selection_delete():
            raise AssertionError("删除按钮没有置灰")
        if gcp.is_enabled_multiple_selection_forward():
            raise AssertionError("转发按钮没有置灰")
        time.sleep(1)
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX')
    def test_msg_common_group_0111(self):
        """选择多条消息体"""
        gcp = GroupChatPage()
        gcp.press_file_to_do("哈哈0", "多选")
        #点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        #验证其他复选框被选中
        if not els[1].get_attribute("checked")=="true" and els[2].get_attribute("checked")=="true":
            raise AssertionError("点击的消息体没有被选中")
        time.sleep(1)
        gcp.click_multiple_selection_back()

    @staticmethod
    def setUp_test_msg_common_group_0112():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0112(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络正常"""
        gcp = GroupChatPage()
        # 输入信息
        dex = 0
        while dex < 3:
            messgage = "哈哈" + str(dex)
            gcp.input_message(messgage)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1

        # 发送语音
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()

        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
            els[3].click()
        else:
            raise AssertionError("没有找到复选框")
        time.sleep(1)
        #点击转发
        gcp.click_multiple_selection_forward()
        #点击取消
        gcp.click_cancel_repeat_msg()
        #验证停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
           raise AssertionError("点击取消没有停留在批量选择器页面")
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击确定
        gcp.click_sure_repeat_msg()
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        # 点击取消
        gcp.click_cancel_repeat_msg()
        #验证停留在最近聊天选择器页面
        if not gcp.is_text_present("选择联系人"):
           raise AssertionError("没有停留在最近聊天选择器页面")
        sc.click_one_contact("和飞信电话")
        # 点击确定
        gcp.click_sure_repeat_msg()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        time.sleep(2)
        sogp.click_back()
        sc.click_back()
        time.sleep(2)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))
            mess.click_element_by_text("和飞信电话")
            chat = SingleChatPage()
            chat.click_i_have_read()
            chat.wait_for_page_load()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            if chat.is_audio_exist():
                raise AssertionError("不支持转发的消息体没有被过滤掉")
            chat.click_back()
            time.sleep(2)
            mess.press_file_to_do("和飞信电话","删除聊天")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0113(self):
        """当转发的消息体中包含不支持转发的类型：①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体——网络异常"""
        gcp = GroupChatPage()
        #断开网络
        gcp.set_network_status(0)
        time.sleep(2)
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
            els[3].click()
        else:
            raise AssertionError("没有找到复选框")
        time.sleep(1)
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
            raise AssertionError("点击取消没有停留在批量选择器页面")
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击确定
        gcp.click_sure_repeat_msg()
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在最近聊天选择器页面
        if not gcp.is_text_present("选择联系人"):
            raise AssertionError("没有停留在最近聊天选择器页面")
        sc.click_one_contact("和飞信电话")
        # 点击确定
        gcp.click_sure_repeat_msg()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        time.sleep(2)
        sogp.click_back()
        sc.click_back()
        time.sleep(2)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))
            mess.click_element_by_text("和飞信电话")
            chat = SingleChatPage()
            if chat.is_text_present("用户须知"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            # 验证是否发送失败
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送失败', 10)
            except TimeoutException:
                raise AssertionError('断网情况下消息在 {}s 内发送成功'.format(10))
            # 判断是否有重发按钮
            if not gcp.is_exist_msg_send_failed_button():
                try:
                    raise AssertionError("没有重发按钮")
                except AssertionError as e:
                    raise e
            if chat.is_audio_exist():
                raise AssertionError("不支持转发的消息体没有被过滤掉")
            chat.click_back()
            time.sleep(2)
            mess.press_file_to_do("和飞信电话", "删除聊天")

    def tearDown_test_msg_common_group_0113(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0114(self):
        """当消息体都是不支持转发的类型（①未下载的图片/视频/文件  ②语音、红包、卡券等特殊消息体）"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        #发送多条语音
        dex = 0
        while dex < 2:
            # 发送语音
            gcp.click_audio_btn()
            audio = ChatAudioPage()
            # if audio.wait_for_audio_type_select_page_load():
            #     # 点击只发送语言模式
            #     audio.click_only_voice()
            #     audio.click_sure()
            # # 权限申请允许弹窗判断
            # time.sleep(1)
            # audio.click_allow()
            time.sleep(3)
            audio.click_send_bottom()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            audio.click_exit()
            gcp.hide_keyboard()
            dex+=1
        gcp.press_audio_to_do("多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
        else:
            raise AssertionError("没有找到其他复选框")
        # 验证其他复选框被选中
        if not els[1].get_attribute("checked")=="true":
            raise AssertionError("点击的消息体没有被选中")
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
            raise AssertionError("点击取消没有停留在批量选择器页面")
        # 点击转发
        gcp.click_multiple_selection_forward()
        # 点击确定
        gcp.click_sure_repeat_msg()
        # 验证停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
            raise AssertionError("点击取消没有停留在批量选择器页面")
        if not els[0].get_attribute("checked")=="true" and els[1].get_attribute("checked")=="true":
            raise AssertionError("点击的消息体没有被选中")
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0115(self):
        """当消息体是支持转发的类型——网络正常转发"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            message = "哈哈" + str(dex)
            gcp.input_message(message)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        # 点击转发
        gcp.click_multiple_selection_forward()
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在最近聊天选择器页面
        if not gcp.is_text_present("选择联系人"):
            raise AssertionError("没有停留在最近聊天选择器页面")
        sc.click_one_contact("和飞信电话")
        # 点击确定
        gcp.click_sure_repeat_msg()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        time.sleep(2)
        sogp.click_back()
        sc.click_back()
        time.sleep(2)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))
            mess.click_element_by_text("和飞信电话")
            chat = SingleChatPage()
            if chat.is_text_present("用户须知"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            chat.click_back()
            time.sleep(2)
            mess.press_file_to_do("和飞信电话", "删除聊天")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0116(self):
        """当消息体是支持转发的类型——网络异常转发"""
        gcp = GroupChatPage()
        time.sleep(2)
        # 断开网络
        gcp.set_network_status(0)
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        # 点击转发
        gcp.click_multiple_selection_forward()
        sc = SelectContactsPage()
        sc.wait_for_page_local_contact_load()
        sc.select_local_contacts()
        time.sleep(1)
        # 选择“和飞信电话”联系人进行转发
        sc.click_one_contact("和飞信电话")
        # 点击取消
        gcp.click_cancel_repeat_msg()
        # 验证停留在最近聊天选择器页面
        if not gcp.is_text_present("选择联系人"):
            raise AssertionError("没有停留在最近聊天选择器页面")
        sc.click_one_contact("和飞信电话")
        # 点击确定
        gcp.click_sure_repeat_msg()
        flag = sc.is_toast_exist("已转发")
        self.assertTrue(flag)
        # 返回消息页面
        gcp.click_back()
        sogp = SelectOneGroupPage()
        time.sleep(2)
        sogp.click_back()
        sc.click_back()
        time.sleep(2)
        # 判断消息页面有新的会话窗口
        mess = MessagePage()
        if mess.is_on_this_page():
            self.assertTrue(mess.is_text_present("和飞信电话"))
            mess.click_element_by_text("和飞信电话")
            chat = SingleChatPage()
            if chat.is_text_present("用户须知"):
                chat.click_i_have_read()
            chat.wait_for_page_load()
            # 验证是否发送失败
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送失败', 10)
            except TimeoutException:
                raise AssertionError('断网情况下消息在 {}s 内发送成功'.format(10))
            # 判断是否有重发按钮
            if not gcp.is_exist_msg_send_failed_button():
                try:
                    raise AssertionError("没有重发按钮")
                except AssertionError as e:
                    raise e
            if chat.is_audio_exist():
                raise AssertionError("不支持转发的消息体没有被过滤掉")
            chat.click_back()
            time.sleep(2)
            mess.press_file_to_do("和飞信电话", "删除聊天")

    def tearDown_test_msg_common_group_0116(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0117(self):
        """删除选中的消息体"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            message = "哈哈" + str(dex)
            gcp.input_message(message)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        #被点到的相对应消息体被选中
        if not (els[2].get_attribute("checked")=="true" and els[1].get_attribute("checked")=="true"):
            raise AssertionError("点击的消息体没有被选中")
        # 点击删除
        gcp.click_multiple_selection_delete()
        #点击确定
        gcp.click_multiple_selection_delete_sure()
        flag = gcp.is_toast_exist("删除成功")
        self.assertTrue(flag)
        #验证删除掉的消息体已删除成功
        if gcp.is_text_present("哈哈0"):
            raise AssertionError("删除掉的消息体没有删除成功")
        if gcp.is_text_present("哈哈1"):
            raise AssertionError("删除掉的消息体没有删除成功")
        if gcp.is_text_present("哈哈2"):
            raise AssertionError("删除掉的消息体没有删除成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0118(self):
        """取消删除选中的消息体"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 3:
            message = "哈哈" + str(dex)
            gcp.input_message(message)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        gcp.press_file_to_do("哈哈0", "多选")
        # 点击其他复选框
        els = gcp.get_multiple_selection_select_box()
        if els:
            els[1].click()
            els[2].click()
        else:
            raise AssertionError("没有找到复选框")
        # 被点到的相对应消息体被选中
        if not (els[2].get_attribute("checked")=="true" and els[1].get_attribute("checked")=="true"):
            raise AssertionError("点击的消息体没有被选中")
        # 点击删除
        gcp.click_multiple_selection_delete()
        # 点击取消
        gcp.click_multiple_selection_delete_cancel()
        #验证还停留在批量选择器页面
        if not gcp.is_text_present("已选择"):
            raise AssertionError("没有停留在批量选择器页面")
        #验证选中的消息体还在选中状态
        if not (els[2].get_attribute("checked")=="true" and els[1].get_attribute("checked")=="true" and els[0].get_attribute("checked")=="true"):
            raise AssertionError("选中的消息体没有在选中状态")
        time.sleep(2)
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0119(self):
        """选择第101条消息体"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        dex = 0
        while dex < 101:
            message = "哈哈" + str(dex)
            gcp.input_message(message)
            # 点击发送
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            dex += 1
        while not gcp.is_text_present("哈哈0"):
            gcp.page_down()
        gcp.press_file_to_do("哈哈0", "多选")
        while not gcp.is_text_present("哈哈100"):
            els = gcp.get_multiple_selection_select_box()
            for el in els:
                flag = el.get_attribute("checked")
                if not flag == "true":
                    el.click()
            gcp.page_up()
        count=gcp.get_multiple_selection_count()
        a = int(count.get_attribute("text"))
        num=101-a-1
        i=0
        while i<num:
            mess="哈哈"+str(a)
            gcp.click_text(mess)
            a+=1
            i+=1
        gcp.click_text("哈哈100")
        if not gcp.is_toast_exist("聊天消息多选最多支持选择100条"):
            raise AssertionError("不会toast提示")
        gcp.click_multiple_selection_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0156(self):
        """发送失败的消息，长按撤回"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.set_network_status(0)
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送失败
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
        gcp.press_file("哈哈0")
        if gcp.is_text_present("撤回"):
            raise AssertionError("长按发送失败的消息体存在撤回按钮")
        gcp.tap_coordinate([(100, 20), (100, 60), (100,100)])

    def tearDown_test_msg_common_group_0156(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0158(self):
        """撤回，发送成功不足一分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("哈哈0","撤回")
        time.sleep(1)
        if gcp.is_text_present("发送时间超10分钟的消息，不能被撤回"):
            gcp.click_text("知道了")
        time.sleep(1)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0159(self):
        """撤回，发送成功不足一分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #断开网络
        gcp.set_network_status(0)
        time.sleep(2)
        gcp.press_file_to_do("哈哈0", "撤回")
        if not gcp.is_toast_exist("当前网络不可用，请检查网络设置"):
            raise AssertionError("没有toast提示")
        if not gcp.is_text_present("哈哈0"):
            raise AssertionError("网络异常时撤回成功")

    def tearDown_test_msg_common_group_0159(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0160(self):
        """撤回，发送成功时间，超过一分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(62)
        gcp.press_file_to_do("哈哈0", "撤回")
        time.sleep(1)
        if gcp.is_text_present("发送时间超10分钟的消息，不能被撤回"):
            gcp.click_text("知道了")
        time.sleep(1)
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0162(self):
        """撤回，发送成功时间，超过10分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        #等待超过十分钟
        a=1
        while a<11:
            time.sleep(60)
            gcp.get_input_box()
            print("{}分钟".format(a))
            a+=1
        gcp.press_file("哈哈0")
        if gcp.is_text_present("撤回"):
            raise AssertionError("存在撤回按钮")

    @staticmethod
    def setUp_test_msg_common_group_0164():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0164(self):
        """APP端第一次使用撤回功能"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        gcp.input_message("哈哈0")
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.press_file_to_do("哈哈0", "撤回")
        time.sleep(1)
        if gcp.is_text_present("发送时间超10分钟的消息，不能被撤回"):
            gcp.click_text("知道了")
        else:
            raise AssertionError("没有弹窗出现")
        if gcp.is_text_present("哈哈0"):
            raise AssertionError("消息撤回失败")
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("不会展示：你撤回了一条信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0165(self):
        """撤回，发送成功不足一分钟的语音消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        gcp.press_voice_message_to_do("撤回")
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0166(self):
        """网络异常，撤回，发送成功不足一分钟的语音消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        time.sleep(1)
        #断开网络
        gcp.set_network_status(0)
        time.sleep(2)
        gcp.press_voice_message_to_do("撤回")
        if not gcp.is_toast_exist("当前网络不可用，请检查网络设置"):
            raise AssertionError("没有toast提示")
        if gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("网络异常时成功撤回信息")

    def tearDown_test_msg_common_group_0166(self):
        #重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0167(self):
        """撤回，发送成功的语音消息，时间超过一分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        # 等待超过一分钟
        a = 1
        while a < 3:
            time.sleep(60)
            gcp.get_input_box()
            print("{}分钟".format(a))
            a += 1
        gcp.press_voice_message_to_do("撤回")
        if not gcp.is_text_present("你撤回了一条信息"):
            raise AssertionError("没有成功撤回信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0169(self):
        """撤回，发送成功的语音消息，时间超过10分钟的消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        # 等待超过十分钟
        a = 1
        while a < 11:
            time.sleep(60)
            gcp.get_input_box()
            print("{}分钟".format(a))
            a += 1
        gcp.press_voice_message()
        if gcp.is_text_present("撤回"):
            raise AssertionError("存在撤回按钮")
        gcp.tap_coordinate([(100, 20), (100, 60), (100,100)])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0170(self):
        """发送一条语音消息，在9分55秒时，长按展示功能菜单列表"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        audio.click_send_bottom()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        audio.click_exit()
        gcp.hide_keyboard()
        # 等待到九分钟以上
        a = 1
        while a < 10:
            time.sleep(60)
            gcp.get_input_box()
            print("{}分钟".format(a))
            a += 1
        gcp.press_voice_message()
        time.sleep(60)
        gcp.click_text("撤回")
        if gcp.is_toast_exist("发送时间超10分钟的消息，不能被撤回"):
            gcp.click_text("知道了")
        if gcp.is_toast_exist("你撤回了一条信息"):
            raise AssertionError("消息超过十秒可以撤回")



class MsgCommonGroupAllTest(TestCase):
    """
            模块：消息-普通群

            文件位置：1.1.3全量测试用例\113和飞信全量测试用例-肖秋.xlsx
            表格：和飞信全量测试用例
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
            current_mobile().reset_app()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    @staticmethod
    def setUp_test_msg_common_group_all_0001():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL','CMCC','group_chat','full')
    def test_msg_common_group_all_0001(self):
        """消息列表——发起群聊——选择已有群"""
        # 1、点击右上角的+号，发起群聊
        # 2、点击选择一个群，是否可以进入到群聊列表展示页面
        # 3、中文模糊搜索，是否可以匹配展示搜索结果
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        #先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "啊测测试试":
            raise AssertionError("无法中文模糊搜索")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0002():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0002(self):
        """消息列表——发起群聊——选择已有群"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊啊测")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0003():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0003(self):
        """群聊列表展示页面——中文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊测测试试")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "啊测测试试":
            raise AssertionError("无法中文精确搜索")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0004():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0004(self):
        """群聊列表展示页面——中文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("啊测测试试")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("啊测测试试啊")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0005():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0005(self):
        """群聊列表展示页面——英文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("atteesstt")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("atteesstt")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "atteesstt":
            raise AssertionError("无法英文精确搜索")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0006():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0006(self):
        """群聊列表展示页面——英文精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("atteesstt")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("aatteesstt")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0007():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0007(self):
        """群聊列表展示页面——空格精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("a a")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword(" ")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "a a":
            raise AssertionError("无法空格精确搜索")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0008():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0008(self):
        """群聊列表展示页面——空格精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("a a")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("  ")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0009():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0009(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("112233445566")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "112233445566":
            raise AssertionError("无法数字精确搜索")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0010():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat','full')
    def test_msg_common_group_all_0010(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("1112233445566")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0011():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0011(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("112233445566")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "112233445566":
            raise AssertionError("无法数字精确搜索")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0012():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0012(self):
        """群聊列表展示页面——数字精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("112233445566")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("1112233445566")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0013():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0013(self):
        """群聊列表展示页面——字符精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("$$")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("$$")
        time.sleep(2)
        els = sog.get_search_result_group()
        if not els[0].get_attribute("text") == "$$":
            raise AssertionError("无法字符精确搜索")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0014():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0014(self):
        """群聊列表展示页面——字符精确搜索"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("$$")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        sog.input_search_keyword("$$$")
        time.sleep(2)
        if not sog.is_text_present("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sog.click_back_icon()
        sog.click_back()
        sc.click_back()

    @staticmethod
    def setUp_test_msg_common_group_all_0015():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0015(self):
        """群聊列表展示页面——索引字母定位选择"""
        # 先保证有特定名称的群
        Preconditions.build_one_new_group("iiiiii")
        # 先点击加号
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_text("I")
        time.sleep(2)
        if not sog.is_text_present("iiiiii"):
            raise AssertionError("索引字母不能进行定位")
        sog.click_back()
        sc.click_back()

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0017(self):
        """在群聊天会话页面，发送一条字符长度等于：1的，文本消息"""
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈")
        if gcp.is_audio_btn_exit():
            raise AssertionError("右边的语音按钮不会自动变为发送按钮")
        gcp.page_should_contain_send_btn()
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0018(self):
        """在群聊天会话页面，发送一条字符长度，大于1的文本消息"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 输入信息
        mess="哈"*10
        gcp.input_message(mess)
        if gcp.is_audio_btn_exit():
            raise AssertionError("右边的语音按钮不会自动变为发送按钮")
        gcp.page_should_contain_send_btn()
        # 点击发送
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0021(self):
        """在群聊天会话页面，输入框中录入1个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        # if not gcp.get_width_of_msg_of_text() <= width:
        #     raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0022(self):
        """在群聊天会话页面，输入框中录入500个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的高度
        info = "哈"*500
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        height= gcp.get_height_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"*500
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,文本框信息正常高度为height
        if not gcp.get_height_of_msg_of_text() < height:
            raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0023(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用缩小功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的高度
        info = "哈" * 5000
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        height = gcp.get_height_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,文本框信息正常高度为height
        # if not gcp.get_height_of_msg_of_text() <= height:
        #     raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0024(self):
        """在群聊天会话页面，输入框中录入1个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() > width:
            raise AssertionError("文本消息没有放大展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0025(self):
        """在群聊天会话页面，输入框中录入500个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈"*500
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈"*500
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        # if not gcp.get_width_of_msg_of_text() > width:
        #     raise AssertionError("文本消息没有放大展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full')
    def test_msg_common_group_all_0026(self):
        """在群聊天会话页面，输入框中录入5000个字符，使用放大功能发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取文本信息正常的宽度
        info = "哈" * 5000
        gcp.input_message(info)
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        info = "哈" * 5000
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
            # if not gcp.get_width_of_msg_of_text() > width:
            #     raise AssertionError("文本消息没有放大展示")

    @tags('ALL', 'CMCC', 'group_chat', 'full','full-yyx')
    def test_msg_common_group_all_0028(self):
        """进入到群聊天会话页面，录入500个表情字符，缩小发送"""
        gcp=GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        i=0
        while i<500:
            els[0].click()
            i+=1
        # inputText = gcp.get_input_box().get_attribute("text")
        # if not inputText == els[0].get_attribute("text")*500:
        #     raise AssertionError("被选中的表情不可以存放输入框展示")

        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','full-yyx')
    def test_msg_common_group_all_0032(self):
        """进入到群聊天会话页面，录入500个表情字符，放大发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        i = 0
        while i < 500:
            els[0].click()
            i += 1
        # inputText = gcp.get_input_box().get_attribute("text")
        # if not inputText == els[0].get_attribute("text") * 500:
        #     raise AssertionError("被选中的表情不可以存放输入框展示")

        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','full-yyx')
    def test_msg_common_group_all_0035(self):
        """进入到群聊天会话页面，录入文字+表情字符，放大发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        gcp.input_message(info)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        # 长按发送按钮并滑动
        gcp.press_and_move_up("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() > width:
            raise AssertionError("文本消息没有放大展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()

    @tags('ALL', 'CMCC', 'group_chat', 'full','full-yyx')
    def test_msg_common_group_all_0036(self):
        """进入到群聊天会话页面，录入文字+表情字符，缩小发送"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        # 获取信息正常的宽度
        info = "哈"
        gcp.input_message(info)
        # 点击表情按钮
        gcp.click_expression_button()
        time.sleep(2)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        width = gcp.get_width_of_msg_of_text()
        Preconditions.delete_record_group_chat()
        time.sleep(2)
        # 再继续输入信息
        gcp.input_message(info)
        # 任意点击一个表情
        els = gcp.get_expressions()
        els[0].click()
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为width
        if not gcp.get_width_of_msg_of_text() < width:
            raise AssertionError("文本消息没有放大展示")
        gcp.click_expression_page_close_button()
        gcp.hide_keyboard()


