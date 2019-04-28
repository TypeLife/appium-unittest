import random
import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver
from pages.components import BaseChatPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages import *


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def enter_preset_file_catalog():
        """进入预置文件目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_more()
        # 点击本地文件
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csfp.click_local_file()
        # 进入预置文件目录
        local_file.click_preset_file_dir()

    @staticmethod
    def send_file_by_type(file_type):
        """发送指定类型文件"""

        # 进入预置文件目录
        Preconditions.enter_preset_file_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送指定类型文件
        local_file.select_file(file_type)
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

    @staticmethod
    def send_large_file():
        """发送大型文件"""

        # 进入预置文件目录
        Preconditions.enter_preset_file_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            local_file.click_preset_file_dir()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def enter_local_picture_catalog():
        """进入本地照片目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地照片
        csfp.click_pic()

    @staticmethod
    def send_local_picture():
        """发送本地图片"""

        # 进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送本地照片
        local_file.click_picture()
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

    @staticmethod
    def send_large_picture_file():
        """发送大型图片文件"""

        # 进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型图片文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_pic()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def enter_local_video_catalog():
        """进入本地视频目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地视频
        csfp.click_video()

    @staticmethod
    def send_local_video():
        """发送本地视频"""

        # 进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送本地视频
        local_file.click_video()
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

    @staticmethod
    def send_large_video_file():
        """发送大型视频文件"""

        # 进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型视频文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_video()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def enter_local_music_catalog():
        """进入本地音乐目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地音乐
        csfp.click_music()

    @staticmethod
    def send_local_music():
        """发送本地音乐"""

        # 进入本地音乐目录
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送本地音乐
        local_file.click_music()
        local_file.click_send_button()
        time.sleep(2)
        if local_file.is_exist_continue_send():
            local_file.click_continue_send()

    @staticmethod
    def send_large_music_file():
        """发送大型音乐文件"""

        # 进入本地音乐目录
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型音乐文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_music()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def make_no_retransmission_button(name):
        """确保当前单聊会话页面没有重发按钮影响验证结果"""

        scp = SingleChatPage()
        if scp.is_exist_msg_send_failed_button():
            scp.click_back()
            mp = MessagePage()
            mp.wait_for_page_load()
            mp.delete_message_record_by_name(name)
            Preconditions.enter_single_chat_page(name)

    @staticmethod
    def make_no_message_send_failed_status(name):
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()
        Preconditions.enter_single_chat_page(name)


class MsgPrivateChatFileLocationTest(TestCase):
    """
    模块：消息->单聊文件,位置
    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：消息-单聊文件,位置
    """

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        current_mobile().launch_app()

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
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @staticmethod
    def public_send_file(file_type):
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
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

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0001(self):
        """单聊会话页面，不勾选本地文件内文件点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、不选择文件，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0002(self):
        """ 单聊会话页面，勾选本地文件内任意文件点击发送按钮"""
        self.public_send_file('.txt')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0003(self):
        """单聊会话页面，不勾选本地视频文件内视频点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击视频
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 3、不选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0004(self):
        """单聊会话页面，勾选本地视频文件内任意视频点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击视频
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 3、选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出视频，则循环6次
        for i in range(6):
            el = local_file.select_file2("视频")
            if el:
                local_file.click_send()
                chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_video()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()
        raise AssertionError("There is no video")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0005(self):
        """单聊会话页面，不勾选本地照片文件内照片点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击照片
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 3、不选择照片，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0006(self):
        """单聊会话页面，勾选本地照片文件内任意照片点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击照片
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 3、选择照片，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出照片，则循环6次
        for i in range(6):
            el = local_file.select_file2("照片")
            if el:
                local_file.click_send()
                chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_pic()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()
        raise AssertionError("There is no pic")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0007(self):
        """单聊会话页面，不勾选本地音乐文件内音乐点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击音乐
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 3、不选择音乐，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0008(self):
        """单聊会话页面，勾选本地音乐文件内任意音乐点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击音乐
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 3、选择音乐，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出音乐，则循环6次
        for i in range(6):
            el = local_file.select_file2("音乐")
            if el:
                local_file.click_send()
                chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_music()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()
        raise AssertionError("There is no music")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0019(self):
        """单聊设置-查找聊天内容-文件页面，长按文件进行删除"""
        self.public_send_file('.xlsx')
        chat = SingleChatPage()
        # 点击设置
        chat.click_setting()
        set_page = SingleChatSetPage()
        # 点击查找聊天内容
        set_page.search_chat_record()
        search = FindChatRecordPage()
        # 点击文件
        search.click_file()
        chat_file = ChatFilePage()
        chat_file.wait_for_page_load()
        chat_file.delete_file(".xlsx")
        # 返回聊天会话页面
        chat_file.click_back()
        search.click_back()
        set_page.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0040(self):
        """单聊天会话页面，长按文件进行删除"""
        # 预置数据，发送文件
        self.public_send_file('.xlsx')
        chat = SingleChatPage()
        # 长按文件删除
        chat.delete_mess(".xlsx")
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0041(self):
        """单聊天会话页面，长按自己发送的文件，十分钟内撤回"""
        # 预置数据，发送文件
        self.public_send_file('.xlsx')
        chat = SingleChatPage()
        # 长按文件撤回消息
        chat.recall_mess(".xlsx")
        try:
            chat.wait_until(
                timeout=3,
                auto_accept_permission_alert=True,
                condition=lambda d: chat.is_text_present("知道了")
            )
        except:
            pass
        if chat.is_text_present("知道了"):
            chat.click_i_know()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'SLOW')
    def test_msg_private_chat_file_location_0042(self):
        """单聊天会话页面，长按自己发送的文件，超过十分钟撤回"""
        self.public_send_file('.xlsx')
        chat = SingleChatPage()
        # 超过十分钟,长按自己发送的文件撤回，没有撤回菜单按钮
        for i in range(122):
            time.sleep(2)
            text = chat.driver.page_source
            del text
            time.sleep(3)
            tmp = chat.driver.current_activity
            del tmp
            print(i)
        chat.press_mess(".xlsx")
        flag = chat.is_text_present("撤回")
        self.assertFalse(flag)
        # 删除文件，关闭弹框菜单
        chat.click_delete()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0043(self):
        """单聊天会话页面，点击位置，再返回到会话页面"""
        # 1、在当前会话窗口点击位置
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、点击左上角的返回按钮
        location_page.click_back()
        chat.click_more()
        chat.wait_for_page_load()

    @staticmethod
    def public_send_location():
        """ 在发送位置信息 """
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        # 1、在当前会话窗口点击位置
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        addr_info = location_page.get_location_info()
        # 2、点击右上角的发送按钮
        location_page.click_send()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()
        return addr_info

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0044(self):
        """单聊天会话页面，点击位置，默认当前位置直接发送"""
        self.public_send_location()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0045(self):
        """单聊天会话页面，点击位置，选择500米内的其他位置发送"""
        # 1、在当前会话窗口点击位置
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、滑动500米内的位置列表，选择其他位置
        location_page.select_other_item()
        # 3、点击右上角的发送按钮
        location_page.click_send()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0046(self):
        """单聊天会话页面，点击位置，选择500米内的其他位置后返回到会话窗口"""
        # 1、在当前会话窗口点击位置
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、滑动500米内的位置列表，选择其他位置
        location_page.select_other_item()
        # 3、点击左上角的返回按钮
        location_page.click_back()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0047(self):
        """单聊天会话页面，长按位置消息体进行转发到本地通讯录联系人"""
        # 1、长按位置消息体
        addr_info = self.public_send_location()
        chat = SingleChatPage()
        # 2、选择转发，选择一个本地通讯录联系人
        chat.forward_file(addr_info)
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
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0048(self):
        """单聊天会话页面，长按位置消息体进行转发到和通讯录联系人"""
        # 1、在当前群聊天会话页面长按长按位置消息体
        addr_info = self.public_send_location()
        chat = SingleChatPage()
        # 2、选择一个和通讯录联系人转发
        chat.forward_file(addr_info)
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
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0049(self):
        """单聊天会话页面，长按位置消息体进行转发到群"""
        # 1、在当前群聊天会话页面长按位置消息体
        addr_info = self.public_send_location()
        chat = SingleChatPage()
        # 2、选择一个群转发
        chat.forward_file(addr_info)
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
            print("WARN: There is no group.")
            sogp.click_back()
            scp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0050(self):
        """单聊天会话页面点击位置消息体，在位置界面点击右下角按钮进行导航"""
        # 先发送位置信息
        chat = SingleChatPage()
        self.public_send_location()
        # 1、在当前页面点击位置消息体
        chat.click_addr_info()
        chat.wait_for_location_page_load()
        # 2、点击右下角按钮
        chat.click_nav_btn()
        location_page = ChatLocationPage()
        toast_flag = location_page.is_toast_exist("未发现手机导航应用", timeout=3)
        map_flag = location_page.is_text_present("地图")
        self.assertTrue(toast_flag or map_flag)
        location_page.driver.back()
        time.sleep(0.3)
        if not chat.is_on_this_page():
            location_page.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def click_open_file(file_type):
        """在聊天会话页面打开自己发送的文件"""
        chat = SingleChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
            local_file.click_send()
            # 打开文件
            chat.open_file_in_chat_page(file_type)
            chat.wait_for_open_file()
            chat.click_back_in_open_file_page()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0051(self):
        """单聊天会话页面，点击自己发送格式为doc的文件"""
        self.click_open_file(".doc")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0052(self):
        """单聊天会话页面，点击自己发送格式为docx的文件"""
        self.click_open_file(".docx")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0053(self):
        """单聊天会话页面，点击自己发送格式为ppt的文件"""
        self.click_open_file(".ppt")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0054(self):
        """单聊天会话页面，点击自己发送格式为pptx的文件"""
        self.click_open_file(".pptx")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0055(self):
        """单聊天会话页面，点击自己发送格式为pdf的文件"""
        self.click_open_file(".pdf")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0056(self):
        """单聊天会话页面，点击自己发送格式为xls的文件"""
        self.click_open_file(".xls")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0057(self):
        """单聊天会话页面，点击自己发送格式为xlsx的文件"""
        self.click_open_file(".xlsx")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_private_chat_file_location_0058(self):
        """单聊天会话页面，点击自己发送格式为txt的文件"""
        self.click_open_file(".txt")


class MsgPrivateChatAllTest(TestCase):
    """
    模块：单聊
    文件位置：1.1.3全量测试用例->113全量测试用例-韦凤莲.xlsx
    表格：单聊
    Author:刘晓东
    """

    def default_setUp(self):
        """
        1、成功登录和飞信
        2.确保每个用例运行前在单聊会话页面
        """

        Preconditions.select_mobile('Android-移动')
        name = "大佬1"
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_single_chat_page(name)
            return
        scp = SingleChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_single_chat_page(name)

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        file_type = ".txt"
        # 1、2.发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 3.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        time.sleep(2)
        # 获取发送的文件名称
        file_name = scp.get_current_file_name()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 4.该消息窗口是否显示文件+文件名
        self.assertEquals(mp.is_message_content_match_file_name(file_name), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0002(self):
        """网络异常时勾选本地文件内任意文件点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        file_type = ".txt"
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        name = "大佬1"
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1、2.发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 3.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)

    @staticmethod
    def tearDown_test_msg_0002():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0003(self):
        """会话页面有文件发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        file_type = ".txt"
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 1.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 2.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_0003():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0004(self):
        """对发送失败的文件进行重发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的文件重发
        file_type = ".txt"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)

    @staticmethod
    def tearDown_test_msg_0004():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0005(self):
        """对发送失败的文件进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面有发送失败的文件重发
        file_type = ".txt"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 3.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), False)

    @staticmethod
    def tearDown_test_msg_0005():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0006(self):
        """点击取消重发文件消失，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的文件重发
        file_type = ".txt"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_cancel()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0006():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0007(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型文件
        Preconditions.send_large_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 1.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0007():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0008(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型文件
        Preconditions.send_large_file()
        local_file = ChatSelectLocalFilePage()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型文件发送
        Preconditions.send_large_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0008():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_0009(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型文件
        Preconditions.send_large_file()
        local_file = ChatSelectLocalFilePage()
        # 勾选以后不再提示
        local_file.click_no_longer_prompt()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型文件发送
        Preconditions.send_large_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示，文件是否发送成功
        self.assertEquals(local_file.is_exist_continue_send(), False)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), False)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), False)
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_0009():
        """恢复网络，重置app，确保不影响其他用例执行"""

        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.make_already_in_message_page(True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0010(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型文件
        Preconditions.send_large_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        local_file.click_free_flow_privilege()
        # 1.等待免流订购页面加载
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        # 2.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0010():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0012(self):
        """在文件列表页选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        file_type = ".txt"
        # 1、2.进入预置文件目录
        Preconditions.enter_preset_file_catalog()
        local_file = ChatSelectLocalFilePage()
        # 选择文件
        local_file.select_file(file_type)
        time.sleep(2)
        # 再次选择，取消
        local_file.select_file(file_type)
        # 3.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0013(self):
        """在文件列表页点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地文件
        csfp.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        time.sleep(2)
        # 1.等待选择文件页面加载
        csfp.wait_for_page_load()
        csfp.click_back()
        time.sleep(2)
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0014(self):
        """勾选本地照片内任意相册的图片点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.发送本地图片
        Preconditions.send_local_picture()
        # 3.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 4.该消息窗口是否显示图片
        self.assertEquals(mp.is_message_content_match_picture(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0015(self):
        """网络异常时勾选本地照片内任意相册的图片点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1、2.发送本地图片
        Preconditions.send_local_picture()
        # 3.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)

    @staticmethod
    def tearDown_test_msg_0015():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0016(self):
        """会话页面有图片发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        file_type = ".jpg"
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        time.sleep(2)
        # 1.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 2.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_0016():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0017(self):
        """对发送失败的图片文件进行重发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的图片文件重发
        file_type = ".jpg"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)

    @staticmethod
    def tearDown_test_msg_0017():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0018(self):
        """对发送失败的图片进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面有发送失败的图片文件重发
        file_type = ".jpg"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 3.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), False)

    @staticmethod
    def tearDown_test_msg_0018():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0019(self):
        """点击取消重发图片消息，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的图片文件重发
        file_type = ".jpg"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_cancel()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0019():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0020(self):
        """未订购每月10G的用户发送大于2M的图片时有弹窗提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型图片文件
        Preconditions.send_large_picture_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 1.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0020():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0021(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型图片文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型图片文件发送
        Preconditions.send_large_picture_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0021():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_0022(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型图片文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 勾选以后不再提示
        local_file.click_no_longer_prompt()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型图片文件发送
        Preconditions.send_large_picture_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示，文件是否发送成功
        self.assertEquals(local_file.is_exist_continue_send(), False)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), False)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), False)
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_0022():
        """恢复网络，重置app，确保不影响其他用例执行"""

        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.make_already_in_message_page(True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0023(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型图片文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        local_file.click_free_flow_privilege()
        # 1.等待免流订购页面加载
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        # 2.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0023():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0025(self):
        """在选择图片页面选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        # 选择本地照片
        local_file.click_picture()
        time.sleep(2)
        # 再次选择，取消
        local_file.click_picture()
        # 3.等待图片列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0026(self):
        """在选择图片页面点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        # 2.等待选择文件页面加载
        csfp.wait_for_page_load()
        csfp.click_back()
        # 3.等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0028(self):
        """勾选本地视频内任意视频点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.发送本地视频
        Preconditions.send_local_video()
        # 3.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 4.该消息窗口是否显示视频
        self.assertEquals(mp.is_message_content_match_video(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0029(self):
        """网络异常时勾选本地文件内任意视频点击发送按钮"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1、2.发送本地视频
        Preconditions.send_local_video()
        # 3.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)

    @staticmethod
    def tearDown_test_msg_0029():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0030(self):
        """会话页面有视频发送失败时查看消息列表是否有消息发送失败的标识"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面没有重发按钮影响验证结果
        Preconditions.make_no_retransmission_button(name)
        # 设置手机网络断开
        scp.set_network_status(0)
        file_type = ".mp4"
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        # 1.验证是否发送失败，是否存在重发按钮
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        self.assertEquals(scp.is_exist_msg_send_failed_button(), True)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 2.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_0030():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0031(self):
        """对发送失败的视频进行重发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的视频文件重发
        file_type = ".mp4"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        time.sleep(2)
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)

    @staticmethod
    def tearDown_test_msg_0031():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0032(self):
        """对发送失败的视频进行重发后，消息列表页面的消息发送失败的标识消失"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        name = "大佬1"
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status(name)
        # 确保当前单聊会话页面有发送失败的视频文件重发
        file_type = ".mp4"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_sure()
        # 2.验证是否重发成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 3.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), False)

    @staticmethod
    def tearDown_test_msg_0032():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0033(self):
        """点击取消重发视频文件消失，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前单聊会话页面有发送失败的视频文件重发
        file_type = ".mp4"
        scp.set_network_status(0)
        # 发送指定类型文件
        Preconditions.send_file_by_type(file_type)
        scp.set_network_status(6)
        # 1.点击重发按钮
        scp.click_msg_send_failed_button(-1)
        time.sleep(2)
        scp.click_cancel()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0033():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0034(self):
        """未订购每月10G的用户发送大于2M的视频时有弹窗提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型视频文件
        Preconditions.send_large_video_file()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        # 1.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0034():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0035(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型视频文件
        Preconditions.send_large_video_file()
        local_file = ChatSelectLocalFilePage()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型视频文件发送
        Preconditions.send_large_video_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示
        self.assertEquals(local_file.is_exist_continue_send(), True)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), True)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), True)
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0035():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_0036(self):
        """勾选“以后不再提示”再点击“继续发送”"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型视频文件
        Preconditions.send_large_video_file()
        local_file = ChatSelectLocalFilePage()
        # 勾选以后不再提示
        local_file.click_no_longer_prompt()
        # 点击继续发送
        local_file.click_continue_send()
        # 1.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 再次选择大型视频文件发送
        Preconditions.send_large_video_file()
        time.sleep(2)
        # 2.是否弹出继续发送、订购免流特权、以后不再提示，文件是否发送成功
        self.assertEquals(local_file.is_exist_continue_send(), False)
        self.assertEquals(local_file.is_exist_free_flow_privilege(), False)
        self.assertEquals(local_file.is_exist_no_longer_prompt(), False)
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_0036():
        """恢复网络，重置app，确保不影响其他用例执行"""

        mp = MessagePage()
        mp.set_network_status(6)
        Preconditions.make_already_in_message_page(True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0037(self):
        """点击订购免流特权后可正常返回"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置当前网络为2/3/4G
        scp.set_network_status(4)
        # 发送大型视频文件
        Preconditions.send_large_video_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        local_file.click_free_flow_privilege()
        # 1.等待免流订购页面加载
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()
        time.sleep(2)
        local_file.tap_coordinate([(100, 20), (100, 60), (100, 100)])
        # 2.等待文件列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_0037():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0039(self):
        """在视频列表页选择文件后再点击取消按钮，停留在当前页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1、2.进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        # 选择本地视频
        local_file.click_video()
        time.sleep(2)
        # 再次选择，取消
        local_file.click_video()
        # 3.等待视频列表页面加载
        local_file.wait_for_page_load()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_back()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_0040(self):
        """在视频列表页点击返回按钮时可正常逐步返回到会话页面"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.click_back()
        csfp = ChatSelectFilePage()
        # 1.等待选择文件页面加载
        csfp.wait_for_page_load()
        csfp.click_back()
        # 2.等待单聊会话页面加载
        scp.wait_for_page_load()



