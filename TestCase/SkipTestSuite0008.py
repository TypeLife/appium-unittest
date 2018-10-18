import unittest

from library import config, keywords
from library.preconditions import Preconditions


class C0008(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        keywords.Android.closed_current_driver()

    def setUp(self):
        Preconditions.open_and_login_app_using_on_key_login()

    def tearDown(self):
        pass

    def test_create_new_message(self):
        """新建消息"""
        keywords.MessagePage.click_add_button()
        keywords.MessagePage.click_new_message()
        keywords.SelectContactPage.wait_for_select_contact_page_load()

        keywords.SelectContactPage.input_contact_search_box("逵哥")
        name = keywords.SelectContactPage.get_concat_name_by_given_index(1)
        number = keywords.SelectContactPage.get_concat_number_by_given_index(1)
        keywords.SelectContactPage.select_contact_by_given_index(1)
        keywords.MessageDetailPage.wait_for_message_detail_page_load()
        keywords.MessageDetailPage.wait_for_user_remind_popup()
        keywords.MessageDetailPage.accept_remind_dialog_and_close_it()
        keywords.MessageDetailPage.input_message_and_send('1234567890 中文 English [呲牙1]')


        # 检查是否发送成功
        # keywords.MessageDetailPage
        # 检查标题
        keywords.MessageDetailPage.title_text_should_be(name)
