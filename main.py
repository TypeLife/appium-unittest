import os
import sys
import unittest
import xmlrunner

from HTMLTestRunner import HTMLTestRunner
from library import utils

if __name__ == '__main__':
    utils.parse_and_store_command_line_params(sys.argv[1:])
    # Set test report file path
    root = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(root, 'report.html')
    # RunTest
    suite = unittest.defaultTestLoader.discover(root, 'TestSuite*.py')
    with open(report_path, 'wb') as report:
        # runner = xmlrunner.XMLTestRunner(output=report).run(suite)
        runner = HTMLTestRunner(stream=report, title='Test Report')
        runner.run(suite)
