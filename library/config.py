from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

default_desired_capability = {
    "platformName": "Android",
    "platformVersion": "7.1",
    "deviceName": "f9213901",
    "automationName": "UiAutomator2",
    "newCommandTimeout": 600,
    "appPackage": "com.chinasofti.rcs",
    "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
    "notReset": True
}


class GlobalConfig:
    server_url = 'http://127.0.0.1:4723/wd/hub'
    desired_caps = {}

    # platformName = 'IOS'
    # platformVersion = '7'
    # app = 'http://dlrcs.fetion-portal.com/mobile/rcs_v6.2.3.0915_20180917.apk'
    # appPackage = 'com.chinasofti.rcs'
    # appActivity = 'com.cmcc.cmrcs.android.ui.activities.WelcomeActivity'
    # deviceName = 'f9213901'
    # automationName = 'UiAutomator2'
    # newCommandTimeout = 600

    @staticmethod
    def set_desired_caps(caps):
        GlobalConfig.desired_caps = caps

    @staticmethod
    def get_desired_caps():
        return GlobalConfig.desired_caps if GlobalConfig.desired_caps else default_desired_capability

    @staticmethod
    def set_server_url(url):
        GlobalConfig.server_url = url

    @staticmethod
    def get_server_url():
        return GlobalConfig.server_url

    @staticmethod
    def get_platform_name():
        return GlobalConfig.desired_caps['platformName'] if ("platformName" in GlobalConfig.desired_caps) else \
            default_desired_capability['platformName']


class DriverCache:
    current_driver = None
    drivers = {}

    @staticmethod
    def register_driver(driver, alis):
        if alis:
            DriverCache.drivers[alis] = driver
        else:
            raise Exception('alis name(: {} ) must a readable name!'.format(alis))

    @staticmethod
    def get_driver(alis):
        DriverCache.current_driver = DriverCache.drivers.get(alis)
        return DriverCache.current_driver

    @staticmethod
    def open_app(server, desired_caps, alis='Default'):
        driver = webdriver.Remote(server, desired_caps)
        # next_wait_time = 30
        # for i in range(5):
        #     try:
        #         e = WebDriverWait(driver, next_wait_time, 0.5).until(
        #             lambda d: d.find_element_by_android_uiautomator('new UiSelector().text("始终允许")'))
        #         e.click()
        #         next_wait_time = 1
        #     except:
        #         next_wait_time = 1
        DriverCache.current_driver = driver
        if alis in DriverCache.drivers.keys():
            raise Exception('Alis name(: {} ) has been registered'.format(alis))
        DriverCache.register_driver(driver, alis)
        return DriverCache.current_driver

    @staticmethod
    def close_current():
        DriverCache.current_driver.quit()
        DriverCache.current_driver = None

    @staticmethod
    def close_all():
        DriverCache.current_driver.close_app()
        for d in DriverCache.drivers.values():
            d.quit()
