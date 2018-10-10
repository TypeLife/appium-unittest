import unittest

from library import config, keywords
from library.preconditions import Preconditions


class C0007(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        keywords.Android.closed_current_driver()

    def setUp(self):
        print('[SetUp]')
        Preconditions.open_and_login_app_using_on_key_login()
        print('[SetUp OK]')

    def tearDown(self):
        pass

    def test_control_add(self):
        """
        控件 “+”
        :return:
        """
        print('[Test Start]')
        keywords.MessagePage.click_add_button()
        keywords.MessagePage.wait_for_new_message_text_match('新建消息')
        keywords.MessagePage.wait_for_free_sms_text_match('免费短信')
        keywords.MessagePage.wait_for_initiate_group_chat_text_match('发起群聊')
        keywords.MessagePage.wait_for_grouping_mass_message_text_match('分组群发')
        keywords.MessagePage.wait_for_take_a_scan_text_match('扫一扫')
        print('[Test OK]')
