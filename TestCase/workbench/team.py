import unittest
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags


class TeamTest(TestCase):
    """团队 模块"""

    def default_setUp(self):
        pass

    def default_tearDown(self):
        pass

    @tags('ALL', 'SMOKE')
    def test_something(self):
        """description"""
        self.assertEqual(True, True)