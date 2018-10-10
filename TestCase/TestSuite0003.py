import unittest

from library import config, keywords


class C0003(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('[SetupClass]')
        desired_caps = config.GlobalConfig.get_desired_caps()
        url = config.GlobalConfig.get_server_url()
        keywords.Android.open_app(url, desired_caps)
        print('[SetupClass OK]')

    @classmethod
    def tearDownClass(cls):
        keywords.Android.closed_current_driver()

    def setUp(self):
        print('[SetUp]')
        self.assertTrue(keywords.current_driver().is_app_installed('com.chinasofti.rcs'))
        keywords.GuidePage.jump_over_the_guide_page()
        keywords.PermissionListPage.accept_all_permission_in_list()
        keywords.Login.wait_for_one_key_login_page_load()
        print('[SetUp OK]')

    def tearDown(self):
        pass

    def test_cmcc_account_login(self):
        """
        移动账号登录
        :return:
        """
        print('[Test Start]')
        keywords.Login.wait_for_one_key_login_page_load()
        keywords.Login.click_one_key_login()
        keywords.MessagePage.wait_for_message_page_load()
        print('[Test OK]')
