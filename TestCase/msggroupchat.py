import re
import time
import unittest

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *

REQUIRED_MOBILES = {
    'Android-移动': 'single_mobile',
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
    def select_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

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
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
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
        one_key.wait_for_tell_number_load(30)
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_for_page_load(60)

    @staticmethod
    def make_already_in_message_page():
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动')
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_have_my_group():
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
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
    def enter_group_chat_page():
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group()
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
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "mygroup" + phone_number[-4:]
        return group_name


class MsgGroupChatTest(TestCase):
    """消息->群聊 模块"""

    @classmethod
    def setUpClass(cls):
        """进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page()

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    def test_msg_group_chat_0001(self):
        """在群聊聊天会话页面，发送一段字符数等于“0”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中不输入任何内容，输入框右边展示的按钮是否是语音按钮
        gcp = GroupChatPage()
        # 语音按钮检查
        gcp.page_should_contain_audio_btn()

    def test_msg_group_chat_0002(self):
        """在群聊聊天会话页面，发送一段字符数大于“0”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数大于0
        gcp = GroupChatPage()
        info = "Hello everyone!"
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.page_should_contain_send_btn()
        gcp.send_message()
        gcp.page_should_contain_text(info)

    def test_msg_group_chat_0003(self):
        """在群聊聊天会话页面，发送一段字符数小于等于“5000”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数小于5000
        gcp = GroupChatPage()
        info = "Hello everyone, Welcome to my group, I hope my group can bring you happy."
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.page_should_contain_send_btn()
        gcp.send_message()
        gcp.page_should_contain_text(info)

    def test_msg_group_chat_0004(self):
        """在群聊聊天会话页面，发送一段字符数等于“5000”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数等于5000
        gcp = GroupChatPage()
        info = "哈哈" * 2500
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按，发送此段文本
        gcp.page_should_contain_send_btn()
        gcp.send_message()

    def test_msg_group_chat_0006(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        # 点击图片按钮
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.不选择照片时，发送按钮是否置灰展示并且不可点击
        flag = cpg.send_btn_is_enabled()
        self.assertEquals(flag, False)
        # 回到聊天回话页面
        cpg.click_back()

    def test_msg_group_chat_0007(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        # 点击图片按钮
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击右下角高亮展示的发送按钮，发送此照片
        cpg.select_pic()
        # 发送按钮可点击
        self.assertTrue(cpg.send_btn_is_enabled())
        cpg.click_send()

    def test_msg_group_chat_0011(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，直接点击当前选中的图片，是否会放大展示当前图片
        cpg.click_pic_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 3、当前放大图片的左上角是否会展示格式为：当前图片张数/当前相册的总张数
        preview_info = cppp.get_pic_preview_info()
        self.assertIsNotNone(re.match(r'预览\(\d+/\d+\)', preview_info))
        cppp.click_back()
        cpg.click_back()

    def test_msg_group_chat_0012(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选择2张照片后，点击左下角的预览按钮，当前图片预览放大后，右上角的编辑按钮是否已隐藏
        cpp.select_pic(n=2)
        cpp.click_preview()
        pic_preview = ChatPicPreviewPage()
        pic_preview.wait_for_page_load()
        # 3、当前放大页面的右下角发送按钮，是否高亮展示并且展示当前已选择的图片数量
        send_num = pic_preview.get_pic_send_num()
        self.assertEqual(send_num, '2')
        # 4、点击发送按钮，能否进行发送
        pic_preview.click_send()

    def test_msg_group_chat_0013(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.选择9张图片后，相册详情右下角的发送按钮上方是否会高亮展示，并且展示已选择的图片数量
        cpp.select_pic(n=9)
        self.assertTrue(cpp.send_btn_is_enabled())
        send_num = cpp.get_pic_send_num()
        self.assertEqual(send_num, '9')
        # 3.点击相册详情右下角的发送按钮，能否进行发送
        cpp.click_send(times=5)

    def test_msg_group_chat_0014(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前页面选择第10张图片，是否会有提示
        cpp.select_pic(n=10)
        flag = cpp.is_toast_exist("最多只能选择9张照片")
        self.assertTrue(flag)
        cpp.click_back()

    def test_msg_group_chat_0015(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前页面选择图片和视频时，是否会有提示
        cpp.select_pic()
        cpp.select_video()
        flag = cpp.is_toast_exist("不能同时选择照片和视频")
        self.assertTrue(flag)
        cpp.click_back()

    def test_msg_group_chat_0016(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，选择一个视频，右下角的发送按钮是否会高亮展示
        cpp.select_video()
        self.assertTrue(cpp.send_btn_is_enabled())
        cpp.click_back()

    def test_msg_group_chat_0017(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，相册详情中是否会展示其中视频的可播放长度
        times = cpp.get_video_times()
        for time in times:
            self.assertIsNotNone(re.match(r'\d+:\d+', time))
        cpp.click_back()

    def test_msg_group_chat_0018(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，选择一个视频后，点击左下角的预览按钮，是否会以预览模式放大展示当前视频
        # 3、预览展示的视频页面中，是否存在点击可播放的三角形按钮
        # 4、预览播放视频中途，点击左上角的返回按钮，是否可以返回到上一级页面
