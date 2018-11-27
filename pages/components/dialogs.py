from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatNoticeDialog(BasePage):
    """用户须知提示框"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {
        '提示框': (MobileBy.ID, 'android:id/content'),
        '用户须知': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '须知内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
        '我已阅读': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_check'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_btn_ok')
    }

    @TestLogger.log('判断是否显示用户须知提示框')
    def is_tips_display(self, max_wait_time=3):
        try:
            self.wait_until(
                condition=lambda d: self.is_text_present('用户须知'),
                timeout=max_wait_time
            )
            return True
        except TimeoutException:
            return False

    @TestLogger.log('勾选用户须知后点击确定')
    def accept_and_close_tips_alert(self):
        self.select_checkbox(self.__locators['我已阅读'])
        self.click_element(self.__locators['确定'])

    @TestLogger.log('不勾选用户须知直接关闭提示框')
    def directly_close_tips_alert(self):
        self.unselect_checkbox(self.__locators['我已阅读'])
        alert_box = self.get_element(self.__locators['提示框'])
        position = (alert_box.location.get('x'), alert_box.location.get('y') - 100)
        print('tap position: {}'.format(position))
        self.mobile.tap([position])
