import unittest


class TestCase(unittest.TestCase):
    """Login 模块"""

    def default_tearDown(self):
        """
        如果没有定义 tearDown_[用例方法名]
        的方法时，默认执行的tearDown方法
        """
        pass

    def default_setUp(self):
        """
        如果没有定义 setUp_[用例方法名]
        的方法时，默认执行的tearDown方法
        """
        pass

    def setUp(self):
        setup = getattr(self, "setUp_{}".format(self._testMethodName), self.default_setUp)
        setup()

    def tearDown(self):
        tear_down = getattr(self, "tearDown_{}".format(self._testMethodName), self.default_tearDown)
        tear_down()


if __name__ == '__main__':
    unittest.main()
