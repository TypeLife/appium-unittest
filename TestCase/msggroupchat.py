import re
import time
import unittest
import random
import uuid
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
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

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
        times = 10
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(1)
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

    @tags('ALL',)
    def test_msg_group_chat_0037(self):
        """在群聊聊天会话页面，点击输入框右上角的+号，展示隐藏图标按钮"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，是否会展示隐藏功能图标
        gcp = GroupChatPage()
        gcp.click_more()
        gcp.page_should_contain_text("文件")
        gcp.page_should_contain_text("群短信")
        gcp.page_should_contain_text("位置")
        gcp.page_should_contain_text("红包")
        gcp.click_more()

    @tags('ALL',)
    def test_msg_group_chat_0038(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        files = ['txt文件', 'pdf文件', 'docx文件', 'jpg文件', 'xlsx文件', 'BPG文件', 'mp4文件', 'avi文件']
        for file_type in files:
            # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
            gcp = GroupChatPage()
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
                csf.click_back()

    @tags('ALL',)
    def test_msg_group_chat_0039(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
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
        el = local_file.select_file("视频")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            raise AssertionError("There is no video")

    @tags('ALL',)
    def test_msg_group_chat_0040(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
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
        el = local_file.select_file("照片")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            raise AssertionError("There is no picture")

    @tags('ALL',)
    def test_msg_group_chat_0041(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
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
        el = local_file.select_file("音乐")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            raise AssertionError("There is no music")

    @tags('ALL',)
    def test_msg_group_chat_0043(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，位置功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
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
        gcp.page_should_contain_text(addr)

    @tags('ALL',)
    def test_msg_group_chat_0044(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，位置功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
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
        gcp.page_should_contain_text(addr)

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

    @tags('ALL',)
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

    @tags('ALL',)
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
        audio.page_should_contain_text("退出")
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

    @tags('ALL',)
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

    @tags('ALL',)
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

    @tags('ALL', )
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

    @tags('ALL', )
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
        group_member.wait_for_profile_page_load()
        group_member.profile_back()
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

    @tags('ALL', )
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

    @tags('ALL', )
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
        self.assertTrue(flag)
        # 3.在联系人选择器页面，点击是否可以取消联系人的选择状态
        contacts_page.select_one_member_by_name(names[0])
        flag = contacts_page.contacts_is_selected(names[0])
        self.assertFalse(flag)
        contacts_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', )
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

    @tags('ALL', )
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
        names = contacts_page.get_all_contacts_name()
        contacts_page.swipe_to_top()
        for name in names:
            contacts_page.search_and_select_one_member_by_name(name)
        contacts_page.click_sure()
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("发出群邀请")

    @tags('ALL', )
    def test_msg_group_chat_0064(self):
        """在群聊聊天设置页面，添加群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，跳转到联系人选择器页面
        # 2.在联系人选择页面，勾选人数超出剩余可勾选人数，是否会提示

    @tags('ALL', )
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

    @tags('ALL', )
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
        # 4.点击右上角高亮展示的确定按钮，是否可以移除当前成员
        contacts.click_sure()
        contacts.click_sure_del()
        group_set.wait_for_page_load()
        group_set.click_back()
        # 5.被移除的成员，是否会收到一条系统通知，你已被群主请出群聊
        # 6.在群聊聊天会话页面，是否会展示一条，XX被移除群聊的信息
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("移出群")

    @tags('ALL', )
    def test_msg_group_chat_0067(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否可以跳转到群成员移除列表展示页面
        # 2.在群成员展示列表中，未选择需要进行移除的成员时，右上角的确定按钮是否默认置灰展示
        # 3.在群成员展示列表中，点击勾选2个成员，右上角的确定是否会高亮展示并且展示已选择的移除数量
        # 4.点击右上角高亮展示的确定按钮，是否可以移除当前成员
        # 5.被移除的成员，是否会收到一条系统通知，你已被群主请出群聊
        # 7.在群聊聊天会话页面，是否会展示一条，XX被移除群聊的信息

