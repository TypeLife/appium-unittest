import unittest
from library.core.TestCase import TestCase


@unittest.skip
class ContactsTest(TestCase):
    """Contacts 模块"""

    def default_setUp(self):
        pass

    def default_tearDown(self):
        pass

    def test_something(self):
        """description"""
        self.assertEqual(True, True)

    def setUp_test_something(self):
        print("Run test case setup.")
