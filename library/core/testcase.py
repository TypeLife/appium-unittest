import unittest

from library.core.report.result import DefaultTestResult


class TestCase(unittest.TestCase):
    """Login 模块"""

    # def moduleSetUp(self):
    #     pass
    #
    # def moduleTearDown(self):
    #     pass

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
        # self.moduleSetUp()
        setup = getattr(self, "setUp_{}".format(self._testMethodName), self.default_setUp)
        setup()

    def tearDown(self):
        tear_down = getattr(self, "setUp_{}".format(self._testMethodName), self.default_tearDown)
        tear_down()
        # self.moduleTearDown()

    def run(self, result=None):
        if result is None:
            result = DefaultTestResult(verbosity=2)
        super().run(result)


if __name__ == '__main__':
    unittest.main()
