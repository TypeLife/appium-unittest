import random
import re
import time
import unittest
import uuid

from appium.webdriver.common.mobileby import MobileBy

import preconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.groupset.GroupChatSetPicVideo import GroupChatSetPicVideoPage
from selenium.common.exceptions import TimeoutException

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
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

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
        one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """
        前置条件：
        1.已登录客户端
        2.当前在消息页面
        """
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
        login_num = Preconditions.login_by_one_key_login()
        return login_num

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

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
        time.sleep(3)
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
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
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
        group_name = "c" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_have_my_picture():
        """确保当前群聊页面已有图片"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.is_on_this_page()
        if gcp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_pic_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def make_already_have_my_videos():
        """确保当前群聊页面已有视频"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.wait_for_page_load()
        if gcp.is_exist_msg_videos():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_video_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n = n + 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()


class MsgGroupChatvedioTest(TestCase):
    """
    模块：消息->群聊>图片&视频

    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：消息-群聊图片&视频
    作者：方康

    """

    """前置条件需要修改创建一个群找不到"""

    # @classmethod
    # def setUpClass(cls):
    #
    #     # 创建联系
    #     fail_time = 0
    #     import dataproviders
    #     while fail_time < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             Preconditions.connect_mobile('Android-移动')
    #             current_mobile().hide_keyboard_if_display()
    #             for name, number in required_contacts:
    #                 Preconditions.make_already_in_message_page()
    #                 conts.open_contacts_page()
    #                 try:
    #                     if conts.is_text_present("发现SIM卡联系人"):
    #                         conts.click_text("显示")
    #                 except:
    #                     pass
    #                 conts.create_contacts_if_not_exits(name, number)
    #
    #             # 创建群
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             return
    #         except:
    #             fail_time += 1
    #             import traceback
    #             msg = traceback.format_exc()
    #             print(msg)

    # @classmethod
    # def setUpClass(cls):
    #     Preconditions.connect_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     local_file = ChatSelectLocalFilePage()
    #     # 没有预置文件，则上传
    #     local_file.push_preset_file()

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
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0001(self):
        """群聊会话页面，不勾选相册内图片点击发送按钮"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 4.判断发送按钮是否能点击
        flg = cpg.send_btn_is_enabled()
        self.assertEquals(flg, False)
        # 5.点击返回
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0002(self):
        """群聊会话页面，勾选相册内一张图片发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        # 4.点击发送返回到群聊页面,校验是否发送成功
        cpg.click_send()
        gcp.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0003(self):
        """群聊会话页面，预览相册内图片"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        # 4.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 5. 校验照片是否可以预览
        self.assertIsNotNone(cpp.get_pic_preview_info())
        # 6.点击返回
        cpp.click_back()
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0004(self):
        """群聊会话页面，预览相册内图片，不勾选原图发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        # 4.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 5.点击发送,
        cpp.click_send()
        gcp.is_on_this_page()
        self.assertEqual(gcp.is_send_sucess(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0005(self):
        """群聊会话页面，预览相册数量与发送按钮数量一致"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择n<=9张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(3)
        # 4.点击预览检验，预览相册数量与发送按钮数量一致
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        ppi = cpp.get_pic_preview_num()
        ppn = cpp.get_pic_send_num()
        self.assertEquals(ppi, ppn)
        cpp.click_back()
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0006(self):
        """群聊会话页面，编辑图片发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片,点击预览
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 4.点击编辑（预览图片）
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # a 涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # b 马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # c 文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        cpe.click_picture_save()
        cpe.click_picture_send()
        # 6 点击发送后，判断在群聊首页
        gcp.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0007(self):
        """群聊会话页面，编辑图片发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片,点击点击打开
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_pic_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 4.点击编辑（预览图片）
        time.sleep(2)
        cpp.click_edit()
        cpe = ChatPicEditPage()
        time.sleep(1)
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # a 涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # b 马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # c 文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        cpe.click_picture_save()
        cpe.click_picture_send()
        # 6 点击发送后，判断在群聊首页,校验是否发送成功
        gcp.wait_for_page_load()
        gcp.is_on_this_page()
        self.assertEqual(gcp.is_send_sucess(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0008(self):
        """群聊会话页面，编辑图片发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片,点击点击打开
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_pic_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 4.点击编辑（预览图片）
        time.sleep(2)
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击图片编辑（预览图片）
        cpe.click_picture_edit()
        # a 涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # b 马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # c 文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我qqqqqqqq程师")
        time.sleep(1)
        cpe.click_picture_save()
        cpe.click_picture_save()
        cpe.click_picture_send()
        # 6 点击发送后，判断在群聊首页
        gcp.wait_for_page_load()
        time.sleep(1)
        gcp.is_on_this_page()
        self.assertEqual(gcp.is_send_sucess(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0009(self):
        """群聊会话页面，编辑图片发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片,点击点击打开
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_pic_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 4.点击编辑（预览图片）
        time.sleep(2)
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # a 涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # b 马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # c 文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        cpe.click_picture_save()
        cpe.click_picture_save()
        cpe.click_picture_send()
        # 6 点击发送后，判断在群聊首页,校验是否发送成功
        gcp.wait_for_page_load()
        gcp.is_on_this_page()
        self.assertEqual(gcp.is_send_sucess(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0010(self):
        """群聊会话页面，取消编辑图片,不发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片,点击点击打开
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        cpg.click_pic_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 4.点击编辑（预览图片）
        time.sleep(2)
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # a 涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # b 马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # c 文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        cpe.click_picture_cancel()
        cpe.click_picture_cancel()
        # 6.点击返回
        cpp.click_back()
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0011(self):
        """群聊会话页面，取消编辑图片,发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片,点击点击打开
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        cpg.click_pic_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 4.点击编辑（预览图片）
        time.sleep(2)
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # a 涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # b 马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # c 文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        cpe.click_picture_cancel()
        cpe.click_picture_cancel()
        cpe.click_picture_select()
        cpe.click_picture_send()
        # 6 点击发送后，判断在群聊首页
        gcp.is_on_this_page()
        gcp.wait_for_page_load()
        self.assertEqual(gcp.is_send_sucess(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0012(self):
        """群聊会话页面，发送相册内的图片，校验预览格式"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(n=1)
        # 4.点击点击打开,校验格式
        cpg.click_pic_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        flag = cpp.get_pic_preview_info()
        self.assertIsNotNone(re.match(r'预览\(\d+/\d+\)', flag))
        # 5.点击返回
        cpp.click_back()
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0013(self):
        """群聊会话页面，点击该相册内两张图片，点击预览，隐藏"编辑"按钮"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择2张相片,点击预览打开
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(n=2)
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        # 4.校验预览页面中隐藏"编辑"按钮的提示/6.2.9版本有改变
        cpp.wait_for_page_load()
        cpp.click_edit()
        # fla = cpp.edit_btn_is_toast()
        # self.assertEqual(fla, True)
        # 5.点击返回
        cpe = ChatPicEditPage()
        cpe.click_cancle()
        cpp.click_back()
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0014(self):
        """群聊会话页面，勾选9张相册内图片发送"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        time.sleep(1)
        gcp.click_picture()
        # 3.进入相片页面,选择9张相片发送
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(n=9)
        cpg.click_send()
        time.sleep(2)
        # 4.点击发送后，判断在群聊首页
        gcp.is_on_this_page()
        gcp.wait_for_page_load()
        self.assertEqual(gcp.is_send_sucess(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0015(self):
        """群聊会话页面，勾选10张相册内图片发送校验"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,选择大于或等于10张相片,校验提示：“最多只能选择9张照片”
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(10)
        flg1 = cpg.is_toast_exist_maxp()
        self.assertEqual(flg1, True)
        flg2 = cpg.get_pic_send_nums()
        self.assertEqual(flg2, '9')
        # 4.点击返回
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0016(self):
        """群聊会话页面，同时发送相册中的图片和视屏"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击输入框左上方的相册图标
        gcp.click_picture()
        # 3.进入相片页面,同时选择视频和图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(n=1)
        cpg.select_video_fk(n=1)
        flag = cpg.is_toast_exist_pv()
        self.assertEqual(flag, True)
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0017(self):
        """群聊会话页面，使用拍照功能拍照发送照片"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击点击富媒体行拍照图标
        gcp.click_take_photo()
        # 3.进入相机拍照页面，点击拍照
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.send_photo()
        time.sleep(1)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0018(self):
        """群聊会话页面，使用拍照功能拍照编辑后发送照片"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击点击富媒体行拍照图标
        gcp.click_take_photo()
        # 3.进入相机拍照页面，点击拍照
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        cpe = ChatPicEditPage()
        cpe.click_text_edit_btn()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("正在编辑图片")
        time.sleep(1)
        cpe.click_picture_save()
        cpe.click_send()
        time.sleep(1)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0019(self):
        """群聊会话页面，使用拍照功能拍照编辑后发送照片"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击点击富媒体行拍照图标
        gcp.click_take_photo()
        # 3.进入相机拍照页面，点击拍照
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        cpe = ChatPicEditPage()
        cpe.click_text_edit_btn()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("正在编辑图片")
        time.sleep(1)
        cpe.click_picture_save()
        cpe.click_picture_save()
        cpe.click_send()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0020(self):
        """群聊会话页面，使用拍照功能拍照编辑后发送照片"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击点击富媒体行拍照图标
        gcp.click_take_photo()
        # 3.进入相机拍照页面，点击拍照
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        cpe = ChatPicEditPage()
        cpe.click_text_edit_btn()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("正在编辑图片")
        time.sleep(1)
        cpe.click_picture_save()
        cpe.click_picture_cancel()
        time.sleep(1)
        cpp.send_photo()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0022(self):
        """群聊会话页面，打开拍照，拍照之后返回会话窗口"""
        # 1.检验是否当前聊天会话页面，
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击点击富媒体行拍照图标
        gcp.click_take_photo()
        # 3.进入相机拍照页面，点击取消拍照
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo_back()
        # 4.校验是否已经返回到聊天页面
        gcp.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0026(self):
        """群聊会话页面，转发他人发送的图片给本地联系人"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.长按他人所发的图片
        gcp.forward_pic()
        # 3.选择任意本地联系人
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 4.选择第一个本地联系人发送
        slc.swipe_select_one_member_by_name("和飞信电话")
        slc.click_sure_forward()
        # 5.校验是否在消息聊天页面，是否提示已转发
        gcp.is_on_this_page()
        self.assertEquals(gcp.is_exist_forward(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0028(self):
        """群聊会话页面，转发他人发送的图片给陌生人"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.长按他人所发的图片转发
        gcp.forward_pic()
        # 3.选择搜索给陌生人
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.search("15915915911")
        # 4.校验是否是陌生人号码
        self.assertEquals(scp.is_present_unknown_member(), True)
        # 5.点击发送
        scp.click_unknown_member()
        scp.click_sure_forward()
        # 6.校验是否在消息聊天页面，是否提示已转发
        gcp.is_on_this_page()
        self.assertEquals(gcp.is_exist_forward(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0030(self):
        """群聊会话页面，删除自己发送的图片"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.长按他人所发的图片转发
        gcp.press_pic()
        gcp.click_delete()
        time.sleep(2)
        # 3.校验是否在消息聊天页面，是否提示已删除成功
        gcp.is_on_this_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0032(self):
        """群聊会话页面，收藏自己发送的照片"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.长按他人所发的图片收藏该图
        gcp.press_pic()
        gcp.click_collection()
        # 3.校验提示已收藏消息，
        gcp.is_on_this_page()
        self.assertEquals(gcp.is_exist_collection(), True)
        # 4.返回到消息主页
        # 6.2.9版本有改动
        gcp.click_back()
        # SelectOneGroupPage().click_back()
        # SelectContactsPage().click_back()
        from pages.components.Footer import FooterPage
        # 5.进入我的-收藏页面
        fp = FooterPage()
        fp.open_me_page()
        me = MePage()
        me.click_collection()
        # 6.校验我的模块中是否有已收藏的图片
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        self.assertEquals(mcp.have_collection_pic(), True)
        # 7.返回到消息页
        mcp.click_back()
        fp.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0036(self):
        """群聊会话页面，转发自己发送的视频给本地联系人"""
        # 1.检验是否当前聊天会话页面且有视频
        Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.长按他人所发的视频
        gcp.forward_video()
        # 3.选择任意本地联系人
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 4.选择第一个本地联系人发送
        slc.swipe_select_one_member_by_name("给个红包3")
        slc.click_sure_forward()
        # 5.校验是否在消息聊天页面，是否提示已转发
        gcp.is_on_this_page()
        self.assertEquals(gcp.is_exist_forward(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0038(self):
        """群聊会话页面，转发他人发送的视频给陌生人"""
        # 1.检验是否当前聊天会话页面且有视频
        Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.长按他人所发的视频转发
        gcp.forward_video()
        # 3.选择搜索给陌生人
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.search("15912312311")
        # 4.校验是否是陌生人号码
        self.assertEquals(scp.is_present_unknown_member(), True)
        # 5.点击发送
        scp.click_unknown_member()
        scp.click_sure_forward()
        # 6.校验是否在消息聊天页面，是否提示已转发
        gcp.is_on_this_page()
        self.assertEquals(gcp.is_exist_forward(), True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0040(self):
        """群聊会话页面，删除自己发送的视频"""
        # 1.检验是否当前聊天会话页面且有视频
        Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.长按自己所发的视频转的删除
        gcp.press_video()
        gcp.click_delete()
        # 3.校验是否在消息聊天页面，是否提示已删除成功
        gcp.is_on_this_page()
        self.assertEquals(gcp.is_exist_msg_videos(), False)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0042(self):
        """群聊会话页面，收藏自己发送的视频"""
        # 1.检验是否当前聊天会话页面且有视频
        Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.长按他人所发的视频收藏该视频
        gcp.press_video()
        gcp.click_collection()
        # 3.校验提示已收藏消息，
        gcp.is_on_this_page()
        self.assertEquals(gcp.is_exist_collection(), True)
        # 4.返回到消息主页
        gcp.click_back()
        # SelectOneGroupPage().click_back()
        # SelectContactsPage().click_back()
        from pages.components.Footer import FooterPage
        # 5.进入我的-收藏页面
        fp = FooterPage()
        fp.open_me_page()
        me = MePage()
        me.click_collection()
        # 6.校验我的模块中是否有已收藏的视频
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        self.assertEquals(mcp.have_collection_video(), True)
        # 7.返回到消息页
        mcp.click_back()
        fp.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0043(self):
        """群聊会话页面，发送相册内的视频"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.选择勾选视频不发送
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        # 3.校验发送按钮是高亮可点击
        self.assertEquals(cpg.send_btn_is_enabled(), True)
        self.assertIsNotNone(cpg.get_video_times()[1])
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0044(self):
        """群聊会话页面，发送相册内一个视频"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.选择视频发送
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        cpg.click_send()
        time.sleep(5)
        # 3.校验发送成功，会话窗口可见可播放
        gcp.is_on_this_page()
        flg = gcp.wait_for_play_video_button_load()
        self.assertIsNotNone(flg)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0045(self):
        """群聊会话页面，发送相册内多个视频"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.选择多个视频发送
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(2)
        # 3.检验选择多个视频提示
        cpg.is_toast_exist_more_video()
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0046(self):
        """群聊会话页面，群聊会话页面，同时发送相册内视频和图片"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.选择一个视频和一张图片发送
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.select_video_fk(1)
        # 3.检验选择视频和图片的提示
        cpg.is_toast_exist_pv()
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0047(self):
        """群聊会话页面，发送视频时预览视频"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.选择一个视频和一张图片发送
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        # 3.点击预览，检验预览视频
        cpg.click_preview()
        time.sleep(1)
        self.assertEquals(cpg.pre_video_btn_is_enabled(), True)
        cpp = ChatPicPreviewPage()
        cpp.click_back()
        cpg.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0060(self):
        """在群聊会话窗，验证点击趣图搜搜入口"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击gif图片
        gcp.click_gif()
        # 3.校验是否有gif图片出现
        gcp.hide_keyboard()
        gcp.wait_for_gif_ele_load()
        gcp.click_cancel_gif()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0061(self):
        """在群聊会话窗，网络正常发送表情搜搜"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击gif图片
        gcp.click_gif()
        # 3.校验是否有gif图片出现
        gcp.hide_keyboard()
        gcp.wait_for_gif_ele_load()
        gcp.send_gif()
        self.assertEquals(gcp.is_send_gif(), True)
        gcp.click_cancel_gif()

    @unittest.skip("断网后gif图片无法加载")
    def test_msg_group_chat_video_0062(self):
        """在群聊会话窗，断网情况下发送表情搜搜"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.设置手机网络断开
        gcp.set_network_status(0)
        # 3.点击gif图片
        gcp.click_gif()
        # 4.校验网络不可用
        self.assertEquals(gcp.is_exist_network(), True)
        # 5恢复网络
        gcp.set_network_status(6)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0063(self):
        """在群聊会话窗，搜索数字关键字选择发送趣图"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击gif图片
        gcp.click_gif()
        gcp.input_gif(2)
        gcp.wait_for_gif_ele_load()
        gcp.send_gif()
        self.assertEquals(gcp.is_send_gif(), True)
        gcp.click_cancel_gif()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0064(self):
        """在群聊会话窗，搜索特殊字符关键字选择发送趣图"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击gif图片
        gcp.click_gif()
        gcp.input_gif("?")
        gcp.wait_for_gif_ele_load()
        gcp.send_gif()
        self.assertEquals(gcp.is_send_gif(), True)
        gcp.click_cancel_gif()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0065(self):
        """在群聊会话窗，搜索无结果的趣图"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击gif图片
        gcp.click_gif()
        gcp.input_gif("3")
        self.assertEquals(gcp.is_gif_exist_toast(), True)
        gcp.click_cancel_gif()
        gcp.edit_clear("3")

    @unittest.skip("断网后gif图片无法加载")
    def test_msg_group_chat_video_0068(self):
        """在群聊会话窗，趣图发送失败后出现重新发送按钮"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击gif图片,输入关键字搜索gif图片
        gcp.click_gif()
        gcp.input_gif("2")
        gcp.wait_for_gif_ele_load()
        # 3.断掉网络，点击发送
        gcp.set_network_status(0)
        gcp.send_gif()
        # 4.检验发送失败的标示
        self.assertEquals(gcp.is_send_sucess(), False)
        # 5.重新连接网络，再发
        gcp.set_network_status(6)
        gcp.click_send_again()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0069(self):
        """在群聊会话窗，关闭GIF搜索框"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击gif图片
        gcp.click_gif()
        gcp.wait_for_gif_ele_load()
        # 3.关闭gif图片，校验是否已关闭
        gcp.click_cancel_gif()
        self.assertEquals(gcp.is_exist_gif_ele(), False)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0072(self):
        """转发聊天内容中的已下载的图片（缩略图）"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.press_file_to_do("转发")
        # 5.检验在选择联系人页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 6.点击返回到群聊页面
        scp.click_back()
        gcv.click_back()
        gcf.click_back()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_group_chat_video_0073(self):
        """转发聊天内容中的已下载的图片（放大图）"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.click_pic_video()
        time.sleep(1.8)
        gcv.press_pre_file_to_do("转发")
        # 5.检验在选择联系人页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 6.点击返回到群聊页面
        scp.click_back()
        gcv.click_pre_pic_video()
        gcv.click_back()
        gcf.click_back()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0074(self):
        """转发聊天内容中的已下载的图片给任意对象"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.press_file_to_do("转发")
        # 5.检验在选择联系人页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.select_local_contacts()
        scp.click_one_contact("大佬2")
        scp.click_sure_forward()
        self.assertEquals(gcv.is_toast_exist_zf(), True)
        # 6.点击返回到群聊页面//6.2.9版本有改动
        gcv.click_back()
        gcf.click_back()
        gcs.click_element([MobileBy.XPATH, "//*[contains(@resource-id,'back')]"], 15)
        # gcp.click_element([MobileBy.XPATH, "//*[contains(@resource-id,'back')]"], 15)
        # sog = SelectOneGroupPage()
        # sog.click_back()
        # sct = SelectContactsPage()
        gcp.click_back()
        scp.click_one_contact("大佬2")
        if gcp.is_exist_dialog():
            gcp.click_i_have_read()
        self.assertEquals(gcp.is_exist_msg_image(), True)
        gcp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0077(self):
        """转发聊天内容中的已下载的视频（缩略图）"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.press_file_to_do("转发")
        # 5.检验在选择联系人页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 6.点击返回到群聊页面
        scp.click_back()
        gcv.click_back()
        gcf.click_back()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0078(self):
        """转发聊天内容中的已下载的视频（放大图）"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.click_pic_video()
        time.sleep(1.9)
        gcv.press_pre_video_to_do("转发")
        # 5.检验在选择联系人页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 6.点击返回到群聊页面
        scp.click_back()
        gcv.click_close_pre_video()
        time.sleep(1)
        if gcv._is_element_present(["id", 'com.chinasofti.rcs:id/title']):
            gcv.click_back()
        time.sleep(1)
        gcf.click_back()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0079(self):
        """转发聊天内容中的已下载的视频给任意对象"""
        # 1.检验是否当前聊天会话页面且有视频
        Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.press_file_to_do("转发")
        # 5.检验在选择联系人页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.select_local_contacts()
        scp.click_one_contact("大佬3")
        scp.click_sure_forward()
        self.assertEquals(gcv.is_toast_exist_zf(), True)
        # 6.点击返回到群聊页面
        gcv.click_back()
        time.sleep(1)
        gcf.click_back()
        time.sleep(2)
        gcs.click_back()
        time.sleep(1)
        gcp.click_back()
        # sog = SelectOneGroupPage()
        # sog.click_back()
        # sct = SelectContactsPage()
        # sct.click_back()
        scp.click_one_contact("大佬3")
        time.sleep(1)
        self.assertEquals(gcp.is_exist_msg_videos(), True)
        time.sleep(1)
        gcp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0081(self):
        """收藏聊天内容中的已下载的图片"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        gcp.click_clean_video()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.press_file_to_do("收藏")
        # 5.检验是否有已收藏提示，且返回到消息页
        self.assertEquals(gcv.is_toast_exist_sc(), True)
        gcv.click_back()
        gcf.click_back()
        gcs.click_back()
        gcp.click_back()
        # sog = SelectOneGroupPage()
        # sog.click_back()
        # sct = SelectContactsPage()
        # sct.click_back()
        from pages.components.Footer import FooterPage
        # 6.进入我的-收藏页面
        fp = FooterPage()
        fp.open_me_page()
        me = MePage()
        me.click_collection()
        # 7.校验我的模块中是否有已收藏的图片
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        self.assertEquals(mcp.have_collection_pic(), True)
        # 8.返回到消息页
        mcp.click_back()
        fp.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0082(self):
        """删除聊天内容中的图片"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面,点击删除
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.press_file_to_do("删除")
        gcv.click_back()
        gcf.click_back()
        gcs.click_back()
        # self.assertEquals(gcp.is_exist_msg_image(), False)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0083(self):
        """保存聊天内容中的图片到本地"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面,点击保存图片
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.click_pic_video()
        time.sleep(1)
        gcv.press_pre_file_to_do("保存图片")
        # 5.校验图片是否已保存成功
        self.assertEquals(gcv.is_toast_exist_save(), True)
        # 6.饭回到消息页面
        gcv.click_pre_pic_video()
        gcv.click_back()
        gcf.click_back()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0084(self):
        """保存聊天内容中的视频到本地"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.click_video()
        time.sleep(1)
        gcv.press_pre_video_to_do("保存视频")
        # 5.检验在选择联系人页面
        self.assertEquals(gcv.is_toast_exist_save_video(), True)
        gcv.click_close_pre_video()
        time.sleep(1)
        if gcv._is_element_present(["id", 'com.chinasofti.rcs:id/title']):
            gcv.click_back()
        time.sleep(1)
        gcf.click_back()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_group_chat_video_0085(self):
        """编辑聊天内容中的图片，并发送"""
        # 1.检验是否当前聊天会话页面且有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        gcp.click_clean_video()
        # 2.打开设置-查找聊天内容
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        # 3.进入搜索消息页面，点击图片与视频
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.click_pic_video()
        # 4.进入图片与视频页面,点击保存图片
        gcv = GroupChatSetPicVideoPage()
        gcv.wait_for_page_load()
        gcv.click_pic_video()
        time.sleep(1)
        gcv.press_pre_file_to_do("编辑")
        # 5.点击文本编辑（预览图片）
        cpe = ChatPicEditPage()
        time.sleep(1)
        cpe.click_picture_edit()
        # a 涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # b 马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # c 文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        cpe.click_picture_save()
        cpe.click_picture_send()
        # 6.检验在选择联系人页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 7.返回到消息页面
        scp.click_back()
        gcv.click_pre_pic_video()
        gcv.click_back()
        gcf.click_back()
        gcs.click_back()


class MsgGroupChatVideoPicAllTest(TestCase):
    """
    模块：群聊-图片视频-GIF
    文件位置：1.1.3全量测试用例->113全量用例--肖立平.xlsx
    表格：群聊-图片视频-GIF
    Author:刘晓东
    """

    @classmethod
    def setUpClass(cls):

        # 创建联系人
        fail_time = 0
        flag = False
        import dataproviders
        while fail_time < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                Preconditions.connect_mobile('Android-移动')
                current_mobile().hide_keyboard_if_display()
                for name, number in required_contacts:
                    Preconditions.make_already_in_message_page()
                    conts.open_contacts_page()
                    conts.create_contacts_if_not_exits(name, number)

                # 创建群
                required_group_chats = dataproviders.get_preset_group_chats()

                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag = True
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)
            if flag:
                break

        # 确保测试手机有resource文件夹
        name = "群聊1"
        Preconditions.get_into_group_chat_page(name)
        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_more()
        # 点击本地文件
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        local_file.push_preset_file()
        local_file.click_back()
        csfp.wait_for_page_load()
        csfp.click_back()
        gcp.wait_for_page_load()

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、确保当前页面在群聊聊天会话页面
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        name = "群聊1"
        if mp.is_on_this_page():
            Preconditions.get_into_group_chat_page(name)
            return
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            # preconditions.force_close_and_launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page(name)

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0021(self):
        """群聊会话页面，打开拍照，立刻返回会话窗口"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 点击富媒体行拍照图标
        gcp.click_take_photo()
        cpp = ChatPhotoPage()
        # 等待聊天拍照页面加载
        cpp.wait_for_page_load()
        # 点击"∨"
        cpp.take_photo_back()
        # 等待群聊页面加载
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0041(self):
        """群聊会话页面,转发自己发送的图片到当前会话窗口"""

        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        time.sleep(2)
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_number(0)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0042(self):
        """群聊会话页面，转发他人发送的图片到当前会话窗口时失败"""

        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        time.sleep(2)
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_number(0)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        cwp = ChatWindowPage()
        # 5.是否显示消息发送失败标识
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)

    @staticmethod
    def tearDown_test_msg_group_chat_total_quantity_0042():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0043(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时点击取消转发"""

        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        time.sleep(2)
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_number(0)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回群聊天页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0044(self):
        """群聊会话页面，转发自己发送的图片给本地联系人"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬1"
        # 3.选择一个本地联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的聊天页
        message.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0045(self):
        """群聊会话页面，转发自己发送的图片到本地联系人时失败"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬1"
        # 3.选择一个本地联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的聊天页
        message.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.是否显示消息发送失败标识
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 返回消息页
        gcp.click_back()

    @staticmethod
    def tearDown_test_msg_group_chat_total_quantity_0045():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0046(self):
        """群聊会话页面，转发自己发送的图片到本地联系人时点击取消转发"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬1"
        # 3.选择一个本地联系人
        slc.selecting_local_contacts_by_name(name)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        # 返回群聊天页面
        slc.click_back()
        scg.wait_for_page_load()
        scg.click_back()

    # @tags('ALL', 'CMCC', 'LXD')
    # def test_msg_group_chat_total_quantity_0047(self):
    #     """群聊会话页面，转发自己发送的图片给和通讯录联系人"""
    #
    #     # 确保当前群聊页面已有图片
    #     Preconditions.make_already_have_my_picture()
    #     gcp = GroupChatPage()
    #     # 等待群聊页面加载
    #     gcp.wait_for_page_load()
    #     # 1.长按自己发送的图片并转发
    #     gcp.forward_pic()
    #     scg = SelectContactsPage()
    #     # 2.等待选择联系人页面加载
    #     scg.wait_for_page_load()
    #     # 点击“选择和通讯录联系人”菜单
    #     scg.click_he_contacts()
    #     slc = SelectLocalContactsPage()
    #     # 等待选择联系人->本地联系人 页面加载
    #     slc.wait_for_page_load()
    #     name = "大佬1"
    #     # 3.选择一个本地联系人
    #     slc.selecting_local_contacts_by_name(name)
    #     # 确定转发
    #     scg.click_sure_forward()
    #     # 4.是否提示已转发,等待群聊页面加载
    #     self.assertEquals(gcp.is_exist_forward(), True)
    #     gcp.wait_for_page_load()
    #     # 返回到消息页
    #     gcp.click_back()
    #     sog = SelectOneGroupPage()
    #     sog.wait_for_page_load()
    #     sog.click_back()
    #     scg.wait_for_page_load()
    #     scg.click_back()
    #     message = MessagePage()
    #     # 等待消息页面加载
    #     message.wait_for_page_load()
    #     # 选择刚发送消息的聊天页
    #     message.choose_chat_by_name(name)
    #     time.sleep(2)
    #     chat = BaseChatPage()
    #     if chat.is_exist_dialog():
    #         # 点击我已阅读
    #         chat.click_i_have_read()
    #     # 5.验证是否发送成功
    #     cwp = ChatWindowPage()
    #     cwp.wait_for_msg_send_status_become_to('发送成功', 10)
    #     # 返回消息页
    #     gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0050(self):
        """群聊会话页面，转发自己发送的图片给陌生人"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的陌生联系人
        message.choose_chat_by_name(number)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0051(self):
        """群聊会话页面，转发自己发送的图片到陌生人时失败"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的陌生联系人
        message.choose_chat_by_name(number)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.是否显示消息发送失败标识
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 返回消息页
        gcp.click_back()

    @staticmethod
    def tearDown_test_msg_group_chat_total_quantity_0051():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0052(self):
        """群聊会话页面，转发自己发送的图片到陌生人时点击取消转发"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回群聊天页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0053(self):
        """群聊会话页面，转发自己发送的图片到普通群"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的聊天页
        message.choose_chat_by_name(name)
        time.sleep(2)
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0054(self):
        """群聊会话页面，转发自己发送的图片到普通群时失败"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的聊天页
        message.choose_chat_by_name(name)
        time.sleep(2)
        # 5.是否显示消息发送失败标识
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 返回消息页
        gcp.click_back()

    @staticmethod
    def tearDown_test_msg_group_chat_total_quantity_0054():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0055(self):
        """群聊会话页面，转发自己发送的图片到普通群时点击取消转发"""

        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 4.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 取消转发
        sog.click_cancel_forward()
        # 5.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回群聊天页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0069(self):
        """群聊会话页面，转发自己发送的视频给本地联系人"""

        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        time.sleep(5)
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载,点击“选择本地联系人”菜单
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬1"
        # 3.选择一个本地联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的聊天页
        message.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0070(self):
        """群聊会话页面，转发自己发送的视频给本地联系人时失败"""

        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        time.sleep(5)
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载,点击“选择本地联系人”菜单
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬1"
        # 3.选择一个本地联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的聊天页
        message.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.是否显示消息发送失败标识
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 返回消息页
        gcp.click_back()

    @staticmethod
    def tearDown_test_msg_group_chat_total_quantity_0070():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0071(self):
        """群聊会话页面，转发自己发送的视频给本地联系人时点击取消转发"""

        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        time.sleep(5)
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬1"
        # 3、4.选择一个本地联系人
        slc.selecting_local_contacts_by_name(name)
        # 取消转发
        scg.click_cancel_forward()
        # 5.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        # 返回群聊天页面
        slc.click_back()
        scg.wait_for_page_load()
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0075(self):
        """群聊会话页面，转发自己发送的视频给陌生人"""

        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        time.sleep(5)
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的陌生联系人
        message.choose_chat_by_name(number)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0076(self):
        """群聊会话页面，转发自己发送的视频给陌生人时失败"""

        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        time.sleep(5)
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        message = MessagePage()
        # 等待消息页面加载
        message.wait_for_page_load()
        # 选择刚发送消息的陌生联系人
        message.choose_chat_by_name(number)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.是否显示消息发送失败标识
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 返回消息页
        gcp.click_back()

    @staticmethod
    def tearDown_test_msg_group_chat_total_quantity_0076():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_group_chat_total_quantity_0077(self):
        """群聊会话页面，转发自己发送的视频给陌生人时点击取消转发"""

        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        time.sleep(5)
        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3、4.选择陌生号码转发
        scg.click_unknown_member()
        # 取消转发
        scg.click_cancel_forward()
        # 5.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回群聊天页面
        scg.click_back()

    @unittest.skip("用例描述有误，暂时跳过")
    def test_msg_group_chat_total_quantity_0118(self):
        """在群聊会话窗，趣图发送失败后出现重新发送按钮"""

        gcs = GroupChatSetPage()
        gcp = GroupChatPage()
        # 如果当前群聊页面已有消息发送失败标识，需要先清除聊天记录
        if not gcp.is_send_sucess():
            # 点击聊天设置
            gcp.click_setting()
            time.sleep(2)
            # 滑到菜单底部
            gcs.scroll_to_bottom()
            # 点击“清空聊天记录”菜单
            gcs.click_clear_chat_record()
            # 点击确定按钮
            gcs.click_sure()
            # 返回上一级
            gcp.click_back()
            time.sleep(2)
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.点击gif图标
        gcp.click_gif()
        # 输入关键字搜索gif图片
        gcp.input_gif("2")
        # 等待gif图片页面加载
        gcp.wait_for_gif_ele_load()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # gcp.click_gif()
        # 点击发送
        gcp.send_gif()
        cwp = ChatWindowPage()
        # 2.检验发送失败的标识
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 重新连接网络
        gcp.set_network_status(6)
        # 点击重发
        gcp.click_send_again()
        # 3.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 10)

    @staticmethod
    def tearDown_test_msg_group_chat_total_quantity_0118():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)
