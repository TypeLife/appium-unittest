from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class Keyboard(BasePage):
    """用户须知提示框"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {
    }

    @TestLogger.log('如果键盘弹出，就收回键盘')
    def hide_keyboard_if_display(self):
        if self.mobile.is_keyboard_shown():
            self.hide_keyboard()

    @TestLogger.log("检查键盘是否弹出")
    def assert_keyboard_is_display(self, max_wait_time=3):
        try:
            self.wait_until(
                condition=lambda d: self.mobile.is_keyboard_shown(),
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('键盘没有弹出')

    @TestLogger.log("检查键盘是否弹出")
    def assert_keyboard_is_hided(self, max_wait_time=3):
        try:
            self.wait_until(
                condition=lambda d: not self.mobile.is_keyboard_shown(),
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('键盘没有收回')
