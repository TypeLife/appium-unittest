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


class DeleteConfirmDialog(BasePage):
    __locators = {
        '取消': (MobileBy.XPATH, '//*[@text="取消"]'),
        '删除': (MobileBy.XPATH, '//*[@text="刪除"]'),
    }

    @TestLogger.log('点击取消')
    def click_cancel(self):
        self.click_element(self.__locators['取消'])

    @TestLogger.log('点击删除')
    def click_delete(self):
        self.click_element(self.__locators['删除'])


class SuspendedTips(BasePage):
    """悬浮窗权限授权提示"""
    ACTIVITY = 'com.cmicc.module_call.ui.multipartycall.MultipartyCallActivity'

    __locators = {
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'android:id/parentPanel': (MobileBy.ID, 'android:id/parentPanel'),
        'android:id/contentPanel': (MobileBy.ID, 'android:id/contentPanel'),
        'android:id/scrollView': (MobileBy.ID, 'android:id/scrollView'),
        'android:id/textSpacerNoTitle': (MobileBy.ID, 'android:id/textSpacerNoTitle'),
        '您的手机没有授予悬浮窗权限，请开启后再试': (MobileBy.ID, 'android:id/message'),
        'android:id/buttonPanel': (MobileBy.ID, 'android:id/buttonPanel'),
        '暂不开启': (MobileBy.ID, 'android:id/button2'),
        '现在去开启': (MobileBy.ID, 'android:id/button1')
    }

    @TestLogger.log('暂不开启')
    def click_not_open_now(self):
        self.click_element(self.__locators['暂不开启'])

    @TestLogger.log('如果弹出“您的手机没有授予悬浮窗权限”提示框，点击暂不开启')
    def ignore_tips_if_tips_display(self):
        try:
            self.click_not_open_now()
        except:
            pass
