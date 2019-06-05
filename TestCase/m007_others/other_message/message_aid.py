import os
import random
import time
import unittest
from pages.components import ChatNoticeDialog, ContactsSelector
from appium.webdriver.common.mobileby import MobileBy

import preconditions
from dataproviders import contact2
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from settings import PROJECT_PATH


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

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
        group_name = "aatest" + phone_number[-4:]
        return group_name


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0130():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0130(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="撤回"]'))
        get_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_sys_msg" and @text="你撤回了一条信息"]'))
        self.assertTrue(len(get_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0131():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0131(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        exist = page.is_toast_exist('已收藏')
        self.assertTrue(exist)
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_message_page()
        me_page.click_collection()
        collection_elements = me_page.get_elements((MobileBy.XPATH,
                                                    '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        self.assertTrue(len(collection_elements))

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0133():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0133(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()
        group_chat_name = Preconditions.get_group_chat_name()
        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后确认
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        page.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0134():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0134(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()
        group_chat_name = Preconditions.get_group_chat_name()
        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后确认  没有企业群
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        page.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0202():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0202(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="502173dc7656b4e634efd455ad48ac23.mp4"]'))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="502173dc7656b4e634efd455ad48ac23.mp4"]'))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        exist = page.is_toast_exist('已收藏')
        self.assertTrue(exist)
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_me_page()
        me_page.page_down()
        me_page.click_collection()
        collection_elements = me_page.get_elements((MobileBy.XPATH,
                                                    '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="502173dc7656b4e634efd455ad48ac23.mp4"]'))
        self.assertTrue(len(collection_elements))
        me_page.click_element((MobileBy.XPATH,
                               '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="502173dc7656b4e634efd455ad48ac23.mp4"]'))
        self.assertTrue(me_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/favorite_title')) == '详情')

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0203():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0203(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '轻快-胡伟立-28618718.mp3';
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找到 文件目录
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 找到元素
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_me_page()
        me_page.wait_for_page_load()
        me_page.page_down()
        me_page.click_collection()
        collection_elements = me_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        while len(collection_elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/rv_favorite'), 'up')
            time.sleep(1)
            collection_elements = me_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        self.assertTrue(len(collection_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0204():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0204(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '大型测试图片.jpg';
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找到 文件目录
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 找到元素
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/imageview_msg_image" and @index="1"]'))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_me_page()
        me_page.wait_for_page_load()
        me_page.page_down()
        me_page.click_collection()
        time.sleep(2)
        collection_elements = me_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/favorite_image" and @index="0"]'))
        while len(collection_elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/rv_favorite'), 'up')
            time.sleep(1)
            collection_elements = me_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/favorite_image" and @index="0"]'))
        self.assertTrue(len(collection_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0205():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0205(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '测试doc文件.doc';
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找到 文件目录
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 找到元素
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_me_page()
        me_page.wait_for_page_load()
        me_page.page_down()
        me_page.click_collection()
        time.sleep(2)
        collection_elements = me_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        while len(collection_elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/rv_favorite'), 'up')
            time.sleep(1)
            collection_elements = me_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        self.assertTrue(len(collection_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0206():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0206(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = 'ppt测试文件.ppt';
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找到 文件目录
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 找到元素
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_me_page()
        me_page.wait_for_page_load()
        me_page.page_down()
        me_page.click_collection()
        time.sleep(2)
        collection_elements = me_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        while len(collection_elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/rv_favorite'), 'up')
            time.sleep(1)
            collection_elements = me_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        self.assertTrue(len(collection_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0207():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0207(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '测试xls文件.xls';
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找到 文件目录
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 找到元素
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_me_page()
        me_page.wait_for_page_load()
        me_page.page_down()
        me_page.click_collection()
        time.sleep(2)
        collection_elements = me_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        while len(collection_elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/rv_favorite'), 'up')
            time.sleep(1)
            collection_elements = me_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        self.assertTrue(len(collection_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0208():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0208(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '文档pdf.pdf'
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找到 文件目录
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 找到元素
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        page.press(file_elements[0])
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_me_page()
        me_page.wait_for_page_load()
        me_page.page_down()
        me_page.click_collection()
        time.sleep(2)
        collection_elements = me_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        while len(collection_elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/rv_favorite'), 'up')
            time.sleep(1)
            collection_elements = me_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/file_name" and @text="%s"]' % file_name))
        self.assertTrue(len(collection_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0226():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0226(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '文档pdf.pdf'
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找到 文件目录
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 找到元素
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))

        file_size_text = page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/textview_select_file_size'))
        self.assertTrue('已选' in file_size_text)
        attribute = page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'), 'enabled')

        self.assertTrue('true' == attribute)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0228():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0228(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '文档pdf.pdf'
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找到 文件目录
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 找到元素
        time.sleep(2)
        elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        while len(elements) == 0:
            page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        proess_elements = page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/progress_send_small"]'))
        if len(proess_elements) == 0:
            proess_elements = page.get_elements(
                (MobileBy.XPATH,
                 '//*[@resource-id="com.chinasofti.rcs:id/img_message_down_file"]'))
        self.assertTrue(len(proess_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0362():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0362(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '文档pdf.pdf'
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0369():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0369(self):
        """将自己发送的位置转发到群"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements) > 0)
        group_chat_name = Preconditions.get_group_chat_name()
        page.press(addr_elements[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后取消
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/btn_cancel" and @text="取消"]'))

        # 点击群名称  然后确认
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        page.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0370():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0370(self):
        """将自己发送的位置转发到群"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '文档pdf.pdf'
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements) > 0)
        group_chat_name = Preconditions.get_group_chat_name()
        page.press(addr_elements[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后取消 todo 企业群
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_cancel" and @text="取消"]'))

        # 点击群名称  然后确认
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        page.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0336():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0336(self):
        """将自己发送的位置转发到个人联系人"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '文档pdf.pdf'
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements) > 0)
        group_chat_name = Preconditions.get_group_chat_name()
        page.press(addr_elements[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后取消 todo 企业群
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/btn_cancel" and @text="取消"]'))

        # 点击群名称  然后确认
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))

        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        page.press(addr_elements[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        contact_page = SelectContactPage()
        contact_page.input_search_key('admin')
        contact_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        contact_page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        contact_page.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0369():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0369(self):
        """将自己发送的位置转发到个人联系人"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '文档pdf.pdf'
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements) > 0)
        group_chat_name = Preconditions.get_group_chat_name()
        page.press(addr_elements[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后取消 todo 企业群
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/btn_cancel" and @text="取消"]'))

        # 点击群名称  然后确认
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))

        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        page.press(addr_elements[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        contact_page = SelectContactPage()
        contact_page.input_search_key('我的电脑')
        contact_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="我的电脑"]'))
        contact_page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        contact_page.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0370():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0370(self):
        """将自己发送的位置转发到个人联系人"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '文档pdf.pdf'
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_new_message()

        page = SelectContactsPage()
        page.input_search_contact_message('admin')
        page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="admin"]'))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements) > 0)
        group_chat_name = Preconditions.get_group_chat_name()
        page.press(addr_elements[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后取消 todo 企业群
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/btn_cancel" and @text="取消"]'))

        # 点击群名称  然后确认
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))

        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        page.press(addr_elements[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        contact_page = SelectContactPage()
        elements = contact_page.get_elements((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_rl"]'))
        elements[0].click()
        contact_page.click_element((MobileBy.XPATH,
                            '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        contact_page.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0373():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0373(self):
        """将自己发送的位置转发到个人联系人"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_group_chat()

        group_chat_name = Preconditions.get_group_chat_name()
        page = SelectContactsPage()
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后取消 todo 企业群
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements) > 0)
        addr_elements_pre = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        page.press(addr_elements_pre[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))
        time.sleep(1)
        addr_elements_suf = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements_suf) == (len(addr_elements_pre) - 1))

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0374():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0374(self):
        """将自己发送的位置转发到个人联系人"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_group_chat()

        group_chat_name = Preconditions.get_group_chat_name()
        page = SelectContactsPage()
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后取消 todo 企业群
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements) > 0)
        addr_elements_pre = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        page.press(addr_elements_pre[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="撤回"]'))
        time.sleep(1)
        addr_elements_suf = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        self.assertTrue(len(addr_elements_suf) == (len(addr_elements_pre) - 1))

    @staticmethod
    def setUp_test_msg_weifenglian_qun_0375():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_qun_0375(self):
        """将自己发送的位置转发到个人联系人"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        messpage = MessagePage()
        messpage.click_add_icon()
        messpage.click_group_chat()

        group_chat_name = Preconditions.get_group_chat_name()
        page = SelectContactsPage()
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
        # 点击群名称  然后取消 todo 企业群
        page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="位置"]'))
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn" and @text="发送"]'))
        time.sleep(2)
        addr_elements_pre = page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/lloc_famous_address_text"]'))
        page.press(addr_elements_pre[0])
        page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        page.is_toast_exist('已收藏')

        addr__text = addr_elements_pre[0].text
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'))
        me_page = MePage()
        me_page.open_me_page()
        me_page.page_down()
        me_page.click_collection()
        time.sleep(2)
        collection_elements = me_page.get_elements((MobileBy.XPATH,
                                                    '//*[@resource-id="com.chinasofti.rcs:id/favorite_tv_content"]'))
        flag = False
        for element in collection_elements:
            if addr__text in element.text:
                flag = True
                break
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_msg_xiaoliping_B_0007():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_have_a_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_B_0007(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        message_page.open_message_page()
        element = message_page.get_element((MobileBy.XPATH,
                                           '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="admin"]'))
        message_page.press(element)
        message_page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除聊天"]'))
        elements = message_page.get_elements((MobileBy.XPATH,
                                            '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="admin"]'))
        self.assertTrue(len(elements) == 0)

    @staticmethod
    def setUp_test_msg_xiaoliping_B_0008():
        Preconditions.select_mobile('Android-移动')
        contact2.push_resource_dir_to_mobile_sdcard(Preconditions.select_mobile('Android-移动'))
        Preconditions.make_already_have_a_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_B_0008(self):
        """进入免费/发送短信--选择联系人页面"""

        time.sleep(5)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0191():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0191(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="测试一个删除"]')):
            single.input_text_message("测试一个删除")
            single.send_text()
        single.press_mess("测试一个删除")
        single.click_multiple_selection()
        time.sleep(2)
        group_chat = GroupChatPage()
        # 勾选消息时校验页面元素
        self.assertTrue(group_chat.is_exist_multiple_selection_back())
        mess.page_should_contain_text('已选择')
        self.assertTrue(group_chat.is_exist_multiple_selection_count())
        self.assertTrue(group_chat.is_enabled_multiple_selection_delete())
        self.assertTrue(group_chat.is_enabled_multiple_selection_forward())
        group_chat.click_multiple_selection_delete()
        group_chat.click_multiple_selection_delete_sure()
        mess.is_toast_exist('删除成功')
        mess.page_should_not_contain_text('测试一个删除')


    @staticmethod
    def setUp_test_msg_huangcaizui_A_0212():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0212(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        single.input_text_message("测试一个删除1")
        single.send_text()
        single.input_text_message("测试一个删除2")
        single.send_text()
        single.press_mess("测试一个删除1")
        single.click_multiple_selection()
        time.sleep(2)
        group_chat = GroupChatPage()
        # 勾选消息时校验页面元素
        self.assertTrue(group_chat.is_exist_multiple_selection_back())
        mess.page_should_contain_text('已选择')
        self.assertTrue(group_chat.is_exist_multiple_selection_count())
        self.assertTrue(group_chat.is_enabled_multiple_selection_delete())
        self.assertTrue(group_chat.is_enabled_multiple_selection_forward())
        group_chat.get_check_all_not_selected()
        group_chat.click_multiple_selection_delete()
        group_chat.click_multiple_selection_delete_sure()
        mess.is_toast_exist('删除成功')
        mess.page_should_not_contain_text('测试一个删除1')
        mess.page_should_not_contain_text('测试一个删除2')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0260():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0260(self):
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        self.assertTrue(me.is_on_this_page())
        me.click_setting_menu()
        message_notice_set = MessageNoticeSettingPage()
        me.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/default_SMS_app'))
        message_notice_set.assert_menu_item_has_been_turn_on('消息送达状态显示')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0261():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0261(self):
        # 打开‘我’页面
        me = MePage()
        mess = MessagePage()
        me.open_me_page()
        self.assertTrue(me.is_on_this_page())
        me.click_setting_menu()
        message_notice_set = MessageNoticeSettingPage()
        me.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/default_SMS_app'))
        message_notice_set.turn_off('消息送达状态显示')
        message_notice_set.click_back()
        message_notice_set.click_back()
        me.open_message_page()
        if me.is_text_present('给个红包1'):
            mess.delete_message_record_by_name("给个红包1")
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        single.input_text_message("测试一个呵呵")
        single.send_text()
        mess.page_should_not_contain_text('已送达')
        mess.page_should_not_contain_text('已转为短信送达')
        mess.page_should_not_contain_text('对方离线')
        mess.page_should_not_contain_text('已提醒')
        single.click_back()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'))
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))

        me.open_me_page()
        me.is_on_this_page()
        me.click_setting_menu()
        message_notice_set = MessageNoticeSettingPage()
        me.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/default_SMS_app'))
        message_notice_set.turn_on('消息送达状态显示')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0273():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0273(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        single.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0274():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0274(self):
        single = SingleChatPage()
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        mess.click_new_message()
        select_page = SelectContactsPage()
        mess.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'))
        mess.page_should_contain_element((MobileBy.XPATH,"//*[@text='选择团队联系人']"))
        select_page.select_one_contact_by_name('给个红包1')

        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0275():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0275(self):
        single = SingleChatPage()
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()

        select_page = SelectContactsPage()
        mess.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'))
        mess.page_should_contain_element((MobileBy.XPATH,"//*[@text='选择团队联系人']"))
        select_page.select_one_contact_by_name('给个红包1')
        chatdialog = ChatNoticeDialog()
        # 判断存在？标志
        chatdialog.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'))
        # 判断存在退出短信按钮
        chatdialog.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_exitsms'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0289():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0289(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        mess.click_element((MobileBy.XPATH, '//*[@text="名片"]'))
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="给个名片2"]'))
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        mess.click_element((MobileBy.XPATH, '//*[@text="给个名片2"]'))
        GroupChatSetSeeMembersPage().wait_for_profile_page_load()
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        MessagePage().is_on_this_page()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0354():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0354(self):
        contactspage = ContactsPage()
        contactspage.click_search_box()
        contactspage.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/edit_query01'),'给个红包1')
        contactspage.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="给个红包1"]'))
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        MessagePage().is_on_this_page()

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0021():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0021(self):
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        singe_chat = SingleChatPage()
        chatdialog = ChatNoticeDialog()
        singe_chat.input_sms_message("测试前一半")
        # 点击退出短信按钮
        chatdialog.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_exitsms'))
        # 点击短信按钮
        singe_chat.click_sms()
        # 判断是否有之前输入的内容
        chatdialog.page_should_contain_element((MobileBy.XPATH, '//*[@text ="测试前一半"]'))
        singe_chat.edit_clear("测试前一半")

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0022():
        # 启动App
        Preconditions.select_mobile('Android-移动', reset=True)
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0022(self):
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        mess.click_element((MobileBy.XPATH, '//*[@text ="给个红包1"]'))
        singe_chat = SingleChatPage()
        chatdialog = ChatNoticeDialog()
        singe_chat.input_sms_message("发送第一条")
        # 点击发送短信
        singe_chat.send_sms()
        # 判断弹出资费提醒提示框
        chatdialog.page_should_contain_element((MobileBy.XPATH, '//*[@text ="资费提醒"]'))
        # 点击发送
        chatdialog.click_element((MobileBy.XPATH, '//*[@text ="发送"]'))
        singe_chat.input_sms_message("发送第二条")
        # 点击发送短信
        singe_chat.send_sms()
        # 判断未弹出资费提醒提示框
        chatdialog.page_should_not_contain_element((MobileBy.XPATH, '//*[@text ="资费提醒"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0025():
        # 启动App
        Preconditions.select_mobile('Android-移动',reset=True)
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0025(self):
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="测试一个呵呵"]')):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        # 长按通过短信发送
        single.send_for_sms('测试一个呵呵')
        # 判断控件存在
        single.is_present_sms_fee_remind()
        single.is_exist_send_button()
        single.is_exist_cancel_button()
        # 点击取消按钮
        single.click_cancel()
        # 再次发送
        single.send_for_sms('测试一个呵呵')
        single.is_present_sms_fee_remind()
        single.click_send_button()
        single.page_should_contain_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message" and @text="测试一个呵呵"]'))
        single.page_should_contain_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_sms_mark" and @text="短信"]'))
        single.send_for_sms('测试一个呵呵')
        single.page_should_not_contain_element((MobileBy.XPATH, '//*[@text="资费提醒"]'))
        single.page_should_contain_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message" and @text="测试一个呵呵"]'))
        single.page_should_contain_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_sms_mark" and @text="短信"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0062():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0062(self):
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        select_page = SelectContactsPage()
        select_page.search('给个红包1')
        time.sleep(2)
        mess.page_should_contain_text('手机联系人')
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('13800138000')
        mess.page_should_contain_text('搜索团队联系人 : 给个红包1')

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0063():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('给个红包1', '13800138000')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0063(self):
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        select_page = SelectContactsPage()
        # 按姓名搜索存在联系人
        select_page.search('给个红包1')
        time.sleep(1)
        mess.page_should_contain_text('手机联系人')
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('13800138000')
        mess.page_should_contain_text('搜索团队联系人 : 给个红包1')
        # 按手机号搜索存在联系人
        select_page.search('13800138000')
        time.sleep(1)
        mess.page_should_contain_text('手机联系人')
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('13800138000')
        mess.page_should_contain_text('搜索团队联系人 : 13800138000')
        # 按手机号搜索不存在联系人
        select_page.search('199815')
        time.sleep(1)
        mess.page_should_not_contain_text('手机联系人')
        mess.page_should_contain_text('搜索团队联系人 : 199815')
        # 无手机联系人且搜索手机号时
        select_page.search('19981512581')
        time.sleep(1)
        mess.page_should_contain_text('网络搜索')
        mess.page_should_contain_text('搜索团队联系人 : 19981512581')
        select_page.is_present_unknown_member()
        # 搜索我的电脑
        select_page.search('我的电脑')
        time.sleep(1)
        mess.page_should_not_contain_text('手机联系人')
        mess.page_should_contain_text('搜索团队联系人 : 我的电脑')

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0004():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0004(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("我的电脑")
        # 选择联系人进入联系人页
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="我的电脑"]'))
        mess.click_back()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        mess.is_on_this_page()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0002():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0002(self):
        mess = MessagePage()
        mess.click_search()
        time.sleep(2)
        self.assertTrue(current_mobile().is_keyboard_shown())
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/result_wrapper'))
        self.assertFalse(current_mobile().is_keyboard_shown())

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0029():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0029(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("我的电脑")
        # 选择联系人进入联系人页
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 点击进入我的电脑
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="我的电脑"]'))
        # 检查是否进入我的电脑页面
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/title" and @text="我的电脑"]'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0186():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人数据
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0186(self):
        """群二维码详情页——保存二维码"""
        # 1、网络正常（4G / WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主 / 群成员
        mess = MessagePage()
        # 预置群数据
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 1、进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        # Step 2、等待群聊页面加载
        groupchat.wait_for_page_load()
        # Step 3、进入群聊设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 4、点击下载群二维码
        groupset.click_QRCode()
        groupset.click_qecode_download_button()
        # Checkpoint 弹出toast提示：已保存
        mess.is_toast_exist("已保存")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0188():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人数据
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0188(self):
        """群聊设置页面——进入到群管理详情页"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        # 5、当前群人数为：1
        # 6、android端
        mess = MessagePage()
        # 预置群数据
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchatset  = GroupChatSetManagerPage()
        # Step 等待群聊页面加载
        groupchat.wait_for_page_load()
        # Step 进入群聊设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 点击群管理，进入到群管理详情页
        groupset.click_group_manage()
        groupset.wait_for_group_manage_load()
        # Step 点击群主管理权转让
        groupchatset.click_group_transfer()
        # Checkpoint 弹出toast提示：暂无群成员并且停留在当前页
        mess.is_toast_exist("暂无群成员")
        self.assertTrue(groupchatset.is_on_groupSetManager_contacts_page())
        # Step 点击左上角的返回按钮
        groupchatset.click_back()
        # Checkpoint 可以返回到群聊设置页
        groupset.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0197():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0197(self):
        """群聊设置页面——查找聊天内容——数字搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        # Step 如果当前页面不存在消息，发送一条消息
        SingleChatPage().send_text_if_not_exist("111")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字搜索条件
        search.search('111')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('111')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0198():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0198(self):
        """群聊设置页面——查找聊天内容——英文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        # Step 如果当前页面不存在消息，发送一条消息
        SingleChatPage().send_text_if_not_exist("AAA")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入英文字母搜索条件
        search.search('AAA')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('AAA')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0199():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0199(self):
        """群聊设置页面——查找聊天内容——特殊字符搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        # Step 如果当前页面不存在消息，发送一条消息
        SingleChatPage().send_text_if_not_exist("!@#$%")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入英文字母搜索条件
        search.search('!@#$%')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('!@#$%')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0201():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0201(self):
        """群聊设置页面，查找聊天内容——空格搜索"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        # Step 如果当前页面不存在消息，发送一条消息
        SingleChatPage().send_text_if_not_exist("呵呵  呵呵")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入空格搜索条件
        search.search(' ')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('呵呵  呵呵')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0203():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0203(self):
        """群聊设置页面——查找聊天内容——数字+汉字+英文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        # Step 如果当前页面不存在消息，发送一条消息
        SingleChatPage().send_text_if_not_exist("呵呵111AAA")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字+汉字+英文作为搜索条件
        search.search('呵呵111AAA')
        # Checkpoint 存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('呵呵111AAA')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0204():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0204(self):
        """群聊设置页面——查找聊天内容——数字+汉字+英文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字+汉字+英文作为搜索条件
        search.search('呵呵22BB')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0205():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0205(self):
        """群聊设置页面——查找聊天内容——中文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字+汉字+英文作为搜索条件
        search.search('吉吉娃')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0206():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0206(self):
        """群聊设置页面——查找聊天内容——数字搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入数字作为搜索条件
        search.search('112233')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0179():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        # Step 构造最近聊天人
        # 点击消息页搜索
        mess = MessagePage()
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("测试短信1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('测试短信1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        single.input_text_message("测试一个呵呵")
        single.send_text()
        single.click_back()
        CallContactDetailPage().click_back()
        SearchPage().click_back()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0179(self):
        """分享群二维码到——选择最近聊天"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主/群成员
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_group_avatars()
        # Step 点击左下角的分享按钮
        groupset.click_qecode_share_button()
        # Checkpoint 跳转到联系人选择器页面
        ContactsSelector().wait_for_contacts_selector_page_load()
        # Step 点击选择最近聊天的联系人
        ContactsPage().select_people_by_name("测试短信1")
        # Checkpoint 弹出确认弹窗,Step 点击取消
        SingleChatPage().click_cancel()
        # Checkpoint 关闭弹窗
        ContactsPage().select_people_by_name("测试短信1")
        # Step 点击确定
        SingleChatPage().click_sure()
        # Checkpoint 返回到群二维码分享页面并弹出toast提示：已转发
        mess.is_toast_exist("已转发")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0195():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0195(self):
        """群聊设置页面——查找聊天内容"""
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        # 如果当前页面不存在消息，发送一条消息
        single = SingleChatPage()
        if not single.is_text_present('测试一个呵呵'):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 点击聊天内容入口
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        # Checkpoint 可以跳转到聊天内容页面
        search.wait_for_page_load()
        # Checkpoint 调起小键盘
        self.assertTrue(current_mobile().is_keyboard_shown())
        # Step 点击顶部的搜索框
        search.search('测试一个呵呵')
        search.click_search_result('测试一个呵呵')
        groupchat.is_on_this_page()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0196():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0196(self):
        """群聊设置页面——查找聊天内容——中文搜索——搜索结果展示"""
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在文本消息
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        # 如果当前页面不存在消息，发送一条消息
        single = SingleChatPage()
        if not single.is_text_present('测试一个呵呵'):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        self.assertTrue(current_mobile().is_keyboard_shown())
        # Step 在查找聊天内容页面，输入框中，输入中文搜索条件
        search.search('测试一个呵呵')
        # Checkpoint 搜索结果是否展示为：发送人头像、发送人名称、发送的内容、发送的时间
        search.check_search_result()
        # Step 任意选中一条聊天记录
        search.click_search_result('测试一个呵呵')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0163():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0163(self):
        """群主——清除旧名片——录入29个字母（不区分大、小写）"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        # Step 群名片编辑页面，清除旧名片后，录入29个字母
        groupset.clear_group_name()
        # Checkpoint 可以正常录入29个字母
        groupset.input_new_group_name("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        # Step 录入成功，点击右上角的完成按钮
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        # Checkpoint 可以完成保存操作
        groupset.check_group_nickname('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0164():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0164(self):
        """群主——清除旧名片——录入30个字母（不区分大、小写）"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        # Step 群名片编辑页面，清除旧名片后，录入30个字母
        groupset.clear_group_name()
        # Checkpoint 可以正常录入30个字母
        groupset.input_new_group_name("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        # Step 录入成功，点击右上角的完成按钮
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        # Checkpoint 可以完成保存操作
        groupset.check_group_nickname('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
