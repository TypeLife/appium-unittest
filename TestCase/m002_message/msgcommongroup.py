import time

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
        """1、在输入框中不输入任何内容，输入框右边展示的按钮是否是语音按钮"""
        #检查是否存在语言按钮
        gcp = GroupChatPage()
        gcp.page_should_contain_audio_btn()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0002(self):
        """1.在输入框中输入一段文本，字符数大于0
            2.点击输入框右边高亮展示的发送按钮，发送此段文本"""
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
        """1.在输入框中输入一段文本，字符数小于5000
            2.点击输入框右边高亮展示的发送按，发送此段文本"""
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
        """1.在当前聊天会话页面，在输入框中输入一段文本，字符数大于5000，是否可以输入此段文本"""
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
        """1.在当前聊天会话页面，在输入框中输入一段文本，字符数等于5000
            2、然后按住发送按钮，向上滑动，放大发送此段文本，文本是否可以放大发送成功"""
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
        """1.在当前聊天会话页面，在输入框中输入一段文本，字符数等于5000
            2、然后按住发送按钮，向下滑动，缩小发送此段文本，文本是否可以缩小发送成功"""
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
        """1、长按文本消息，是否会弹窗展示：功能菜单栏。
            2、点击选择复制功能，复制成功后，是否会弹出toast提示：已复制
            3、长按输入框，是否会弹出粘贴内容到输入框中的提示"""
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
        """1、长按文本消息，是否会弹窗展示：功能菜单栏。
        2、点击选择删除功能，删除成功后，聊天会话页面的消息是否会消失"""
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
        """1、长按文本消息，选择转发功能，是否可以跳转到联系人选择器页面
            2、搜索选择转发对象，选择搜索结果，确认转发后，是否弹出toast提示：已转发
            3、转发成功后，返回到消息列表，是否产生了一个新的会话窗口
            4、进入到新会话窗口页面中，转发的消息，是否已发送成功"""
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
        1、长按文本消息，选择转发功能，是否可以跳转到联系人选择器页面
        2、搜索选择转发对象，选择搜索结果，确认转发后，是否弹出toast提示：已转发
        3、转发成功后，返回到消息列表，是否产生了一个新的会话窗口并且在当前会话窗口上展示一个发送失败的标志：“！”
        4、进入到新会话窗口页面中，转发的消息，是否会展示为发送失败的状态
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
        1、长按文本消息，选择转发功能，是否可以跳转到联系人选择器页面
        2、搜索选择转发对象，选择搜索结果，确认转发后，是否弹出toast提示：已转发
        3、转发成功后，返回到消息列表，是否产生了一个新的会话窗口
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
        """1、点击发送失败消息体，左边的重发按钮，点击重发按钮，是否会弹出确认重新发送的弹窗
            2、点击确认重新发送，是否可以重新发送成功此条消息"""
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
        """1、长按文本消息，选择转发功能，跳转到联系人选择器页面
            2、选择一个群，进入到群聊列表展示页面，任意选中一个群聊，确认转发，是否会在消息列表，
            重新产生一个新的会话窗口或者在已有窗口中增加一条记录
        3、进入到聊天会话窗口页面，转发的消息，是否已发送成功并正常展示"""
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
        """1、长按文本消息，选择转发功能，跳转到联系人选择器页面
            2、选择本地联系人，确认转发，是否会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
            3、进入到聊天会话窗口页面，转发的消息，是否已发送成功并正常展示"""
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
        """1、长按文本消息，选择转发功能，跳转到联系人选择器页面
            2、选择最近聊天，确认转发，是否会在消息列表，重新产生一个新的会话窗口或者在已有窗口中增加一条记录
            3、进入到聊天会话窗口页面，转发的消息，是否已发送成功并正常展示"""
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
        """1、长按文本消息，选择收藏功能，收藏成功后，是否弹出toast提示：已收藏
            2、在我的页面，点击收藏入口，检查刚收藏的消息内容，是否可以正常展示出来
            3、点击收藏成功的消息体，是否可以进入到消息展示详情页面
            4、左滑收藏消息体，是否会展示删除按钮
            5、点击删除按钮，是否可以删除收藏的消息体"""
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
        """1、长按语音消息，选择收藏功能，收藏成功后，是否弹出toast提示：已收藏
            2、在我的页面，点击收藏入口，检查刚收藏的语音消息体，是否可以正常展示出来
            3、点击收藏成功的消息体，是否可以进入到消息展示详情页面
            4、在收藏消息体详情页面，是否可以点击播放和暂停语音消息
            5、左滑收藏消息体，是否会展示删除按钮
            6、点击删除按钮，是否可以删除收藏的消息体"""
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
        """1.点击输入框右边的语音按钮，在未获取录音权限时，是否会弹出权限申请允许弹窗"""
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
        """1、点击输入框右边的语音按钮，跳转到的页面是否是语音模式设置页面
            2、默认展示的选择项是否是，语音+文字模式"""
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
        """1、点击输入框右边的语音按钮，设置语音模式为：语音+文字模式
            2、3秒内未能识别出内容，是否会提示：无法识别，请重试"""
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
        """1、点击输入框右边的语音按钮，设置语音识别模式为：语音+文字模式
            2、语音识别中途，网络异常，是否会展示提示：网络异常，请检查网络后重试"""
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
        """1、点击输入框右边的语音按钮，设置语音模式为：语音+文字模式
            2、3秒内未检测到声音，是否会提示：无法识别，请重试"""
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
        """1、点击输入框右边的语音按钮，设置语音模式为：语音+文字模式
        2、语音+文字模式识别中途，点击左下角的退出按钮，是否会退出语音识别模式"""
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
        """1、点击输入框右边的语音按钮，设置语音模式为：语音转文字模式
            2、3秒内未检测到声音，是否会提示：无法识别，请重试"""
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
        """1、点击输入框右边的语音按钮，设置语音模式为：语音转文字模式
            2、3秒内未能识别出内容，是否会提示：无法识别。请重试"""
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
        """1、点击输入框右边的语音按钮，设置语音模式为：仅语音模式
            2、录制中途，点击左下角的退出按钮，是否可以退出语音录制模式并自动清除已录制的语音文件"""
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
        """1、在输入框中录入内容
            2、长按输入框右边的发送按钮，向上滑动，然后松开手指
            3.发送出去的文本消息，是否是放大展示"""
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
        if not gcp.get_width_of_msg_of_text()>163:
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
        """1、在输入框中录入内容
            2、长按输入框右边的发送按钮，向下滑动，然后松开手指
            3.发送出去的文本消息，是否是缩小展示"""
        gcp = GroupChatPage()
        # 输入信息
        info = "哈哈"
        gcp.input_message(info)
        # 长按发送按钮并滑动
        gcp.press_and_move_down("发送按钮")
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断文本是否缩小,‘哈哈’文本框信息正常宽度为163
        if not gcp.get_width_of_msg_of_text() < 163:
            raise AssertionError("文本消息没有缩小展示")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0041(self):
        """1、在输入框输入一串号码数字
            2、点击输入框右边的发送按钮，是否可以发送成功"""
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
        """
            1、点击聊天会话页面的号码，是否会弹出窗体，展示：呼叫、复制号码
            2、点击呼叫，是否可以发起呼叫"""
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
        """1、在输入框中，录入一组数字：12345678900，点击发送，发送成功后，在消息列表展示状态是否被识别为号码
            2.、点击此组数字，是否会弹出拨打弹窗"""
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
        """1、在输入框中，录入一组数字：123456，点击发送，发送成功后，在消息列表展示状态是否被识别为号码
            2.、点击此组数字，是否会弹出拨打弹窗"""
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
        """1、在输入框中，录入一组数字：18431931414，点击发送，发送成功后，在消息列表展示状态是否被识别为号码
            2.、点击此组数字，是否会弹出拨打弹窗"""
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
        """1、在输入框中，录入一组数字：+85267656003，点击发送，发送成功后，在消息列表展示状态是否被识别为号码
            2.、点击此组数字，是否会弹出拨打弹窗"""
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
        """1、在输入框中，录入一组数字：67656003，点击发送，发送成功后，在消息列表展示状态是否被识别为号码
            2.、点击此组数字，是否会弹出拨打弹窗"""
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
        """1、在输入框中，录入一组数字：95533，点击发送，发送成功后，在消息列表展示状态是否被识别为号码
            2.、点击此组数字，是否会弹出拨打弹窗"""
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
        """
            1、点击聊天会话页面的非号码数字，是否会弹出窗体，展示：呼叫、复制号码"""
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
        """1、在聊天会话页面，点击页面右上角的聊天设置按钮，是否可以正常进入到聊天设置页面"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0051(self):
        """1、在聊天设置页面，点击群成员下方的+号，跳转到联系人选择器页面
            2、未选择联系人时，右上角的确定按钮是否置灰展示"""
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
        """1、在聊天设置页面，点击群成员下方的+号，跳转到联系人选择器页面
            2、选择一个联系人后，右上角的确定按钮是否高亮展示
            3.点击右上角的确定按钮，是否会向被邀请发送一条邀请信息并在聊天会话页面同步提示"""
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


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0053(self):
        """1、在聊天设置页面，点击群成员下方的+号，跳转到联系人选择器页面
        2.选择多个联系人，点击右上角的确定按钮，是否会向被邀请发送一条邀请信息并在聊天会话页面同步提示"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0059(self):
        """1、在聊天设置页面，点击群成员下方的+号，跳转到联系人选择器页面
            2.选择1个联系人，点击右上角的确定按钮，是否会向被邀请发送一条邀请信息并在聊天会话页面同步提示"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0060(self):
        """1.在聊天设置页面，点击群成员下方的移除群成员按钮—号，是否可以进入群成员列表展示页面"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0065(self):
        """1、点击群名称进入到群名称编辑修改页面
            2、清除旧的群名称后，页面右上角的确定按钮是否置灰展示"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0066(self):
        """1、点击群名称进入到群名称编辑修改页面
            2、清除旧名称，录入新的群名称后，页面右上角的确定按钮是否高亮展示
            3、点击高亮展示的确定按钮，群名称自动更改为新名称"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0067(self):
        """1、点击群名片入口，能否进入到群名片修改页面
            2、旧名称右边是否会展示“X”按钮
            3、点击X按钮，是否可以一次清除旧名称
            4、名称修改框为空时，右上角的完成按钮是否置灰展示"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0068(self):
        """1、录入新的内容后，右上角展示的完成按钮是否会高亮展示
            2、在名称输入框中输入10汉字，点击右上角的完成按钮，是否可以保存输入的名称内容"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0069(self):
        """1、在群名片修改页面，录入11个汉字，是否可以录入成功"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0070(self):
        """1、在群名片修改页面，录入30个英文字符，是否可以录入成功
            2、录入成功后，点击右上角的完成按钮，是否可以保存成功"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0071(self):
        """1、在群名片修改页面，录入31个英文字符，是否可以录入成功"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0072(self):
        """1、在群名片修改页面，录入30个数字字符，是否可以录入成功
            2、录入成功后，点击右上角的完成按钮，是否可以保存成功"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0073(self):
        """1、在群名片修改页面，录入中文、英文、数字字符，是否可以录入成功
            2、录入成功后，点击右上角的完成按钮，是否可以保存成功"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0074(self):
        """1、在群名片修改页面，录入特殊字符，（如：表情、符号等等。）是否可以录入成功"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0075(self):
        """1、点击群二维码，是否可以跳转到群二维码分享页面
            2、点击页面右下角的下载按钮，下载成功后，是否会toast提示：已保存"""
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



    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0076(self):
        """1、点击群二维码，是否可以跳转到群二维码分享页面
            2、点击页面左下角的分享按钮，是否可以调起联系人选择器"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0077(self):
        """1、点击群二维码，是否可以跳转到群二维码分享页面
            2、调起联系人选择器，任意选中一个联系人或者群聊，是否会弹出确认弹窗
            5、点击确认按钮，是否可以分享成功"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0078(self):
        """1、点击群管理入口，进入到群管理页面
            2、点击“群主管理权转让”，是否跳转到群成员列表展示页面"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0081(self):
        """1、点击群管理入口，进入到群管理页面
            2、点击“解散群”按钮，是否会弹出确认弹窗
            3、点击取消，是否仍然停留在群管理页面
            4、点击确定，是否会toast提示：该群已解散并系统消息通知：该群已解散"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0087(self):
        """1、点击聊天内容入口，是否可以跳转到聊天内容页面
            2、点击顶部的搜索框，是否可以调起小键盘"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat','DEBUG_YYX1')
    def test_msg_common_group_0088(self):
        """1、在查找聊天内容页面，输入框中，输入中文搜索条件，存在搜索结果时，搜索结果是否展示为：发送人头像、发送人名称、发送的内容、发送的时间
            4、任意选中一条聊天记录，是否会跳转到聊天记录对应的位置"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0089(self):
        """1、在查找聊天内容页面，输入框中，输入数字搜索条件，存在搜索结果时，搜索结果是否展示为：发送人头像、发送人名称、发送的内容、发送的时间
            2、任意选中一条聊天记录，是否会跳转到聊天记录对应的位置"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0090(self):
        """1、在查找聊天内容页面，输入框中，输入英文字母搜索条件，存在搜索结果时，搜索结果是否展示为：发送人头像、发送人名称、发送的内容、发送的时间
            2、任意选中一条聊天记录，是否会跳转到聊天记录对应的位置"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0091(self):
        """1、在查找聊天内容页面，输入框中，输入特殊字符字母搜索条件，存在搜索结果时，搜索结果是否展示为：发送人头像、发送人名称、发送的内容、发送的时间
            2、任意选中一条聊天记录，是否会跳转到聊天记录对应的位置"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0092(self):
        """1、在聊天设置页面
            2、点击清空聊天记录入口功能，是否会弹出聊天记录清除确认弹窗
            3、点击取消或空白处，弹窗是否会消失并且停留在聊天设置页面
            4、点击确定按钮，是否可以清除聊天会话页面的聊天记录
            5、返回到聊天会话页面，聊天会话页的记录是否已全部被清除"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG_YYX1')
    def test_msg_common_group_0094(self):
        """1、在聊天设置页面
            2、点击页面底部的“删除并退出”按钮，是否会弹出确认弹窗
            3、点击取消或者弹窗空白处，是否可以关闭弹窗
            4、点击“确定”按钮，是否会退出当前群聊返回到消息列表并收到一条系统消息：你已退出群"""
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
