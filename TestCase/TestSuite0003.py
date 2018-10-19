import unittest

from library import config, keywords


class C0003(unittest.TestCase):
    """登录测试"""

    @classmethod
    def setUpClass(cls):
        """启动APP"""
        desired_caps = config.GlobalConfig.get_desired_caps()
        url = config.GlobalConfig.get_server_url()
        if not keywords.current_driver():
            keywords.Android.open_app(url, desired_caps)
        else:
            keywords.current_driver().launch_app()

    @classmethod
    def tearDownClass(cls):
        """关闭APP"""
        keywords.current_driver().close()
        # keywords.Android.closed_current_driver()
        pass

    def setUp(self):
        """跳转到引导页"""
        self.assertTrue(keywords.current_driver().is_app_installed('com.chinasofti.rcs'))
        keywords.GuidePage.jump_over_the_guide_page()
        keywords.PermissionListPage.accept_all_permission_in_list()
        keywords.Login.wait_for_one_key_login_page_load()

    def tearDown(self):
        pass

    def test_cmcc_account_login(self):
        """移动账号登录"""
        keywords.Login.wait_for_one_key_login_page_load()
        keywords.Login.click_one_key_login()
        keywords.MessagePage.wait_for_message_page_load()
