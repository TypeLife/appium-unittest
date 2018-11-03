import os
import datetime
from library.core.common.simcardtype import CardType
from library.core.common.supportedmodel import SupportedModel
from .available_devices import AVAILABLE_DEVICES

NOW = datetime.datetime.now()

# 项目根目录
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试用例目录
TEST_CASE_ROOT = os.path.join(PROJECT_PATH, 'TestCase')
# 测试报告目录
REPORT_PATH = os.path.join(PROJECT_PATH, 'report')
# 测试报告HTML文件
REPORT_HTML_PATH = os.path.join(REPORT_PATH, 'TestReport.html')
# 屏幕截图存储路径
SCREEN_SHOT_PATH = os.path.join(REPORT_PATH, 'screen-shot', NOW.date().__str__())
# log文件存放目录
LOG_FILE_PATH = os.path.join(REPORT_PATH, 'log')

# Appium 服务地址
APPIUM_SETTING = {
    "REMOTE_URL": "http://127.0.0.1:4723/wd/hub"
}
# Driver 默认的 desired_capabilities
DEFAULT_DESIRED_CAPABILITY = {
    "platformName": "Android",
    "platformVersion": "8.0",
    "deviceName": "test",
    "udid": 'bb5671d',
    "automationName": "UiAutomator2",
    "newCommandTimeout": 600,
    "appPackage": "com.chinasofti.rcs",
    "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
}
