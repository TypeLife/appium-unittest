import unittest
import time
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages import *
from selenium.common.exceptions import TimeoutException

import re
import random
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile


REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}

class Preconditions(LoginPreconditions):
    """前置条件"""
    @staticmethod
    def enter_my_PC_chat_page(reset=False):
        """进入我的电脑会话页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 点击搜索我的电脑
        if mess.is_text_present('我的电脑'):
            mess.choose_chat_by_name('我的电脑')
        else:
            mess.click_search()
            SearchPage().input_search_keyword('我的电脑')
            mess.choose_chat_by_name('我的电脑')

    @staticmethod
    def make_sure_chatwindow_exist_file():
        """确保我的电脑页面有文件记录"""
        chat=ChatWindowPage()
        time.sleep(2)
        if chat.is_element_present_file():
            chat.wait_for_page_load()
        else:
            chat.click_more()
            ChatMorePage().click_file()
            csf = ChatSelectFilePage()
            csf.wait_for_page_load()
            csf.click_local_file()
            # 3、选择任意文件，点击发送按钮
            local_file = ChatSelectLocalFilePage()
            # 进入预置文件目录，选择文件发送
            local_file.push_preset_file()
            local_file.click_preset_file_dir()
            local_file.select_file('.txt')
            local_file.click_send()
            chat.wait_for_page_load()


class MsgMyPCChating(TestCase):
    """
    文件位置：全量/115 和飞信测试用例(分)-消息(4294).xlsx
    表格：我的电脑-文件
    author: 余梦思
    """

    def default_setUp(self):
        """确保每个用例运行前在我的电脑会话页面"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_my_PC_chat_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0253(self):
        """我的电脑预览文件页面,右上角显示更多选项"""
        #确保页面有.txt文件
        chat=ChatWindowPage()
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        #打开文件
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.page_contain_element_more()
        #返回聊天页面
        chat.click_back_in_open_file_page()

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0254(self):
        """我的电脑预览文件页面,点击更多"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(1)
        chat.page_should_contain_text('转发')
        chat.page_should_contain_text('收藏')
        chat.page_should_contain_text('其他应用打开')

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0256(self):
        """我的电脑预览文件页面,点击转发"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(1)
        chat.click_forward_Preview()
        #选择联系人
        scp = SelectContactsPage()
        scp.is_on_this_page()
        scp.click_phone_contact()
        scp.click_one_contact('给个红包1')
        scp.click_sure_forward()
        time.sleep(2)
        self.assertTrue(chat.is_toast_exist('已转发'))
        chat.page_contain_element_more()

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0257(self):
        """我的电脑预览文件页面,点击收藏"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(2)
        chat.click_collection_Preview()
        self.assertTrue(chat.is_toast_exist('已收藏'))
        chat.click_back_in_open_file_page()

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0258(self):
        """我的电脑预览文件页面,点击其他应用打开"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(2)
        chat.click_other_App_open()
        chat.page_should_contain_text('使用以下方式打开')

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0302(self):
        """断网,我的电脑预览文件页面,右上角显示更多选项"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        chat.set_network_status(0)
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.page_contain_element_more()
        #返回聊天页面
        chat.click_back_in_open_file_page()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0302():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)


    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0306(self):
        """断网 我的电脑预览文件页面,点击收藏"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        chat.set_network_status(0)
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(2)
        chat.click_collection_Preview()
        self.assertTrue(chat.is_toast_exist('已收藏'))
        chat.click_back_in_open_file_page()


    @tags('ALL', 'CMCC', 'DEBUG_1', 'my_PC')
    def test_msg_weifenglian_PC_0307(self):
        """断网 我的电脑预览文件页面,点击其他应用打开"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        chat.set_network_status(0)
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(2)
        chat.click_other_App_open()
        chat.page_should_contain_text('使用以下方式打开')

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0307():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0532(self):
        """放大发送表情文本"""
        #选择表情
        chat=ChatWindowPage()
        chat.open_expression()
        chat.select_expression(n=5)
        #放大发送表情
        time.sleep(1)
        chat.press_and_move_up('发送按钮')
        # 验证是否发送成功
        try:
            chat.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否放大,一个表情文本框信息正常宽度为107
        if not chat.get_width_of_msg_of_text() > 107:
            raise AssertionError("表情没有放大展示")
        chat.close_expression()
        chat.hide_keyboard()


    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0014(self):
        """我的电脑-本地照片发送"""
        #进入选择照片文件夹
        chat = ChatWindowPage()
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        #选择照片
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.jpg')
        local_file.click_send()
        chat.wait_for_msg_send_status_become_to('发送成功',10)
        #返回消息页面
        chat.click_back()
        time.sleep(2)
        MessagePage().page_should_contain_text('图片')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0028(self):
        """我的电脑-本地视频发送"""
        #进入选择视频文件夹
        chat = ChatWindowPage()
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        #选择视频
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp4')
        local_file.click_send()
        chat.wait_for_msg_send_status_become_to('发送成功',10)
        #返回消息页面
        chat.click_back()
        time.sleep(2)
        MessagePage().page_should_contain_text('视频')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0042(self):
        """我的电脑-本地音乐发送"""
        #进入选择音乐文件夹
        chat = ChatWindowPage()
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        #选择音乐
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp3')
        local_file.click_send()
        chat.wait_for_msg_send_status_become_to('发送成功',10)
        #返回消息页面
        chat.click_back()
        time.sleep(2)
        MessagePage().page_should_contain_text('文件')













