import os

# 项目根目录路径、测试报告目录路径、截图存储路径
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_CASE_ROOT = os.path.join(PROJECT_PATH, 'TestCase')
REPORT_PATH = os.path.join(PROJECT_PATH, 'report')
REPORT_HTML_PATH = os.path.join(REPORT_PATH, 'TestReport.html')
SCREEN_SHOT_PATH = os.path.join(REPORT_PATH, 'screen-shot')

# Appium 服务地址
APPIUM_SETTING = {
    "REMOTE_URL": "http://127.0.0.1:4723/wd/hub"
}
# Driver 默认的 desired_capabilities
DEFAULT_DESIRED_CAPABILITY = {
    "platformName": "Android",
    "platformVersion": "8.0",
    "deviceName": "192.168.200.103:5555",
    "automationName": "UiAutomator2",
    "newCommandTimeout": 600,
    "appPackage": "com.chinasofti.rcs",
    "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
}
