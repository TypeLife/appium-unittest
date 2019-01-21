import random
import time
import re
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *

REQUIRED_MOBILES = {
    # 'Android-移动': 'single_mobile',
    'Android-移动': 'M960BDQN229CH',
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
        message_page.wait_for_page_load(60)

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def enter_private_chat_page(reset=False):
        """进入单聊会话页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        chat = SingleChatPage()
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
        contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()
        # 点击消息进入单聊会话页面
        cdp.click_message_icon()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        chat.wait_for_page_load()


class MsgPrivateChatVideoPicTest(TestCase):
    """消息->单聊视频,图片 模块"""

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """确保每个用例运行前在单聊会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0001(self):
        """单聊会话页面，不勾选相册内图片点击发送按钮"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.不选择照片时，发送按钮是否置灰展示并且不可点击
        flag = cpg.send_btn_is_enabled()
        self.assertEquals(flag, False)
        # 回到聊天回话页面
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0002(self):
        """单聊会话页面，勾选相册内一张图片发送"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击右下角高亮展示的发送按钮，发送此照片
        cpg.select_pic()
        # 发送按钮可点击
        self.assertTrue(cpg.send_btn_is_enabled())
        cpg.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0003(self):
        """单聊会话页面，预览相册内图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击左下角的预览按钮
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_back()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0004(self):
        """单聊会话页面，预览相册内图片，不勾选原图发送"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击左下角的预览按钮
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 3.直接点击发送按钮
        cppp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0005(self):
        """单聊会话页面，预览相册数量与发送按钮数量一致"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.选择多张照片，点击左下角的预览按钮
        cpp.select_pic(n=3)
        cpp.click_preview()
        pic_preview = ChatPicPreviewPage()
        pic_preview.wait_for_page_load()
        # 3.查看发送按钮数字
        send_num = pic_preview.get_pic_send_num()
        self.assertEqual(send_num, '3')
        pic_preview.click_back()
        cpp.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def public_edit_pic():
        """图片编辑操作"""
        # 1.在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击右上角编辑按钮，进行涂鸦、马赛克、文本编辑
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_edit()
        pic = ChatPicEditPage()
        # 涂鸦
        pic.click_doodle()
        pic.do_doodle()
        # 马赛克
        pic.click_mosaic()
        pic.do_mosaic()
        # 文本编辑
        pic.click_text_edit_btn()
        pic.input_pic_text()
        # 完成
        pic.click_save()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0006(self):
        """单聊会话页面，编辑图片发送"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击保存按钮
        pic.click_save()
        # 4.点击发送
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0007(self):
        """单聊会话页面，编辑图片不保存发送"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 4.点击发送按钮
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0008(self):
        """单聊会话页面，编辑图片中途直接发送"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击发送
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0009(self):
        """单聊会话页面，编辑图片保存"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击保存
        pic.click_save()
        flag = pic.is_toast_exist("保存成功")
        if not flag:
            raise AssertionError("保存编辑图片时没有弹出“保存成功”提示")
        # 返回单聊会话页面
        pic.click_cancle()
        cppp = ChatPicPreviewPage()
        cppp.click_back()
        cpg = ChatPicPage()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0010(self):
        """单聊会话页面，取消编辑图片"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击取消按钮
        pic.click_cancle()
        # 返回单聊会话页面
        cppp = ChatPicPreviewPage()
        cppp.click_back()
        cpg = ChatPicPage()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0011(self):
        """单聊会话页面，取消编辑图片，点击发送按钮"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击取消按钮
        pic.click_cancle()
        # 4.点击发送按钮
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0012(self):
        """单聊会话页面，发送相册内的图片 """
        # 1.在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，直接点击当前选中的图片，放大展示当前图片
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        preview_info = cppp.get_pic_preview_info()
        self.assertIsNotNone(re.match(r'预览\(\d+/\d+\)', preview_info))
        cppp.click_back()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0013(self):
        """单聊会话页面，预览已选中的图片，隐藏编辑按钮 """
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2、选择2张照片后，点击左下角的预览按钮
        cpg.select_pic(n=2)
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_edit()
        flag = cppp.is_toast_exist("仅支持勾选单张图片时进行编辑")
        if not flag:
            raise AssertionError("勾选多张图片时编辑按钮没有隐藏")
        cppp.click_back()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0014(self):
        """单聊会话页面，勾选9张相册内图片发送"""
        # 1.在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择9张图片，点击发送
        cpg.select_pic(n=9)
        cpg.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0015(self):
        """单聊会话页面，勾选超9张相册内图片发送"""
        # 1.在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.选择超9张图片
        cpp.select_pic(n=10)
        flag = cpp.is_toast_exist("最多只能选择9张照片")
        if not flag:
            raise AssertionError("选择超过9张图片时无‘最多只能选择9张照片’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0016(self):
        """单聊会话页面，同时发送相册中的图片和视屏"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前页面选择图片和视频
        cpp.select_pic()
        cpp.select_video()
        flag = cpp.is_toast_exist("不能同时选择照片和视频")
        if not flag:
            raise AssertionError("同时选择照片和视频时无‘不能同时选择照片和视频’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0017(self):
        """单聊会话页面，使用拍照功能并发送照片"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击“√”
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.send_photo()
        chat.wait_for_page_load()
