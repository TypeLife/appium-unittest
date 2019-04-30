import os
import traceback
import unittest

# from pip._internal import main as install_requirements

# 自动安装依赖
module_list = os.popen('pip freeze').readlines()
with open('requirements.txt', 'r') as f:
    require_list = f.readlines()
    for require in require_list:
        if require not in module_list:
            os.system('pip install -r requirements.txt')
            break
# install_requirements(['install', '-r', 'requirements.txt'])

if __name__ == '__main__':
    os.environ.setdefault('AVAILABLE_DEVICES_SETTING', 'AVAILABLE_DEVICES')
    from library.core.utils import CommandLineTool

    cli_commands = CommandLineTool.parse_and_store_command_line_params()
    if cli_commands.deviceConfig:
        os.environ['AVAILABLE_DEVICES_SETTING'] = cli_commands.deviceConfig

    from library.core.utils import ConfigManager, common

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
    from library.HTMLTestRunner import HTMLTestRunner

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
