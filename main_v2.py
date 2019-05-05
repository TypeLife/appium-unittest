import os
import traceback
import unittest
from library.core.utils import ConfigManager, common

module_list = os.popen('pip freeze').readlines()
with open('requirements.txt', 'r') as f:
    require_list = f.readlines()
    for require in require_list:
        if require not in module_list:
            os.system('pip install -r requirements.txt')
            break

def get_case(cli_commands):
    if cli_commands.suite:
        sui = unittest.TestSuite()
        for p in cli_commands.suite:
            path_list = [os.path.join(root, name) for root, dirs, files in os.walk(p) for name in files if os.path.join(root, name).endswith('.py') and not os.path.join(root, name).endswith('__init__.py')]
            print(path_list)
            for path in path_list:
                loader = unittest.TestLoader()
                print(path)
                path, file = os.path.split(os.path.abspath(path))
                s = loader.discover(path, file)
                sui.addTest(s)
    else:
        case_path = ConfigManager.get_test_case_root()
        sui = unittest.defaultTestLoader.discover(case_path, '*.py')
    return sui

def run():
    os.environ.setdefault('AVAILABLE_DEVICES_SETTING', 'AVAILABLE_DEVICES')
    from library.core.utils import CommandLineTool
    cli_commands = CommandLineTool.parse_and_store_command_line_params()
    if cli_commands.deviceConfig:
        os.environ['AVAILABLE_DEVICES_SETTING'] = cli_commands.deviceConfig
    suite = get_case(cli_commands)
    from library.HTMLTestRunner import HTMLTestRunner
    report_path = ConfigManager.get_html_report_path()
    with common.open_or_create(report_path, 'wb') as output:
        runner = HTMLTestRunner(
            stream=output, title='Test Report', verbosity=2)
        result = runner.run(suite)

        # 成功、失败、错误、总计、通过率
        try:
            count = str(result.success_count + result.failure_count + result.error_count)  # 总计
            pazz = str(result.success_count)  # 成功
            total_fail = str(result.failure_count + result.error_count)  # 失败
            if result.success_count + result.failure_count + result.error_count == 0:
                pazz_rate = '00.00%'
            else:
                rate = (result.success_count / (result.success_count + result.failure_count + result.error_count)) * 100
                pazz_rate = "%.2f%%" % rate
            from library.core.utils import send_report

            send_report.get_ui_automation_metric(count, pazz, total_fail, pazz_rate)
            if cli_commands.sendTo:
                send_report.send_mail(*cli_commands.sendTo)
        except:
            msg = traceback.format_exc()
            print(msg)
            print("报告Email发送失败")

if __name__ == '__main__':
    run()

