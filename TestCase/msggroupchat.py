import re
import time
import unittest
import random

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
            # current_mobile().launch_app()
            current_mobile().reset_app()
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

    @tags('ALL',)
    def test_msg_group_chat_0001(self):
        """在群聊聊天会话页面，发送一段字符数等于“0”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中不输入任何内容，输入框右边展示的按钮是否是语音按钮
        gcp = GroupChatPage()
        # 语音按钮检查
        gcp.page_should_contain_audio_btn()

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
    def test_msg_group_chat_0004(self):
        """在群聊聊天会话页面，发送一段字符数等于“5000”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数等于5000
        gcp = GroupChatPage()
        info = "哈哈" * 2500
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按，发送此段文本
        gcp.page_should_contain_send_btn()
        gcp.send_message()

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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
        video_preview.click_back()
        cpp.wait_for_page_load()
        cpp.click_back()

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL',)
    def test_msg_group_chat_0029(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，是否可以搜索选择本地联系人名片，进行发送
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        names = cpp.get_contacts_name()
        # 随机选择一个联系人，进行搜索发送
        cpp.search(random.choice(names))
        cpp.select_card()
        cpp.wait_for_card_page_load()
        cpp.send_card()

    @tags('ALL',)
    def test_msg_group_chat_0030(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，可进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，不可以搜索选择陌生联系人名片，进行发送
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        names = cpp.get_contacts_name()
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

    @tags('ALL',)
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
        self.assertIn(letter, left_lets)
        cpp.click_back()

    @tags('ALL',)
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

    @tags('ALL',)
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
        for info in infos:
            gif.input_message(info)
            toast_flag = gif.is_toast_exist("无搜索结果，换个热词试试", timeout=3)
            gif_flag = gif.is_gif_exist()
            self.assertNotEqual(toast_flag, gif_flag)
        gif.close_gif()

    @tags('ALL',)
    def test_msg_group_chat_0036(self):
        """在群聊聊天会话页面，发送GIF图片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的GIF图标，进入到GIF图片展示页面
        gcp = GroupChatPage()
        gcp.click_gif()
        gif = ChatGIFPage()
        gif.wait_for_page_load()
        # 2、在GIF图片展示页面，点击输入框右边的语音，是否可以切换到语音模式页面
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if gcp.is_text_present("请选择您偏好的语音发送模式"):
            audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()

