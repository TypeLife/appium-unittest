import os
import random
import time
import unittest

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

