import unittest

from library import config, keywords
from library.core.testcase import TestCase
from library.pages import *


class LoginTest(TestCase):
    """Login 模块"""

    @classmethod
    def tearDownClass(cls):
        keywords.Android.closed_current_driver()

    def default_setUp(self):
        pass

    def default_tearDown(self):
        pass

    def test_login_0001(self):
        """descript"""
        GuidePage().wait_for_page_load(20). \
            swipe_to_the_second_banner(). \
            swipe_to_the_third_banner(). \
            click_start_the_experience()

    def setUp_test_login_0001(self):
        if config.DriverCache.current_driver is None:
            keywords.Android.open_app()

    def tearDown_test_login_0001(self):
        # keywords.Android.closed_current_driver()
        pass


if __name__ == '__main__':
    unittest.main()
