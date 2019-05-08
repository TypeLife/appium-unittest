import time
import unittest
import preconditions
from pages.components import BaseChatPage
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
        Preconditions.make_already_in_message_page(reset=False)
        message = MessagePage()
        #未进入到我的电脑聊天界面,可以在搜索框搜索我的电脑进入,MessagePage里面有写好的方法.
        #进入我的电脑页面
        message.click_search()
        SearchPage().input_search_keyword('我的电脑')
        message.choose_chat_by_name('我的电脑')
        time.sleep()

class MsgAllPrior(TestCase):
    @staticmethod
    def test_result():
        Preconditions.select_mobile('Android-移动')
        message = MessagePage()
        chat = BaseChatPage()
        # message.input_search_message('我的电脑')
        message.look_detail_news_by_name("我的电脑")
        chat.open_file_in_chat_page("deviceid.txt")
        chat.wait_for_open_file()
        chat.page_contain_element_more()


