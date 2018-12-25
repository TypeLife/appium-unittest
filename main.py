import os
import unittest

from library.HTMLTestRunner import HTMLTestRunner
from library.core.utils import CommandLineTool, ConfigManager, common

if __name__ == '__main__':
    cli_commands = CommandLineTool.parse_and_store_command_line_params()
    report_path = ConfigManager.get_html_report_path()
    s = cli_commands.suite
    if cli_commands.suite:
        suite = None
        for p in cli_commands.suite:
            if os.path.isdir(p):
                s = unittest.defaultTestLoader.discover(os.path.abspath(p), '*.py')
            elif os.path.isfile(p):
                path, file = os.path.split(os.path.abspath(p))
                s = unittest.defaultTestLoader.discover(path, file)
            else:
                raise ValueError('Path "{}" is not an valid file path!'.format(p))
            if suite is None:
                suite = s
            else:
                suite.addTest(s)
    else:
        case_path = ConfigManager.get_test_case_root()
        suite = unittest.defaultTestLoader.discover(case_path, '*.py')
    # RunTest
    with common.open_or_create(report_path, 'wb') as output:
        runner = HTMLTestRunner(
            stream=output, title='Test Report', verbosity=2)
        runner.run(suite)
