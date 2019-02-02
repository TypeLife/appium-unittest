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
from pages.GroupChatSet import GroupChatSetPage

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
    """消息->普通群 模块"""

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        # scp = GroupChatPage()
        # if scp.is_on_this_page():
        #     current_mobile().hide_keyboard_if_display()
        #     return
        # else:
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_common_group_0019(self):
        """1.点击输入框右边的语音按钮，在未获取录音权限时，是否会弹出权限申请允许弹窗"""
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            audio.click_sure()
        # 权限申请允许弹窗判断
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
        flag = audio.wait_for_audio_type_select_page_load()
        self.assertTrue(flag)
        # 2、默认展示的选择项是否是，语音+文字模式
        info = audio.get_selected_item()
        self.assertIn("语音+文字", info)
        audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()