import unittest
from library.core.testcase import TestCase


class MessageTest(TestCase):
    """Message 模块"""

    def default_setUp(self):
        pass

    def default_tearDown(self):
        pass

    def test_something(self):
        """description"""
        self.assertEqual(True, False)

    def setUp_test_something(self):
        print("Run test case setup.")
