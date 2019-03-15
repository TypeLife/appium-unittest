import random
import re
import time
import unittest
import uuid
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为agroup+电话号码后4位的群"""
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
        times = 30
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
        try:
            sc.click_select_one_group()
        except:
            raise AssertionError("选择联系人页面在%ss内，没有加载出选项" % (times*2))
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
        slc.wait_for_page_load()
        names = slc.get_contacts_name()
        if not names:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
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
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "agroup" + phone_number[-4:]
        return group_name


class MsgGroupChatTest(TestCase):
    """
    模块：消息->群聊
    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：消息-群聊
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0001(self):
        """在群聊聊天会话页面，发送一段字符数等于“0”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中不输入任何内容，输入框右边展示的按钮是否是语音按钮
        gcp = GroupChatPage()
        # 语音按钮检查
        gcp.page_should_contain_audio_btn()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0004(self):
        """在群聊聊天会话页面，发送一段字符数等于“5000”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数等于5000
        gcp = GroupChatPage()
        info = "哈哈" * 2500
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按，发送此段文本
        gcp.page_should_contain_send_btn()
        gcp.send_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0005(self):
        """在群聊聊天会话页面，发送一段字符数大于“5000”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数等于5000
        gcp = GroupChatPage()
        info = "呵呵" * 2501
        gcp.input_message(info)
        # 2.在输入框中不可以输入一段字符大于5000文本
        gcp.page_should_contain_send_btn()
        info = gcp.get_input_message()
        self.assertEqual(len(info), 5000)
        gcp.send_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
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
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0018(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，选择一个视频后，点击左下角的预览按钮，是否会以预览模式放大展示当前视频
        cpp.select_video()
        cpp.click_preview()
        video_preview = ChatPicPreviewPage()
        video_preview.wait_for_video_preview_load()
        # 3、预览展示的视频页面中，是否存在点击可播放的三角形按钮
        self.assertTrue(video_preview.play_video_btn_is_enabled())
        # 4、预览播放视频中途，点击左上角的返回按钮，是否可以返回到上一级页面
        video_preview.play_video()
        video_preview.close_video()
        cpp.wait_for_page_load()
        cpp.click_back()
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0019(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.在当前相册详情页面，选择2个视频，选择第二个视频时，是否会提示：最多只能选择1个视频的提示
        cpp.select_video(n=0)
        cpp.select_video(n=1)
        flag = cpp.is_toast_exist("最多只能选择1个视频")
        self.assertTrue(flag)
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0020(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，选择一张照片或者视频后，点击左上角的返回按钮，是否可以返回到聊天会话页面
        cpp.select_pic()
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0022(self):
        """在群聊聊天会话页面，拍照发送照片"""
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，轻触拍摄按钮，是否可以拍摄成功一张照片
        cpp = ChatPhotoPage()
        cpp.take_photo()
        # 3、照片拍摄成功后，点击左边的返回按钮，是否可以删除本次拍摄的照片
        cpp.click_back()
        # 4、重新拍摄一张照片后，点击右边的√按钮，是否可以发送这张照片
        cpp.take_photo()
        cpp.send_photo()

    @unittest.skip("无法实现")
    def test_msg_group_chat_0023(self):
        """在群聊聊天会话页面，拍照发送照片"""
        # 无法实现：appium执行按压1s操作服务器响应需要3s，在这3s时间内toast提示已消失，无法捕获提示
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，长按拍摄按钮，是否可以进入到录像模式
        video = ChatPhotoPage()
        video.wait_for_page_load()
        video.record_video(times=1000)
        # 3.在录像模式下，长按录像按钮，1秒钟之后，松开手指，是否会提示：拍摄失败
        flag = video.is_toast_exist("拍摄失败", timeout=5, poll_frequency=0.01)
        self.assertTrue(flag)
        video.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0024(self):
        """在群聊聊天会话页面，拍照发送照片"""
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，长按拍摄按钮，进入到录像模式
        video = ChatPhotoPage()
        video.wait_for_page_load()
        # 3.在录像模式下，长按录像按钮，10秒钟之后，松开手指，是否会展示并且自动播放当前录制的10秒录像
        video.record_video(times=11000)
        video.wait_for_record_video_after_page_load()
        # 4.在录像展示页面，点击左边的返回按钮，是否可以删除本次录像
        video.click_back()
        video.take_photo_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0025(self):
        """在群聊聊天会话页面，拍照发送照片"""
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，长按拍摄按钮，进入到录像模式
        video = ChatPhotoPage()
        video.wait_for_page_load()
        # 3.在录像模式下，长按录像按钮，10秒钟之后，松开手指，是否会展示并且自动播放当前录制的10秒录像
        video.record_video(times=11000)
        video.wait_for_record_video_after_page_load()
        # 4.在录像展示页面，点击右边的√按钮，是否可以发送本次录像
        video.send_video()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0027(self):
        """在群聊聊天会话页面，拍照发送照片/录像"""
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，点击左下角倒三角，是否可以返回到聊天会话页面
        video = ChatPhotoPage()
        video.wait_for_page_load()
        video.take_photo_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0028(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，是否可以选择本地联系人名片，进行发送
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        cpp.select_card()
        cpp.wait_for_card_page_load()
        cpp.send_card()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0029(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，是否可以搜索选择本地联系人名片，进行发送
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        # names = cpp.get_contacts_name()
        names = cpp.get_first_page_contacts_name()
        if "和通讯录" in names:
            names.remove("和通讯录")
        if "和飞信电话" in names:
            names.remove("和飞信电话")
        # 随机选择一个联系人，进行搜索发送
        cpp.search(random.choice(names))
        cpp.select_card()
        cpp.wait_for_card_page_load()
        cpp.send_card()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0030(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，可进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，不可以搜索选择陌生联系人名片，进行发送
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        # names = cpp.get_contacts_name()
        names = cpp.get_first_page_contacts_name()
        # 构造陌生联系人名
        name = ""
        while True:
            info = "在名片详情页面，不可以搜索选择陌生联系人名片，进行发送"
            name = random.choices(info, k=3)
            if name not in names:
                break
        cpp.search(name)
        flag = cpp.select_card()
        self.assertFalse(flag)
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0033(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，点击右侧的索引字母，索引字母定位搜索是否正常
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        # 获取所有右侧索引字母，随机选择一个点击
        letters = cpp.get_letters_index()
        letter = random.choice(letters)
        cpp.click_letter_index(letter)
        left_lets = cpp.get_left_letters()
        if letter not in left_lets:
            raise AssertionError("在名片详情页面，点击右侧的索引字母，索引字母定位搜索异常")
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0034(self):
        """在群聊聊天会话页面，发送GIF图片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的GIF图标，进入到GIF图片展示页面
        gcp = GroupChatPage()
        gcp.click_gif()
        # 2、在GIF图片展示页面，直接点击上方展示的GIF图片，能否可以进行发送
        gif = ChatGIFPage()
        gif.wait_for_page_load()
        gif.send_gif()
        # 3.在GIF图片展示页面，多次点击上方展示的GIF图片，发送出去的GIF图片是否会展示多张
        gif.send_gif()
        gif.send_gif()
        # 4、点击输入框左上角的X按钮是否可以关闭GIF图片的展示
        gif.close_gif()
        gcp.page_should_not_contain_text("趣图搜搜")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0035(self):
        """在群聊聊天会话页面，发送GIF图片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的GIF图标，进入到GIF图片展示页面
        gcp = GroupChatPage()
        gcp.click_gif()
        gif = ChatGIFPage()
        gif.wait_for_page_load()
        # 2、在输入框中输入英文、中文、字符、数字、表情，是否可以搜索出对应的GIF图片
        # 3、在输入框中输入的搜索条件，搜索不出对应的GIF图片时，是否会提示：无搜索结果,换个热词试试
        infos = ["appium", "哈哈", "a", "123456", "w(ﾟДﾟ)w"]
        try:
            for info in infos:
                gif.input_message(info)
                toast_flag = gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4)
                gif_flag = gif.is_gif_exist()
                self.assertTrue(toast_flag or gif_flag)
        finally:
            gif.close_gif()
            gif.input_message("")
            gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0036(self):
        """在群聊聊天会话页面，发送GIF图片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的GIF图标，进入到GIF图片展示页面
        gcp = GroupChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gcp.click_gif()
        gif.wait_for_page_load()
        # 2、在GIF图片展示页面，点击输入框右边的语音，是否可以切换到语音模式页面
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if gcp.is_text_present("请选择您偏好的语音发送模式"):
            audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0037(self):
        """在群聊聊天会话页面，点击输入框右上角的+号，展示隐藏图标按钮"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，是否会展示隐藏功能图标
        gcp = GroupChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        if not gcp.is_open_more():
            gcp.click_more()
        time.sleep(1)
        gcp.page_should_contain_text("文件")
        gcp.page_should_contain_text("群短信")
        gcp.page_should_contain_text("位置")
        gcp.page_should_contain_text("红包")
        gcp.click_more()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0038(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        files = ['.txt', '.pdf', '.docx', '.jpg', '.xlsx', '.BPG', '.mp4', '.avi']
        for file_type in files:
            # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
            gcp = GroupChatPage()
            if not gcp.is_open_more():
                gcp.click_more()
            # 2.点击展示的隐藏功能图标，文件图标，进入到文件选择页面
            more_page = ChatMorePage()
            more_page.click_file()
            # 3、点击本地文件，进入到本地文件中，选择.txt,.pdf,.docx,.xlsx,.jpg,.BPG,.MP4,.AVI等格式的文件，
            # 选择完成后，右下角的发送按钮是否变成高亮展示
            csf = ChatSelectFilePage()
            csf.wait_for_page_load()
            csf.click_local_file()
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
                self.assertTrue(local_file.send_btn_is_enabled())
                # 4.选择文件后，左下角是否会展示已选择文件的大小
                file_size = local_file.get_file_size()
                select_file_size = local_file.get_selected_file_size()
                self.assertIn(file_size, select_file_size)
                # 5.右下角的发送按钮高亮展示后，点击发送按钮，是否可以进行发送
                local_file.click_send()
            else:
                local_file.click_back()
                local_file.click_back()
                csf.click_back()
                gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0039(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，文件图标，进入到文件选择页面
        more_page = ChatMorePage()
        more_page.click_file()
        # 3.点击视频选择项，进入到本地视频详情展示页面。当前页面的发送按钮，是否默认置灰展示
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        local_file = ChatSelectLocalFilePage()
        self.assertFalse(local_file.send_btn_is_enabled())
        # 4.选择一个视频之后，左下角是否会展示当前选择视频的大小，右下角的发送按钮变成高亮展示
        el = local_file.select_file2("视频")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            gcp.wait_for_page_load()
            raise AssertionError("There is no video")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0040(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，文件图标，进入到文件选择页面
        more_page = ChatMorePage()
        more_page.click_file()
        # 3.点击照片选择项，进入到本地照片详情展示页面。当前页面的发送按钮，是否默认置灰展示
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        local_file = ChatSelectLocalFilePage()
        self.assertFalse(local_file.send_btn_is_enabled())
        # 4、选择一张照片之后，左下角是否会展示当前选择照片的大小，右下角的发送按钮变成高亮展示
        el = local_file.select_file2("照片")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            gcp.wait_for_page_load()
            raise AssertionError("There is no picture")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0041(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，文件图标，进入到文件选择页面
        more_page = ChatMorePage()
        more_page.click_file()
        # 3.点击音乐选择项，进入到本地音乐文件详情展示页面。当前页面的发送按钮，是否默认置灰展示
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        local_file = ChatSelectLocalFilePage()
        self.assertFalse(local_file.send_btn_is_enabled())
        # 4.选择一个音乐文件之后，左下角是否会展示当前选择音乐文件的大小，右下角的发送按钮变成高亮展示
        el = local_file.select_file2("音乐")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            gcp.wait_for_page_load()
            raise AssertionError("There is no music")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG')
    def test_msg_group_chat_0043(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，位置功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，位置功能图标，进入到位置详情展示页面
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 3.在当前页面底部展示的地标选择项中，是否会默认选中第一项。
        self.assertTrue(location_page.is_selected_first_item())
        # 4.位置底部，地标选择项是否可以手动切换选择项
        location_page.select_other_item()
        # 5.选择完成后，点击右上角的发送按钮，是否可以发送
        addr = location_page.get_location_info()
        location_page.click_send()
        gcp.wait_for_page_load()
        # gcp.wait_until(condition=lambda d: gcp.is_text_present(addr))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG')
    def test_msg_group_chat_0044(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，位置功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，位置功能图标，进入到位置详情展示页面
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 3.在当前页面底部展示的地标选择项中，是否会默认选中第一项。
        self.assertTrue(location_page.is_selected_first_item())
        # 4、直接点击当前页面的右上角发送按钮，是否可以发送默认选择项位置
        addr = location_page.get_location_info()
        location_page.click_send()
        gcp.wait_for_page_load()
        # gcp.page_should_contain_text(addr)

    @staticmethod
    def setUp_test_msg_group_chat_0420():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0420(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，位置功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        gcp.click_more()
        # 2.点击展示的隐藏功能图标，位置功能图标，是否会弹出权限允许申请弹窗
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_permission_message_load()
        location_page.wait_for_page_load()
        location_page.click_back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_group_chat_0470():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0470(self):
        """在群聊聊天会话页面，点击输入框右边的语音按钮"""
        # 1.在当前聊天会话页面，点击输入框右边的语音按钮，在未获取录音权限时，是否会弹出权限申请允许弹窗
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

    @staticmethod
    def setUp_test_msg_group_chat_0480():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0480(self):
        """首次使用语音功能"""
        # 1、点击输入框右边的语音按钮，跳转到的页面是否是语音模式设置页面
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

    @staticmethod
    def setUp_test_msg_group_chat_0520():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0520(self):
        """在群聊聊天会话页面，点击输入框右边的语音按钮"""
        # 1.在当前聊天会话页面，点击输入框右边的语音按钮，进入到语音录制页面
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        # 2.首次使用语音录制功能时，点击语音按钮是否会跳转到，语音模式选择页面
        audio = ChatAudioPage()
        flag = audio.wait_for_audio_type_select_page_load()
        self.assertTrue(flag)
        # 3.在语音模式选择页面，是否会默认展示已选择：同时发送语音+文字（语音识别）选择项
        info = audio.get_selected_item()
        self.assertIn("同时发送语音+文字(语音识别)", info)
        # 4.在语音模式选择页面，是否可以手动更改已选择的模式
        audio.select_other_audio_item()
        # 5.更改模式后，点击右下角的确定按钮，是否可以跳转到语音录制页面
        audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_group_chat_0530():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0530(self):
        """在群聊聊天会话页面，点击输入框右边的语音按钮"""
        # 1.在当前聊天会话页面，点击输入框右边的语音按钮，进入到语音录制页面
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        # 2.首次使用语音录制功能时，点击语音按钮会跳转到，语音模式选择页面
        audio = ChatAudioPage()
        flag = audio.wait_for_audio_type_select_page_load()
        self.assertTrue(flag)
        # 3.在语音模式选择页面，点击取消是否可以返回到聊天会话页面
        audio.click_cancel()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0058(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员展示的右边“>”三角形符号，是否可以展示群成员列表
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.click_group_member_show()
        group_member = GroupChatSetSeeMembersPage()
        group_member.wait_for_page_load()
        # 2.在展示的群成员列表上方是否会展示，未进群提示
        flag = group_member.is_others_not_in_group()
        if flag:
            # 3.点击未进群提示，是否可以进入到未进群成员展示列表
            group_member.click_invite_prompt()
            group_member.wait_for_invite_page_load()
            group_member.invite_back()
            group_set.click_group_member_show()
            group_member.wait_for_page_load()
        # 4.点击群成员列表中的成员，是否可以跳转到个人profile页
        group_member.click_group_member()
        if not group_member.is_toast_exist("该联系人不可选择", 3):
            group_member.wait_for_profile_page_load()
            group_member.profile_back()
            group_member.wait_for_page_load()
        # 5.在群成员列表上方的搜索框，通过英文（大、小写）、中文、等搜索条件，搜索出符合条件的结果
        names = group_member.get_all_group_member_names()
        group_member.search(names[0])
        results = group_member.get_all_group_member_names()
        self.assertIn(names[0], results)
        name1 = str(uuid.uuid1()) + "Name"
        group_member.search(name1)
        results1 = group_member.get_all_group_member_names()
        self.assertEqual(0, len(results1))
        name2 = str(uuid.uuid1()) + "中文"
        group_member.search(name2)
        results2 = group_member.get_all_group_member_names()
        self.assertEqual(0, len(results2))
        group_member.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0060(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，是否会跳转到联系人选择器页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        # 2.在联系人选择器页面，是否可以选择本地联系人
        # 3、在联系人选择器页面，是否可以选择和通讯录联系人
        # 4、在联系人选择器页面，未选择任何联系人时，右上角展示的确定按钮是否是置灰展示
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        # 选择与否获取的属性都是可点击
        # flag = contacts_page.sure_btn_is_enabled()
        # self.assertFalse(flag)
        # 5、选择联系人后，右上角的确定按钮上是否会展示已选择人数加剩余可选择人数，例：确定（2/462）
        names = contacts_page.get_contacts_name()
        for name in names:
            contacts_page.select_one_member_by_name(name)
        info = contacts_page.get_sure_btn_text()
        self.assertIsNotNone(re.match(r'确定\(\d+/\d+\)', info))
        # 返回聊天页面
        contacts_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0061(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，是否会跳转到联系人选择器页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        # 2.在联系人选择器页面，单击是否可以选择联系人
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        names = contacts_page.get_contacts_name()
        contacts_page.select_one_member_by_name(names[0])
        flag = contacts_page.contacts_is_selected(names[0])
        if not flag:
            raise AssertionError("在联系人选择器页面，单击不可以选择联系人")
        # 3.在联系人选择器页面，点击是否可以取消联系人的选择状态
        contacts_page.select_one_member_by_name(names[0])
        time.sleep(1)
        flag2 = contacts_page.contacts_is_selected(names[0])
        if flag2:
            raise AssertionError("在联系人选择器页面，单击不可以取消联系人的选择状态")
        contacts_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0062(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，跳转到联系人选择器页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        # 2.在联系人选择器页面，选择多个联系人之后，点击左上角的返回按钮，
        # 是否可以返回到聊天会话页面并且清除已选择的联系人选择状态
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        names = contacts_page.get_contacts_name()
        for name in names:
            contacts_page.select_one_member_by_name(name)
        contacts_page.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0063(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，跳转到联系人选择器页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        # 2.在联系人选择页面，把剩余可选择人数全部勾选上，点击右上角的确定按钮，是否可以发送邀请
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        names = contacts_page.get_contacts_name()
        contacts_page.swipe_to_top()
        for name in names:
            contacts_page.search_and_select_one_member_by_name(name)
        contacts_page.click_sure()
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("发出群邀请")

    def msg_group_chat_0064_pre_condition(self):
        """test_msg_group_chat_0064执行前置条件"""
        # 从通讯录获取人数，如果人数不足510(一个群可以添加500人)则先创建联系人
        gcp = GroupChatPage()
        gcp.click_back()
        if gcp.is_text_present("选择一个群"):
            sogp = SelectOneGroupPage()
            sogp.click_back()
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_contacts()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        names = contacts_page.get_all_contacts_name()
        if "和通讯录" in names:
            names.remove("和通讯录")
        if "和飞信电话" in names:
            names.remove("和飞信电话")
        totals = len(names)
        if totals < 510:
            # 人数不足创建联系人
            nums = 510 - totals
            info = "abcdefghigklmnopqrstuvwxyz"
            bname = "z" + random.choice(info) + random.choice(info)
            bnumber = "1477" + str(time.time())[-4:]
            for n in range(1, nums + 1):
                name = bname + "%05d" % n
                names.append(name)
                number = bnumber + "%03d" % n
                contacts_page.click_add()
                ccp = CreateContactPage()
                ccp.wait_for_page_load()
                ccp.create_contact(name, number)
                cdp = ContactDetailsPage()
                cdp.wait_for_page_load()
                cdp.click_back_icon()
        # 人数足够回到群聊设置页面
        mess.open_message_page()
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        sogp = SelectOneGroupPage()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()
        gcp.click_setting()
        return names

    @tags('ALL', 'SMOKE', 'group_chat0064')
    def test_msg_group_chat_0064(self):
        """在群聊聊天设置页面，添加群成员"""
        names = self.msg_group_chat_0064_pre_condition()
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，跳转到联系人选择器页面
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        # 2.在联系人选择页面，勾选人数超出剩余可勾选人数，是否会提示
        for name in names:
            contacts_page.search_and_select_one_member_by_name(name)
        selected_nums, threshold_nums = contacts_page.get_selected_and_threshold_nums()
        if selected_nums > threshold_nums:
            name_list = contacts_page.get_contacts_name()
            if contacts_page.contacts_is_selected(name_list[0]):
                contacts_page.select_one_member_by_name(name_list[0])
            contacts_page.select_one_member_by_name(name_list[0])
            flag = contacts_page.is_toast_exist("最多只能选择" + str(threshold_nums) + "人", timeout=6)
            if not flag:
                raise AssertionError("勾选人数超出剩余可勾选人数无‘最多只能选择" + str(threshold_nums) + "人' 提示")
        else:
            raise AssertionError("没有选择超出剩余可勾选人数，请确定")
        contacts_page.click_sure()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'only_group_owner')
    def test_msg_group_chat_0065(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否会跳转到群成员移除列表展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums != 1:
            print("当前群聊中只能有群主,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_del_member()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'group_chat_6_members')
    def test_msg_group_chat_0066(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否可以跳转到群成员移除列表展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums < 3:
            print("当前群聊成员需要大于2,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        # 2.在群成员展示列表中，未选择需要进行移除的成员时，右上角的确定按钮是否默认置灰展示
        group_set.click_del_member()
        contacts = SelectLocalContactsPage()
        contacts.wait_for_page_load()
        # 3.在群成员展示列表中，点击勾选一个成员，右上角的确定是否会高亮展示并且展示已选择的移除数量
        names = contacts.get_contacts_name()
        contacts.select_one_member_by_name(names[0])
        info = contacts.get_sure_btn_text()
        self.assertIsNotNone(re.match(r'确定\(1/\d+\)', info))
        # 4.点击右上角高亮展示的确定按钮，是否可以移除当前成员
        contacts.click_sure()
        contacts.click_sure_del()
        group_set.wait_for_page_load()
        group_set.click_back()
        # 5.被移除的成员，是否会收到一条系统通知，你已被群主请出群聊
        # 6.在群聊聊天会话页面，是否会展示一条，XX被移除群聊的信息
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("移出群")

    @tags('ALL', 'SMOKE', 'group_chat_6_members')
    def test_msg_group_chat_0067(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否可以跳转到群成员移除列表展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums < 4:
            print("当前群聊成员需要大于3,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_del_member()
        # 2.在群成员展示列表中，未选择需要进行移除的成员时，右上角的确定按钮是否默认置灰展示
        contacts = SelectLocalContactsPage()
        contacts.wait_for_page_load()
        # 3.在群成员展示列表中，点击勾选2个成员，右上角的确定是否会高亮展示并且展示已选择的移除数量
        names = contacts.get_contacts_name()
        contacts.select_one_member_by_name(names[0])
        contacts.select_one_member_by_name(names[1])
        info = contacts.get_sure_btn_text()
        self.assertIsNotNone(re.match(r'确定\(2/\d+\)', info))
        # 4.点击右上角高亮展示的确定按钮，是否可以移除当前成员
        contacts.click_sure()
        contacts.click_sure_del()
        group_set.wait_for_page_load()
        group_set.click_back()
        # 5.被移除的成员，是否会收到一条系统通知，你已被群主请出群聊
        # 6.在群聊聊天会话页面，是否会展示一条，XX被移除群聊的信息
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("移出群")

    @tags('ALL', 'SMOKE', 'group_chat_6_members')
    def test_msg_group_chat_0068(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否可以跳转到群成员移除列表展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums != 3:
            print("当前群聊成员必须为3人,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_del_member()
        # 2.在群成员展示列表中，未选择需要进行移除的成员时，右上角的确定按钮是否默认置灰展示
        contacts = SelectLocalContactsPage()
        contacts.wait_for_page_load()
        # 3.在群成员展示列表中，点击勾选2个成员，右上角的确定是否会高亮展示并且展示已选择的移除数量
        names = contacts.get_contacts_name()
        contacts.select_one_member_by_name(names[0])
        contacts.select_one_member_by_name(names[1])
        info = contacts.get_sure_btn_text()
        self.assertIsNotNone(re.match(r'确定\(2/\d+\)', info))
        # 4.点击右上角高亮展示的确定按钮，是否可以移除当前成员
        contacts.click_sure()
        contacts.click_sure_del()
        # 5.被移除的成员，是否会收到一条系统通知，你已被群主请出群聊同时提示该群已解散
        # 6.在群聊聊天会话页面，是否会展示一条，XX被移除群聊的信息同时展示该群已解散
        flag = contacts.is_toast_exist("该群已解散")
        self.assertTrue(flag)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0069(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，是否会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，点击左上角的“修改群聊名称”返回按钮，是否可以返回到聊天设置页面
        group_name.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0070(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，不修改直接点击右上角的保存按钮，是否可以进行保存
        group_name.click_save()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0071(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2、在群聊名称修改页面，录入29个英文（大小写）字母字符，点击右上角的保存按钮是否可以保存
        old_name = Preconditions.get_group_chat_name()
        new_name = "PreconditionsGetGroupChatName"
        group_name.input_group_name(new_name)
        group_name.click_save()
        flag = group_name.is_toast_exist("修改成功")
        self.assertTrue(flag)
        group_set.wait_for_page_load()
        # 改回之前的名字
        group_set.click_modify_group_name()
        group_name.input_group_name(old_name)
        group_name.click_save()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0072(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，不录入任何字符，右上角的保存按钮是否是置灰展示，不可点击
        group_name.input_group_name("")
        flag = group_name.save_btn_is_enabled()
        self.assertFalse(flag)
        # 回到群聊页面
        group_name.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0073(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，点击群名称右边的“X”符号，是否可以一次清除输入框中的群聊名称
        group_name.click_delete_group_name()
        # 3.群聊名称被清除后，右上角的保存按钮，是否会置灰展示不可点击
        flag = group_name.save_btn_is_enabled()
        self.assertFalse(flag)
        # 回到群聊页面
        group_name.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0074(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，录入30个英文（大小写）字母字符，点击右上角的保存按钮，是否可以保存
        old_name = Preconditions.get_group_chat_name()
        new_name = "PreconditionsGetGroupChatNameX"
        group_name.input_group_name(new_name)
        group_name.click_save()
        flag = group_name.is_toast_exist("修改成功")
        self.assertTrue(flag)
        group_set.wait_for_page_load()
        # 改回之前的名字
        group_set.click_modify_group_name()
        group_name.input_group_name(old_name)
        group_name.click_save()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0075(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群名片修改页面，录入31个英文字符，不可以录入成功（只支持30个字符）
        new_name = "PreconditionsGetGroupChatNameXx"
        try:
            group_name.input_group_name(new_name)
        except:
            print("ok")
        else:
            name = group_name.get_input_group_name()
            if len(name) != 30:
                raise AssertionError("修改群名片录入31个英文字符，代码可以实现，请确认是否可以手动录入31个英文字符！")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0076(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，录入10个汉字，点击右上角的保存按钮，是否可以保存
        old_name = Preconditions.get_group_chat_name()
        new_name = "汉字群聊名称修改页面"
        group_name.input_group_name(new_name)
        group_name.click_save()
        flag = group_name.is_toast_exist("修改成功")
        self.assertTrue(flag)
        group_set.wait_for_page_load()
        # 改回之前的名字
        group_set.click_modify_group_name()
        group_name.input_group_name(old_name)
        group_name.click_save()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0077(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群名片修改页面，不可以录入11个汉字（只能录入10个汉字）
        new_name = "汉字群聊名称修改页面字"
        try:
            group_name.input_group_name(new_name)
        except:
            print("ok")
        else:
            name = group_name.get_input_group_name()
            if len(name) != 10:
                raise AssertionError("修改群名片录入11个汉字，代码可以实现，请确认是否可以手动录入11个汉字！")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0078(self):
        """在聊天设置页面，分享群二维码"""
        # 1、在聊天设置页面，点击群二维码，是否会跳转到群聊二维码展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_QRCode()
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 2、在当前群聊展示页面，点击左下角的分享按钮，是否会跳转到联系人选择器页面
        code_page.click_qecode_share_btn()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 3、在联系人选择器页面，选择一个群聊或者联系人，是否会弹出确认分享弹窗
        scp.select_local_contacts()
        local_contacts = SelectLocalContactsPage()
        names = local_contacts.get_contacts_name()
        local_contacts.select_one_member_by_name(names[0])
        # 4、点击确定是否可以分享成功
        local_contacts.click_sure_share()
        flag = code_page.is_toast_exist("已转发")
        self.assertTrue(flag)
        code_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0079(self):
        """在聊天设置页面，分享群二维码"""
        # 1、在聊天设置页面，点击群二维码，是否会跳转到群聊二维码展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_QRCode()
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 2、在当前群聊展示页面，点击右下角的下载按钮，是否会提示下载成功
        code_page.click_qecode_save_btn()
        flag = code_page.is_toast_exist("已保存")
        self.assertTrue(flag)
        # 3、点击左上角的“<”返回按钮，是否可以返回到聊天设置页面
        code_page.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0080(self):
        """在聊天设置页面，修改我在本群的昵称"""
        # 1、在聊天设置页面，点击我在本群的昵称，是否会跳转到修改群名片页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_my_card()
        mycard = GroupChatSetModifyMyCardPage()
        mycard.wait_for_page_load()
        # 2、在修改群名片页面，输入新的名称，点击右上角的保存按钮，是否可以保存
        name = "w" + str(int(time.time()))
        mycard.input_my_name(name)
        mycard.click_save()
        flag = group_set.is_toast_exist("修改成功", timeout=8)
        if not flag:
            raise AssertionError("修改群名片后，无‘修改成功’提示")
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0081(self):
        """在聊天设置页面，修改我在本群的昵称"""
        # 1.在聊天设置页面，点击我在本群的昵称，会跳转到修改群名片页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_my_card()
        mycard = GroupChatSetModifyMyCardPage()
        mycard.wait_for_page_load()
        # 2.在修改群名片页面，点击输入框右边的“x”按钮，是否可以一次清除已存在的昵称
        mycard.click_delete_my_name()
        mycard.page_should_contain_text("设置你在群内显示的昵称")
        # 3.输入框中不存在内容后，右上角的保存按钮是否会置灰展示
        flag = mycard.save_btn_is_enabled()
        self.assertFalse(flag)
        # 4.输入框录入内容后，右上角的保存按钮，是否会高亮展示
        name = "w" + str(int(time.time()))
        mycard.input_my_name(name)
        flag = mycard.save_btn_is_enabled()
        self.assertTrue(flag)
        # 5.点击高亮展示的保存按钮，是否可以保存
        mycard.click_save()
        flag = group_set.is_toast_exist("修改成功")
        if not flag:
            raise AssertionError("修改群名片后，无‘修改成功’提示")
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0820(self):
        """在聊天设置—群管理页面，转让群主或者解散群"""
        # 1.点击群管理，是否可以跳转到群管理页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_group_manage()
        # 2.点击解散群，是否会弹窗提示解散群聊确认操作
        manage_page = GroupChatSetManagerPage()
        manage_page.click_group_disband()
        manage_page.click_confirm()
        # 3.点击确定，是否可以解散群聊
        flag = manage_page.is_toast_exist("该群已解散")
        self.assertTrue(flag)

    @tags('ALL', 'SMOKE', 'only_group_owner')
    def test_msg_group_chat_0083(self):
        """在聊天设置—群管理页面，转让群主或者解散群"""
        # 1.点击群管理，跳转到群管理页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums != 1:
            print("当前群不能有群成员,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_group_manage()
        # 2.点击群主管理权转让，是否会弹出提示：暂无群成员
        manage_page = GroupChatSetManagerPage()
        manage_page.click_group_transfer()
        flag = manage_page.is_toast_exist("暂无群成员")
        self.assertTrue(flag)
        manage_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'transfer_group_owner')
    def test_msg_group_chat_1084(self):
        """在聊天设置—群管理页面，转让群主或者解散群"""
        # 1、点击群管理，跳转到群管理页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums == 1:
            print("当前群只有群主,请添加成员")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_group_manage()
        # 2、点击群主管理权转让，是否会跳转到“新群主选择”页面
        manage_page = GroupChatSetManagerPage()
        manage_page.click_group_transfer()
        # 3、点击选择一个群成员，是否会弹出提示：是否确定XXX为新群主的确认提示
        contacts = SelectLocalContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        contacts.select_one_member_by_name(names[0])
        contacts.page_should_contain_text("确定选择" + names[0] + "为新群主")
        # 4、点击取消，返回到上一级操作
        contacts.click_cancel_transfer()
        # 5、点击确定，群主转让成功同时在群聊天会话页面展示XXX已成为新群主
        contacts.select_one_member_by_name(names[0])
        contacts.page_should_contain_text("确定选择" + names[0] + "为新群主")
        contacts.click_sure_transfer()
        flag = group_set.is_toast_exist("已转让")
        self.assertTrue(flag)
        group_set.click_back()
        gcp.wait_for_page_load()
        gcp.page_should_contain_text(names[0] + " 已成为新群主")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0085(self):
        """在聊天设置—设置免打扰"""
        # 1、点击消息免打扰的开关，是否可以打开消息免打扰开关
        gcp = GroupChatPage()
        # 点击前先发送一条消息
        info = "Hello everyone!"
        gcp.input_message(info)
        gcp.send_message()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        if not switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)
        # 2、返回到聊天会话页面，页面上方是否会展示免打扰标志
        group_set.click_back()
        gcp.wait_for_page_load()
        flag = gcp.is_exist_undisturb()
        if not flag:
            raise AssertionError("在聊天会话页面，页面上方没有展示免打扰标志")
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        scp = SelectContactsPage()
        scp.click_back()
        # 3、返回到消息列表，开启免打扰的聊天窗口上是否会展示免打扰标志
        mess = MessagePage()
        mess.wait_for_page_load()
        group_name = Preconditions.get_group_chat_name()
        flag2 = mess.is_exist_undisturb(group_name)
        if not flag2:
            raise AssertionError("在消息列表，开启免打扰的聊天窗口上没有展示免打扰标志")
        # 回到群聊会话页面
        mess.click_add_icon()
        mess.click_group_chat()
        scp.click_select_one_group()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0086(self):
        """在聊天设置—设置免打扰"""
        # 1.点击消息免打扰开关，是否可以关闭免打扰
        gcp = GroupChatPage()
        # 先发送一条消息
        info = "Hello"
        gcp.input_message(info)
        gcp.send_message()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        # 如果开关打开则关闭
        if switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)
        # 2.返回到聊天会话页面，页面上方是否会隐藏免打扰标志
        group_set.click_back()
        flag = gcp.is_exist_undisturb()
        self.assertFalse(flag)
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        scp = SelectContactsPage()
        scp.click_back()
        # 3.返回到消息列表，关闭免打扰的聊天窗口上是否会隐藏免打扰标志
        mess = MessagePage()
        mess.wait_for_page_load()
        group_name = Preconditions.get_group_chat_name()
        flag = mess.is_exist_undisturb(group_name)
        self.assertFalse(flag)
        # 回到群聊会话页面
        mess.click_add_icon()
        mess.click_group_chat()
        scp.click_select_one_group()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0087(self):
        """在聊天设置—设置置顶聊天 """
        # 1.点击置顶聊天的开关，是否可以开启置顶聊天开关
        gcp = GroupChatPage()
        # 先发送一条消息
        info = "hehe"
        gcp.input_message(info)
        gcp.send_message()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        top_switch = group_set.get_chat_set_to_top_switch_status()
        if not top_switch:
            group_set.click_chat_set_to_top_switch()
            time.sleep(1)
        # 2.返回到消息列表，当前打开置顶聊天功能的群聊是否成功置顶
        group_set.click_back()
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        scp = SelectContactsPage()
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 给其他联系人发送一条消息，看群聊是否设置成功置顶
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        contacts.select_people_by_name(names[0])
        contact_detail = ContactDetailsPage()
        contact_detail.click_message_icon()
        chat = GroupChatPage()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        info = "您好"
        chat.input_message(info)
        chat.send_message()
        chat.click_back()
        contact_detail.click_back_icon()
        contacts.open_message_page()
        # 获取群名字
        group_name = Preconditions.get_group_chat_name()
        # 顶部消息群名
        top_name = mess.get_top_news_name()
        # 名字一致，则置顶成功
        self.assertEqual(group_name, top_name)
        # 回到群聊会话页面
        mess.click_add_icon()
        mess.click_group_chat()
        scp.click_select_one_group()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0088(self):
        """在聊天设置—设置置顶聊天 """
        # 1.点击置顶聊天的开关，是否可以关闭置顶聊天开关
        gcp = GroupChatPage()
        # 先发送一条消息
        info = "hehe"
        gcp.input_message(info)
        gcp.send_message()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        top_switch = group_set.get_chat_set_to_top_switch_status()
        if top_switch:
            group_set.click_chat_set_to_top_switch()
            time.sleep(1)
        # 2.返回到消息列表，当前关闭置顶聊天功能的群聊，是否成功取消置顶
        group_set.click_back()
        gcp.click_back()
        sogp = SelectOneGroupPage()
        sogp.click_back()
        scp = SelectContactsPage()
        scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 给其他联系人发送一条消息，看群聊是否成功取消置顶
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        contacts.select_people_by_name(names[0])
        contact_detail = ContactDetailsPage()
        contact_detail.click_message_icon()
        chat = GroupChatPage()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        info = "您好"
        chat.input_message(info)
        chat.send_message()
        chat.click_back()
        contact_detail.click_back_icon()
        contacts.open_message_page()
        # 获取群名字
        group_name = Preconditions.get_group_chat_name()
        # 顶部消息群名
        top_name = mess.get_top_news_name()
        # 名字不一致，则取消置顶成功
        self.assertNotEqual(group_name, top_name)
        # 回到群聊会话页面
        mess.click_add_icon()
        mess.click_group_chat()
        scp.click_select_one_group()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0089(self):
        """在聊天设置—查找聊天内容 """
        # 1.点击查找聊天内容，是否可以跳转到聊天内容搜索展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.scroll_to_bottom()
        group_set.click_find_chat_record()
        search_page = GroupChatSetFindChatContentPage()
        search_page.wait_for_page_load()
        # 2.在页面顶部搜索框中，输入搜索条件，无搜索结果，页面是否会展示文案：“无搜索结果”
        info = str(uuid.uuid1())
        search_page.search(info)
        search_page.page_should_contain_text("无搜索结果")
        # 3.搜索框中存在内容时，右边是否会展示一键清除输入框中内容按钮“X”
        # 4.点击“X”按钮是否可以清除输入框中内容并展示初始化页面
        search_page.click_x_icon()
        search_page.wait_for_page_load()
        search_page.page_should_contain_text("分类索引")
        search_page.page_should_contain_text("图片与视频")
        search_page.page_should_contain_text("文件")
        search_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()
