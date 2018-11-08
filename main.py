import sys
import unittest

from library.HTMLTestRunner import HTMLTestRunner
from library.core.utils import CommandLineTool, ConfigManager, common

if __name__ == '__main__':
    CommandLineTool.parse_and_store_command_line_params()
    report_path = ConfigManager.get_html_report_path()
    case_path = ConfigManager.get_test_case_root()
    # RunTest
    suite = unittest.defaultTestLoader.discover(case_path, '*.py')
    with common.open_or_create(report_path, 'wb') as output:
        runner = HTMLTestRunner(stream=output, title='Test Report')
        runner.run(suite)
