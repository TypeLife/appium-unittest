import random
import re
import time
import unittest
import uuid

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.groupset.GroupChatSetPicVideo import GroupChatSetPicVideoPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage

from preconditions.BasePreconditions import WorkbenchPreconditions

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


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

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
        else:
            try:
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()

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
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if sog.is_element_exit("群聊名"):
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            return
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        sog.click_back()
        time.sleep(2)
        sc.click_back()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
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
            sogp.click_one_contact(group_name)
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
            n += 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def if_exists_multiple_enterprises_enter_group_chat(types):
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入群聊转发图片/视频"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            gcp = GroupChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            gcp.wait_for_page_load()
            gcp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            group_name = "群聊1"
            Preconditions.get_into_group_chat_page(group_name)
            # 转发图片/视频
            if types == "pic":
                gcp.forward_pic()
            elif types == "video":
                gcp.forward_video()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)
            time.sleep(2)

    @staticmethod
    def make_already_delete_my_group():
        """确保删掉所有群"""
        # 消息页面
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
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群删除，无群返回
        if len(group_names) == 0:
            sog.click_back()
            pass
        else:
            for group_name in group_names:
                sog.select_one_group_by_name(group_name)
                gcp = GroupChatPage()
                gcp.wait_for_page_load()
                gcp.click_setting()
                gcs = GroupChatSetPage()
                gcs.wait_for_page_load()
                gcs.click_delete_and_exit()
                # gcs.click_sure()
                mess.click_add_icon()
                mess.click_group_chat()
                sc.wait_for_page_load()
                sc.click_select_one_group()
            sog.click_back()
            # if not gcs.is_toast_exist("已退出群聊"):
            #     raise AssertionError("无退出群聊提示")
        # sc.click_back()
        # mess.open_me_page()

    @staticmethod
    def delete_record_group_chat():
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # if not gcsp.is_toast_exist("聊天记录清除成功"):
            #     raise AssertionError("没有聊天记录清除成功弹窗")
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            if not scp.is_on_this_page():
                raise AssertionError("没有返回到群聊页面")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    #多人群聊前置条件
    @staticmethod
    def select_one_mobile(moible_param):
        """选择指定的设备连接，并确保在消息列表页面"""
        Preconditions.select_mobile(moible_param)
        # 消息页面
        Preconditions.make_in_message_page(moible_param,reset=False)

    @staticmethod
    def make_in_message_page(moible_param,reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile(moible_param, reset)
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
    def build_one_new_group_with_number(puhone_number,group_name):
        """新建一个指定成员和名称的群，如果已存在，不建群"""
        # 消息页面
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
        # group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if sog.is_element_exit("群聊名"):
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            return True
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        time.sleep(2)
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        #添加指定电话成员
        time.sleep(2)
        sc.input_search_keyword(puhone_number)
        time.sleep(2)
        sog.click_text("tel")
        time.sleep(2)
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
        return False

    @staticmethod
    def get_group_chat_name_double():
        """获取多人群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "多机" + phone_number[-4:]
        return group_name

    @staticmethod
    def go_to_group_double(group_name):
        """从消息列表进入双机群聊，前提：已经存在双机群聊"""
        mess = MessagePage()
        mess.wait_for_page_load()
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
        # # 群名
        # group_name = Preconditions.get_group_chat_name_double()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if not sog.is_element_exit("群聊名"):
            raise AssertionError("没有找到双机群聊，请确认是否创建")
        sog.click_element_("群聊名")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def change_mobile(moible_param):
        """转换设备连接并且确保在消息列表页面"""
        Preconditions.select_mobile(moible_param)
        current_mobile().hide_keyboard_if_display()
        current_mobile().launch_app()
        Preconditions.make_in_message_page(moible_param)


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
    #             Preconditions.make_already_in_message_page()
    #             conts.open_contacts_page()
    #             try:
    #                 if conts.is_text_present("发现SIM卡联系人"):
    #                     conts.click_text("显示")
    #             except:
    #                 pass
    #             for name, number in required_contacts:
    #                 conts.create_contacts_if_not_exits(name, number)
    #             # 创建群
    #             required_group_chats = dataproviders.get_preset_group_chats()
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0001(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0002(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0003(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0004(self):
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
        # self.assertEqual(gcp.is_send_sucess(), True)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0005(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0006(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0007(self):
        """群聊会话页面，编辑图片不保存发送"""
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
        # self.assertEqual(gcp.is_send_sucess(), True)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0008(self):
        """群聊会话页面，编辑图片中途直接发送"""
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
        # self.assertEqual(gcp.is_send_sucess(), True)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0009(self):
        """群聊会话页面，编辑图片保存"""
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
        # self.assertEqual(gcp.is_send_sucess(), True)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0010(self):
        """群聊会话页面，取消编辑图片"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0011(self):
        """群聊会话页面，取消编辑图片，点击发送按钮"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0012(self):
        """群聊会话页面，发送相册内的图片 """
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0013(self):
        """群聊会话页面，预览已选中的图片，隐藏编辑按钮"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0014(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0015(self):
        """群聊会话页面，勾选超9张相册内图片发送"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0016(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0017(self):
        """群聊会话页面，使用拍照功能并发送照片"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0018(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0019(self):
        """群聊会话页面，使用拍照功能拍照之后编辑并保存"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0020(self):
        """群聊会话页面，使用拍照功能拍照编辑图片，再取消编辑并发送"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0022(self):
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
    def test_msg_xiaoliping_D_0026(self):
        """群聊会话页面，转发他人发送的图片给手机联系人"""
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
    def test_msg_xiaoliping_D_0032(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0060(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0062(self):
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
    def test_msg_xiaoliping_D_0069(self):
        """群聊会话页面，转发自己发送的视频给手机联系人"""
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
    def test_msg_xiaoliping_D_0066(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0079(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0081(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0082(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0083(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0084(self):
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0085(self):
        """群聊会话页面，同时发送相册内视频和图片"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk', 'high')
    def test_msg_xiaoliping_D_0086(self):
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
    def test_msg_xiaoliping_D_0110(self):
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
    def test_msg_xiaoliping_D_0111(self):
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
    def test_msg_xiaoliping_D_0112(self):
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
    def test_msg_xiaoliping_D_0113(self):
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
    def test_msg_xiaoliping_D_0114(self):
        """在群聊会话窗，搜索特殊字符关键字发送趣图"""
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
    def test_msg_xiaoliping_D_0115(self):
        """在群聊会话窗，搜索无结果的趣图"""
        # 1.检验是否在当前聊天会话页
        gcp = GroupChatPage()
        gcp.is_on_this_page()
        # 2.点击gif图片
        gcp.click_gif()
        gcp.wait_for_gif_ele_load()
        gcp.input_gif("3")
        self.assertEquals(gcp.is_gif_exist_toast(), True)
        gcp.click_cancel_gif()
        gcp.edit_clear("3")

    @unittest.skip("断网后gif图片无法加载")
    def test_msg_xiaoliping_D_0118(self):
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
    def test_msg_xiaoliping_D_0119(self):
        """在群聊会话窗，关闭GIF搜索框"""
        Preconditions.enter_group_chat_page()
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
    def test_msg_xiaoliping_D_0140(self):
        """转发聊天内容中的已下载的图片（缩略图）"""
        # # 1.检验是否当前聊天会话页面且有图片
        # Preconditions.make_already_have_my_picture()
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证转发的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
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
        gcv.wait_for_page_load()
        gcv.click_back()
        gcf.wait_for_page_load()
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk')
    def test_msg_xiaoliping_D_0141(self):
        """转发聊天内容中的已下载的图片（放大图）"""
        # # 1.检验是否当前聊天会话页面且有图片
        # Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证转发的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
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
    def test_msg_xiaoliping_D_0142(self):
        """转发聊天内容中的已下载的图片给任意对象"""
        # # 1.检验是否当前聊天会话页面且有图片
        # Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证转发的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
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
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        scp.click_one_contact("大佬2")
        scp.click_sure_forward()
        self.assertEquals(gcv.is_toast_exist_zf(), True)
        # 6.点击返回到群聊页面//6.2.9版本有改动
        gcv.wait_for_page_load()
        gcv.click_back()
        gcf.wait_for_page_load()
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()
        gcp.wait_for_page_load()
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # gcp.click_element([MobileBy.XPATH, "//*[contains(@resource-id,'back')]"], 15)
        # sog = SelectOneGroupPage()
        # sog.click_back()
        # sct = SelectContactsPage()
        # gcp.click_back()
        scp.click_one_contact("大佬2")
        time.sleep(2)
        if gcp.is_exist_dialog():
            gcp.click_i_have_read()
        self.assertEquals(gcp.is_exist_msg_image(), True)
        gcp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_xiaoliping_D_0145(self):
        """转发聊天内容中的已下载的视频（缩略图）"""
        # # 1.检验是否当前聊天会话页面且有视频
        # Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一个视频,保证转发的为视频
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        cpg.click_send()
        time.sleep(5)
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
        time.sleep(1)
        if gcv._is_element_present(["id", 'com.chinasofti.rcs:id/title']):
            gcv.click_back()
        gcf.wait_for_page_load()
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_xiaoliping_D_0146(self):
        """转发聊天内容中的已下载的视频（放大图）"""
        # # 1.检验是否当前聊天会话页面且有视频
        # Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一个视频,保证转发的为视频
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        cpg.click_send()
        time.sleep(5)
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
        time.sleep(1)
        gcv.click_close_pre_video()
        time.sleep(1)
        if gcv._is_element_present(["id", 'com.chinasofti.rcs:id/title']):
            gcv.click_back()
        time.sleep(1)
        gcf.wait_for_page_load()
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_xiaoliping_D_0147(self):
        """转发聊天内容中的已下载的视频给任意对象"""
        # # 1.检验是否当前聊天会话页面且有视频
        # Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一个视频,保证转发的为视频
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        cpg.click_send()
        time.sleep(5)
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
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        scp.click_one_contact("大佬3")
        scp.click_sure_forward()
        self.assertEquals(gcv.is_toast_exist_zf(), True)
        # 6.点击返回到群聊页面
        time.sleep(1)
        if gcv._is_element_present(["id", 'com.chinasofti.rcs:id/title']):
            gcv.click_back()
        gcf.wait_for_page_load()
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()
        gcp.wait_for_page_load()
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # sog = SelectOneGroupPage()
        # sog.click_back()
        # sct = SelectContactsPage()
        # sct.click_back()
        scp.click_one_contact("大佬3")
        time.sleep(2)
        if gcp.is_exist_dialog():
            gcp.click_i_have_read()
        self.assertEquals(gcp.is_exist_msg_videos(), True)
        time.sleep(1)
        gcp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_xiaoliping_D_0149(self):
        """收藏聊天内容中的已下载的图片"""
        # # 1.检验是否当前聊天会话页面且有图片
        # Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证收藏的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
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
        gcv.wait_for_page_load()
        gcv.click_back()
        gcf.wait_for_page_load()
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()
        gcp.wait_for_page_load()
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
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
    def test_msg_xiaoliping_D_0150(self):
        """删除聊天内容中的图片"""
        # # 1.检验是否当前聊天会话页面且有图片
        # Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证删除的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
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
        gcv.wait_for_page_load()
        gcv.click_back()
        gcf.wait_for_page_load()
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()
        # self.assertEquals(gcp.is_exist_msg_image(), False)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_xiaoliping_D_0151(self):
        """保存聊天内容中的图片到本地"""
        # # 1.检验是否当前聊天会话页面且有图片
        # Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证保存的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
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
    def test_msg_xiaoliping_D_0152(self):
        """保存聊天内容中的视频到本地"""
        # # 1.检验是否当前聊天会话页面且有视频
        # Preconditions.make_already_have_my_videos()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一个视频,保证保存的为视频
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        cpg.click_send()
        time.sleep(5)
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
        gcf.wait_for_page_load()
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'debug_fk1')
    def test_msg_xiaoliping_D_0153(self):
        """编辑聊天内容中的图片，并发送"""
        # # 1.检验是否当前聊天会话页面且有图片
        # Preconditions.make_already_have_my_picture()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,保证编辑的为图片
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
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

    @tags('ALL', 'CMCC', 'message114', 'debug_fk1', 'high')
    def test_msg_xiaoqiu_0413(self):
        """群主在群设置页面——点击群名称——修改群名称"""
        # 1.检验是否当前聊天会话页面,点击进入群设置页面
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gsp = GroupChatSetPage()
        gsp.wait_for_page_load()
        # 2.点击群名称，修改群名
        gsp.click_modify_group_name()
        names = str(uuid.uuid1())
        group_name = "a" + names[-4:]
        gsp.input_new_group_name(group_name)
        gsp.save_group_name()
        self.assertEquals(gsp.is_toast_exist("修改成功"), True)
        gsp.wait_for_page_load()
        # 3.返回群聊主页
        gsp.click_back()
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("群名称已修改为 " + group_name)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0413():
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gsp = GroupChatSetPage()
        gsp.wait_for_page_load()
        # 2.点击群名称，修改群名
        gsp.click_modify_group_name()
        group_name = Preconditions.get_group_chat_name()
        gsp.input_new_group_name(group_name)
        gsp.save_group_name()
        gsp.wait_for_page_load()
        gsp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'message114', 'debug_fk1', 'high')
    def test_msg_xiaoqiu_0414(self):
        """群主在设置页面——点击群管理——点击解散群按钮"""
        # 1.检验是否当前聊天会话页面,点击进入群设置页面
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gsp = GroupChatSetPage()
        gsp.wait_for_page_load()
        # 2.点击群管理，解散群
        gsp.click_group_manage()
        gsp.click_group_manage_disband_button()
        gsp.click_sure()
        # 3.返回群聊主页
        mess = MessagePage()
        mess.wait_for_page_load()
        gcp.page_should_contain_text("系统消息")
        gcp.page_should_contain_text("该群已解散")

    @tags('ALL', 'CMCC', 'message114', 'debug_fk1', 'high')
    def test_msg_xiaoqiu_0416(self):
        """群成员在群设置页面——点击删除并退出按钮后"""
        # 1.检验是否当前聊天会话页面,点击进入群设置页面
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gsp = GroupChatSetPage()
        gsp.wait_for_page_load()
        # 2.点击删除并退出
        gsp.click_delete_and_exit()
        # gsp.click_sure()
        # 3.返回消息页，提示你已退出群
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_text("系统消息")
        time.sleep(3)
        mess.page_should_contain_text("你已退出群")

    @tags('ALL', 'CMCC', 'message114', 'debug_fk1', 'high')
    def test_msg_xiaoqiu_0421(self):
        """群主或群成员在设置页面——点击+邀请群成员后"""
        # 1.检验是否当前聊天会话页面,点击进入群设置页面
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gsp = GroupChatSetPage()
        gsp.wait_for_page_load()
        # 2.点击点击+邀请群成员后
        gsp.click_add_number()
        slc = SelectLocalContactsPage()
        group_name = "和飞信电话"
        slc.swipe_select_one_member_by_name(group_name)
        slc.click_sure()
        # 3.返回消息页，提示你已退出群
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("你向 " + group_name + "... 发出群邀请")

    @tags('ALL', 'CMCC', 'message114', 'debug_fk1', 'high')
    def test_msg_xiaoqiu_0422(self):
        """群主点击消息列表右上角的+点击发起群聊/点对点建群/点击通讯录-群聊右上角/通话记录-一键建群按钮，创建群后"""
        # 1.检验是否当前聊天会话页面,点击进入群设置页面
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # gcp.click_back()
        # Preconditions.make_already_delete_my_group()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_delete_and_exit()
        mess = MessagePage()
        mess.wait_for_page_load()
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
        mess.click_add_icon()
        mess.click_group_chat()
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
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("发出群邀请")

    @tags('ALL', 'CMCC', 'message114', 'debug_fk1', 'high')
    def test_msg_xiaoqiu_0534(self):
        """创建一个普通群"""
        # 1.检验是否当前聊天会话页面,点击进入群设置页面
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # gcp.click_back()
        # Preconditions.make_already_delete_my_group()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_delete_and_exit()
        mess = MessagePage()
        mess.wait_for_page_load()
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
        mess.click_add_icon()
        mess.click_group_chat()
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
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("发出群邀请")

    @unittest.skip("用例不稳定，跳过")
    def test_msg_xiaoqiu_0535(self):
        """创建10个普通群"""
        # 1.检验是否当前聊天会话页面,点击进入群设置页面
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_back()
        # Preconditions.make_already_delete_my_group()
        for i in range(10):
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_add_icon()
            # 点击 发起群聊
            mess.click_group_chat()
            # 选择联系人界面，选择一个群
            sc = SelectContactsPage()
            # 群名
            group_name = Preconditions.get_group_chat_name() + "% d" % i
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
                    sc.page_up()
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
            gcp.wait_for_page_load()
            gcp.click_back()

    # @tags('ALL', 'CMCC', 'message114', 'debug_fk1', 'high')
    @unittest.skip("用例重复，跳过")
    def test_msg_xiaoqiu_0548(self):
        """普通群，分享群聊邀请口令"""
        # 1. 普通群，分享群聊邀请口令
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gsp = GroupChatSetPage()
        gsp.wait_for_page_load()
        # 2. 分享群聊邀请口令
        gsp.click_text("邀请微信或QQ好友进群")
        # 3.验证是否有生成口令的加载框
        gsp.page_should_contain_text("生成口令")
        # 4.验证是否群口令分享弹窗
        gsp.wait_for_share_group_load()
        gsp.page_should_contain_text("分享群口令邀请好友进群")
        gsp.page_should_contain_text("下次再说")
        # 5.点击下次再说，进入群聊设置页面
        gsp.click_text("下次再说")
        gsp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'message114', 'debug_fk1', 'high')
    def test_msg_xiaoqiu_0548(self):
        """普通群，分享群聊邀请口令"""
        # 1. 普通群，分享群聊邀请口令
        Preconditions.enter_group_chat_page()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gsp = GroupChatSetPage()
        gsp.wait_for_page_load()
        # 2. 分享群聊邀请口令
        gsp.click_text("邀请微信或QQ好友进群")
        # 3.验证是否有生成口令的加载框（loading状态验证暂时跳过）
        # gsp.page_should_contain_text("生成口令")
        # 4.验证是否群口令分享弹窗
        gsp.wait_for_share_group_load()
        gsp.page_should_contain_text("分享群口令邀请好友进群")
        gsp.page_should_contain_text("下次再说")
        # 5.点击下次再说，进入群聊设置页面
        gsp.click_text("下次再说")
        gsp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0024():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_D_0024(self):
        """群聊会话页面，转发他人发送的图片到当前会话窗口时失败"""
        # 1、在当前聊天会话页面，长按他人发送的图片
        # 2、点击转发
        # 3、在最近聊天中选择当前会话窗
        # 4、点击发送按钮
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
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
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        gcp.wait_for_page_load()
        gcp.click_element_("消息图片")
        time.sleep(3)
        gcp.set_network_status(0)
        time.sleep(8)
        gcp.press_xy()
        gcp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text(group_name)
        time.sleep(2)
        gcp.click_element_("确定移除")
        if not gcp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        try:
            cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
        Preconditions.delete_record_group_chat()

    def tearDown_test_msg_xiaoliping_D_0024(self):
        # 重新连接网络
        scp = GroupChatPage()
        scp.set_network_status(6)
        time.sleep(6)
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0025():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_D_0025(self):
        """群聊会话页面，转发他人发送的图片到当前会话窗口时取消转发"""
        # 1、在当前聊天会话页面，长按他人发送的图片
        # 2、点击转发
        # 3、在最近聊天中选择当前会话窗
        # 4、点击发送按钮
        # 5、点击弹窗取消按钮
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
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
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        gcp.wait_for_page_load()
        gcp.click_element_("消息图片")
        time.sleep(2)
        gcp.press_xy()
        gcp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text(group_name)
        time.sleep(2)
        gcp.click_element_("取消移除")
        sc.wait_for_page_load()
        current_mobile().back()
        current_mobile().back()
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0026():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_D_0026(self):
        """群聊会话页面，转发他人发送的图片给手机联系人"""
        # 1、在当前聊天会话页面，长按他人发送的图片
        # 2、点击转发
        # 3、选择任意手机联系人
        # 4、点击发送按钮
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
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
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        gcp.wait_for_page_load()
        gcp.click_element_("消息图片")
        time.sleep(2)
        gcp.press_xy()
        gcp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.click_one_contact("飞信电话")
        time.sleep(2)
        gcp.click_element_("确定移除")
        if not gcp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        self.assertTrue(mess.is_text_present("飞信电话"))
        mess.click_element_by_text("飞信电话")
        chat = SingleChatPage()
        time.sleep(2)
        if gcp.is_text_present("1元/条"):
            chat.click_i_have_read()
        chat.wait_for_page_load()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(2)
        # 最后删除消息记录，返回消息页面结束用例
        gcp.press_element_("消息图片",3000)
        gcp.click_text("删除")
        time.sleep(2)
        chat.click_back()

    @staticmethod
    def setUp_test_msg_xiaoliping_D_0027():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_D_0027(self):
        """群聊会话页面，转发他人发送的图片到手机联系人时失败"""
        # 1、在当前聊天会话页面，长按他人发送的图片
        # 2、点击转发
        # 3、选择任意手机联系人
        # 4、点击发送按钮
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
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
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        gcp.wait_for_page_load()
        gcp.click_element_("消息图片")
        time.sleep(3)
        gcp.set_network_status(0)
        time.sleep(8)
        gcp.press_xy()
        gcp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.click_one_contact("飞信电话")
        time.sleep(2)
        gcp.click_element_("确定移除")
        if not gcp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        self.assertTrue(mess.is_text_present("飞信电话"))
        mess.click_element_by_text("飞信电话")
        chat = SingleChatPage()
        time.sleep(2)
        if gcp.is_text_present("1元/条"):
            chat.click_i_have_read()
        chat.wait_for_page_load()
        try:
            cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送失败'.format(10))
        time.sleep(2)
        # 最后删除消息记录，返回消息页面结束用例
        gcp.press_element_("消息图片", 3000)
        gcp.click_text("删除")
        time.sleep(2)
        chat.click_back()

    def tearDown_test_msg_xiaoliping_D_0027(self):
        # 重新连接网络
        scp = GroupChatPage()
        scp.set_network_status(6)
        time.sleep(6)

class MsgGroupChatVideoPicAllTest(TestCase):
    """
    模块：群聊-图片视频-GIF
    文件位置：1.1.3全量测试用例->113全量用例--肖立平.xlsx
    表格：群聊-图片视频-GIF
    Author:刘晓东
    """

    @classmethod
    def setUpClass(cls):

        Preconditions.select_mobile('Android-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        # 确保有企业群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 5:
            try:
                Preconditions.make_already_in_message_page()
                Preconditions.ensure_have_enterprise_group()
                flag3 = True
            except:
                fail_time3 += 1
            if flag3:
                break

        # 确保测试手机有resource文件夹
        name = "群聊1"
        Preconditions.get_into_group_chat_page(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        csfp.wait_for_page_load()
        csfp.click_local_file()
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
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page(name)

    def default_tearDown(self):
        pass
        # Preconditions.make_already_in_message_page()
        # cdp = ContactDetailsPage()
        # cdp.delete_all_contact()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0021(self):
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
        # 1.等待群聊页面加载
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0041(self):
        """群聊会话页面,转发自己发送的图片到当前会话窗口"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        time.sleep(2)
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        # 解决发送图片后，最近聊天窗口没有记录，需要退出刷新的问题
        gcp.click_back()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        time.sleep(2)
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(group_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0042(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时失败"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        time.sleep(2)
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
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
        scg.select_recent_chat_by_name(group_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0042():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0043(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时点击取消转发"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        time.sleep(2)
        gcp.click_picture()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        cpg.click_send()
        time.sleep(5)
        # 解决发送图片后，最近聊天窗口没有记录，需要退出刷新的问题
        gcp.click_back()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(group_name)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回群聊天页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0044(self):
        """群聊会话页面，转发自己发送的图片给手机联系人"""

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
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0045(self):
        """群聊会话页面，转发自己发送的图片到手机联系人时失败"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
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
        contact_name = "大佬1"
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(contact_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0045():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0046(self):
        """群聊会话页面，转发自己发送的图片到手机联系人时点击取消转发"""

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
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        # 返回群聊天页面
        slc.click_back()
        scg.wait_for_page_load()
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0047(self):
        """群聊会话页面，转发自己发送的图片给团队联系人"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_group_chat("pic")
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0048(self):
        """群聊会话页面，转发自己发送的图片到团队联系人时失败"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_group_chat("pic")
        contact_name = "大佬3"
        shc.selecting_he_contacts_by_name(contact_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0048():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0049(self):
        """群聊会话页面，转发自己发送的图片到团队联系人时点击取消转发"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
        # 1.长按自己发送的图片并转发
        gcp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_group_chat("pic")
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 返回群聊天页面
        shc.click_back()
        shc.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0050(self):
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
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的陌生联系人
        mp.choose_chat_by_name(number)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0051(self):
        """群聊会话页面，转发自己发送的图片到陌生人时失败"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
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
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0051():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0052(self):
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
    def test_msg_xiaoliping_D_0053(self):
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
        name = "群聊2"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0054(self):
        """群聊会话页面，转发自己发送的图片到普通群时失败"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
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
        name = "群聊2"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0054():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0055(self):
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
        name = "群聊2"
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
    def test_msg_xiaoliping_D_0056(self):
        """群聊会话页面，转发自己发送的图片到企业群"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
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
        # 3.选择一个企业群
        name = sog.select_one_enterprise_group()
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0057(self):
        """群聊会话页面，转发自己发送的图片到企业群时失败"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
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
        # 3.选择一个企业群
        sog.select_one_enterprise_group()
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0057():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0058(self):
        """群聊会话页面，转发自己发送的图片到企业群时点击取消转发"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 确保当前群聊页面已有图片
        Preconditions.make_already_have_my_picture()
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
        # 4.选择一个企业群
        sog.select_one_enterprise_group()
        # 取消转发
        sog.click_cancel_forward()
        # 5.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回群聊天页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0069(self):
        """群聊会话页面，转发自己发送的视频给手机联系人"""

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
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0070(self):
        """群聊会话页面，转发自己发送的视频给手机联系人时失败"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        time.sleep(5)
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
        contact_name = "大佬1"
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(contact_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0070():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0071(self):
        """群聊会话页面，转发自己发送的视频给手机联系人时点击取消转发"""

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
        # 3、4.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 取消转发
        scg.click_cancel_forward()
        # 5.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        # 返回群聊天页面
        slc.click_back()
        scg.wait_for_page_load()
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0072(self):
        """群聊会话页面，转发自己发送的视频给团队联系人"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_group_chat("video")
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0073(self):
        """群聊会话页面，转发自己发送的视频给团队联系人时失败"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_group_chat("video")
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待群聊页面加载
        self.assertEquals(gcp.is_exist_forward(), True)
        gcp.wait_for_page_load()
        # 返回到消息页
        gcp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0073():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0074(self):
        """群聊会话页面，转发自己发送的视频给团队联系人时点击取消转发"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        # 1.长按自己发送的视频并转发
        gcp.forward_video()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3、4.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_group_chat("video")
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 取消转发
        scg.click_cancel_forward()
        # 5.等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 返回群聊天页面
        shc.click_back()
        shc.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0075(self):
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
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        gcp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0076(self):
        """群聊会话页面，转发自己发送的视频给陌生人时失败"""

        gcp = GroupChatPage()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        gcp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        # 确保当前群聊页面已有视频
        Preconditions.make_already_have_my_videos()
        time.sleep(5)
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
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0076():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0077(self):
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

    @unittest.skip("断网后返回会话页面，趣图列表关闭，无法打开")
    def test_msg_xiaoliping_D_0118(self):
        """在群聊会话窗，趣图发送失败后出现重新发送按钮"""

        gcp = GroupChatPage()
        # 如果当前群聊页面已有消息发送失败标识，需要先清除聊天记录
        if not gcp.is_send_sucess():
            # 点击聊天设置
            gcp.click_setting()
            gcs = GroupChatSetPage()
            gcs.wait_for_page_load()
            # 点击清空聊天记录
            gcs.click_clear_chat_record()
            # 点击确定按钮
            gcs.click_sure()
            time.sleep(1)
            # 返回上一级
            gcp.click_back()
        # 等待群聊页面加载
        gcp.wait_for_page_load()
        # 1.点击gif图标
        gcp.click_gif()
        gcp.wait_for_gif_ele_load()
        # 输入关键字搜索gif图片
        gcp.input_gif("2")
        # 等待gif图片页面加载
        gcp.wait_for_gif_ele_load()
        # 设置手机网络断开
        gcp.set_network_status(0)
        # 点击发送
        gcp.send_gif()
        cwp = ChatWindowPage()
        # 2.检验发送失败的标识
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        # 重新连接网络
        gcp.set_network_status(6)
        # 点击重发
        gcp.click_send_again()
        # 3.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @staticmethod
    def tearDown_test_msg_xiaoliping_D_0118():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

