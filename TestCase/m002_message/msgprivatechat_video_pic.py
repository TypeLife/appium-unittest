import random
import time
import re
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages import *


class Preconditions(LoginPreconditions):
    """前置条件"""

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
    """
    模块：消息->单聊视频,图片
    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：消息-单聊视频,图片
    """

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
            current_mobile().reset_app()
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

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0018(self):
        """单聊会话页面，使用拍照功能拍照编辑后发送照片"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_doodle()
        pic.do_doodle()
        # 3.点击"发送"
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0019(self):
        """单聊会话页面，使用拍照功能拍照之后编辑并保存"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_text_edit_btn()
        pic.input_pic_text(text="VideoPic_0019")
        # 点击完成
        pic.click_save()
        # 3.点击"保存"
        pic.click_save()
        # 4.点击"发送"
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0020(self):
        """单聊会话页面，使用拍照功能拍照编辑图片，再取消编辑并发送"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_doodle()
        pic.do_doodle()
        # 3.点击"取消"
        pic.click_cancle()
        # 4.点击“发送”
        cpp.send_photo()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0021(self):
        """单聊会话页面，打开拍照，立刻返回会话窗口"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        # 2、打开照相机，点击“∨”
        cpp.send_photo()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0022(self):
        """单聊会话页面，打开拍照，拍照之后返回会话窗口"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        # 2、打开照相机，点击“返回图标”
        cpp.click_back()
        cpp.take_photo_back()
        chat.wait_for_page_load()

    @staticmethod
    def public_send_pic():
        """在聊天会话页面发送一张图片"""
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 选择一张照片发送
        cpp.select_pic()
        cpp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0026(self):
        """单聊会话页面，转发自己发送的图片给本地联系人"""
        self.public_send_pic()
        # 1、在当前聊天会话页面，长按自己发送的图片
        chat = SingleChatPage()
        chat.press_pic()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意本地联系人
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        if names:
            slcp.select_one_member_by_name(names[0])
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0027(self):
        """单聊会话页面，转发自己发送的图片给和通讯录联系人"""
        self.public_send_pic()
        # 1、在当前聊天会话页面，长按自己发送的图片
        chat = SingleChatPage()
        chat.press_pic()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意和通讯录联系人
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            shcp.select_one_team_by_name(teams[0])
            detail_page = SelectHeContactsDetailPage()
            detail_page.wait_for_page_load()
            names = detail_page.get_contacts_names()
            if not names:
                print("WARN: Please add m005_contacts in %s." % teams[0])
            for name in names:
                detail_page.select_one_linkman(name)
                flag = detail_page.is_toast_exist("该联系人不可选", timeout=3)
                if not flag:
                    break
            # 3、点击确定
            detail_page.click_sure_forward()
            flag2 = detail_page.is_toast_exist("已转发")
            self.assertTrue(flag2)
        else:
            print("WARN: Please create a team and add m005_contacts.")
            shcp.click_back()
            scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0028(self):
        """单聊会话页面，转发自己发送的图片给陌生人"""
        self.public_send_pic()
        # 1、在当前聊天会话页面，长按自己发送的图片
        chat = SingleChatPage()
        chat.press_pic()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意陌生人
        scp = SelectContactsPage()
        times = 500
        while times > 0:
            tel = "147752" + str(random.randint(10000, 99999))
            scp.search(tel)
            # 构造陌生号码发送
            if scp.is_present_unknown_member():
                scp.click_unknown_member()
                scp.click_sure_forward()
                chat.wait_for_page_load()
                break
            times = times - 1

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0030(self):
        """单聊会话页面，删除自己发送的图片"""
        self.public_send_pic()
        # 1、在当前聊天会话页面，长按自己发送的图片
        chat = SingleChatPage()
        chat.press_pic()
        # 2、点击 删除
        chat.click_delete()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0032(self):
        """单聊会话页面，收藏自己发送的照片"""
        # 1、在当前聊天会话页面，长按自己发送的图片
        self.public_send_pic()
        chat = SingleChatPage()
        chat.press_pic()
        # 2.收藏该图片
        chat.click_collection()
        flag = chat.is_toast_exist("已收藏")
        if not flag:
            raise AssertionError("收藏图片没有‘已收藏’提示")
        chat.wait_for_page_load()
        # 3.在我模块中的收藏是否可见
        chat.click_back()
        cdp = ContactDetailsPage()
        cdp.click_back_icon()
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_menu("收藏")
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        flag = mcp.have_collection_pic()
        if not flag:
            raise AssertionError("收藏图片后，在我的收藏中不可见")
        # 回到聊天页面
        mcp.click_back()
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()
        # 点击消息进入单聊会话页面
        cdp.click_message_icon()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        chat.wait_for_page_load()

    @staticmethod
    def public_send_video():
        """在聊天会话页面发送一个视频"""
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 选择一个视频发送
        cpp.select_video()
        cpp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0036(self):
        """单聊会话页面，转发自己发送的视频给本地联系人"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意本地联系人
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        if names:
            slcp.select_one_member_by_name(names[0])
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("转发消息无‘已转发’提示")
        else:
            print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0037(self):
        """单聊会话页面，转发自己发送的视频给和通讯录联系人"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意和通讯录联系人
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            shcp.select_one_team_by_name(teams[0])
            detail_page = SelectHeContactsDetailPage()
            detail_page.wait_for_page_load()
            names = detail_page.get_contacts_names()
            if not names:
                print("WARN: Please add m005_contacts in %s." % teams[0])
            for name in names:
                detail_page.select_one_linkman(name)
                flag = detail_page.is_toast_exist("该联系人不可选", timeout=3)
                if not flag:
                    break
            # 3、点击确定
            detail_page.click_sure_forward()
            flag2 = detail_page.is_toast_exist("已转发")
            if not flag2:
                raise AssertionError("转发消息无‘已转发’提示")
        else:
            print("WARN: Please create a team and add m005_contacts.")
            shcp.click_back()
            scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0038(self):
        """单聊会话页面，转发自己发送的视频给陌生人"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意陌生人
        scp = SelectContactsPage()
        times = 500
        while times > 0:
            tel = "147752" + str(random.randint(10000, 99999))
            scp.search(tel)
            # 构造陌生号码发送
            if scp.is_present_unknown_member():
                scp.click_unknown_member()
                scp.click_sure_forward()
                chat.wait_for_page_load()
                break
            times = times - 1

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0040(self):
        """单聊会话页面，删除自己发送的视频"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2、点击 删除
        chat.click_delete()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0042(self):
        """单聊会话页面，收藏自己发送的视频"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2.收藏该视频
        chat.click_collection()
        flag = chat.is_toast_exist("已收藏")
        if not flag:
            raise AssertionError("收藏视频没有‘已收藏’提示")
        chat.wait_for_page_load()
        # 3.在我模块中的收藏是否可见
        chat.click_back()
        cdp = ContactDetailsPage()
        cdp.click_back_icon()
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_menu("收藏")
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        flag = mcp.have_collection_video()
        if not flag:
            raise AssertionError("收藏视频后，在我的收藏中不可见")
        # 回到聊天页面
        mcp.click_back()
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()
        # 点击消息进入单聊会话页面
        cdp.click_message_icon()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0043(self):
        """单聊会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选择一个视屏
        cpp.select_video()
        flag = cpp.send_btn_is_enabled()
        if not flag:
            raise AssertionError("选择视频，发送按钮不可点击")
        times = cpp.get_video_times()
        res = re.match(r'\d+:\d+', times[0])
        if not res:
            raise AssertionError("视频显示时长格式错误，不是‘00:00’类型")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0044(self):
        """在单聊聊天会话页面，发送相册内一个视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选中一个视屏，点击发送
        cpp.select_video()
        cpp.click_send()
        chat.wait_for_page_load()
        # 3、发送成功，会话窗口可见可播放
        chat.play_video()
        chat.wait_for_play_video_page_load()
        chat.close_video()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0045(self):
        """在单聊聊天会话页面，发送相册内多个视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选中多个视屏
        cpp.select_video(n=0)
        cpp.select_video(n=1)
        # toast提示“最多只能选择一个视频”
        flag = cpp.is_toast_exist("最多只能选择1个视频")
        if not flag:
            raise AssertionError("选择多个视频时无‘最多只能选择1个视频’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0046(self):
        """在单聊聊天会话页面，同时发送相册内视频和图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选中一个视频和一个图片
        cpp.select_video()
        cpp.select_pic()
        # toast提示“不能同时选择照片和视频”
        flag = cpp.is_toast_exist("不能同时选择照片和视频", 5)
        if not flag:
            raise AssertionError("选中一个视频和一个图片时无‘不能同时选择照片和视频’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Msg_PrivateChat_VideoPic_0047(self):
        """在单聊聊天会话页面，发送视频时预览视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选中一个视频点击预览
        cpp.select_video()
        cpp.click_preview()
        # 3、可正常预览
        preview = ChatPicPreviewPage()
        preview.wait_for_video_preview_load()
        preview.click_back()
        cpp.click_back()
        chat.wait_for_page_load()
