from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ScanPage(BasePage):
    """扫一扫"""
    ACTIVITY = 'cn.com.fetion.zxing.qrcode.activity.CaptureActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iab_back'),
        '扫一扫': (MobileBy.ID, 'com.chinasofti.rcs:id/iab_title'),
        'com.chinasofti.rcs:id/finderView': (MobileBy.ID, 'com.chinasofti.rcs:id/finderView'),
        'com.chinasofti.rcs:id/surfaceView': (MobileBy.ID, 'com.chinasofti.rcs:id/surfaceView'),
        'com.chinasofti.rcs:id/qrcode_scan_anim': (MobileBy.ID, 'com.chinasofti.rcs:id/qrcode_scan_anim'),
        '将二维码放入扫描框内,即可自动扫描': (MobileBy.ID, 'com.chinasofti.rcs:id/qrcode_warn_info'),
        '我的二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/my_qrcode'),
    }

    @TestLogger.log('进入我的二维码页面')
    def open_my_qr_code_page(self):
        self.click_element(self.__locators['我的二维码'])

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])
