import os

# 项目根目录路径、测试报告目录路径、截图存储路径
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORT_PATH = os.path.join(PROJECT_PATH, 'report')
SCREEN_SHOT_PATH = os.path.join(REPORT_PATH, 'screen-shot')

# Appium 服务地址
APPIUM_SETTING = {
    "REMOTE_URL": "http://127.0.0.1:4723/wd/hub"
}
