from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class Scan1Page(BasePage):
    """网络异常扫一扫"""
    ACTIVITY = 'com.chinamobile.app.yuliao_common.baseActivity.LoadingActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/return_im'),
        '扫一扫': (MobileBy.ID, 'com.chinasofti.rcs:id/title_tv'),
        '无网络连接图片': (MobileBy.ID, 'com.chinasofti.rcs:id/img_fail'),
    }

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('检查网络异常视图是否显示')
    def assert_network_disconnect_img_is_display(self):
        try:
            self.wait_until(
                lambda d: self.get_element(self.__locators['无网络连接图片'])
            )
        except TimeoutException:
            raise AssertionError('没有找到表示网络异常的图例')
