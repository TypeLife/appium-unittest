from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GuidePage(BasePage):
    """引导页"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.SplashActivity'

    __locators = {
        "Banner": (MobileBy.ID, 'com.chinasofti.rcs:id/splash_view_pager'),
    }

    @TestLogger.log()
    def is_on_the_first_guide_page(self):
        """判断当前页是否在引导页第一页"""
        flag = self.is_text_present("解锁“免费通信”新攻略")
        return flag

    @TestLogger.log()
    def swipe_to_the_second_banner(self):
        """从引导页第一屏左滑到第二屏"""
        try:

            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present("解锁“免费通信”新攻略")
            )
        except:
            raise AssertionError('页面没有包含文本：体验“畅聊沟通”新视界')
        self.swipe_by_direction(self.__class__.__locators['Banner'], 'left', 200)
        return self

    @TestLogger.log()
    def swipe_to_the_third_banner(self):
        """从引导页第二屏左滑到第三屏"""
        try:
            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present("体验“畅聊沟通”新视界")
            )
        except:
            raise AssertionError('页面没有包含文本：体验“畅聊沟通”新视界')
        self.swipe_by_direction(self.__class__.__locators['Banner'], 'left', 200)
        return self

    @TestLogger.log()
    def click_start_the_experience(self):
        """点击引导页第三屏的开始体验"""
        try:
            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present("开始体验")
            )
            self.click_text("开始体验", True)
            return self
        except:
            # raise AssertionError('页面没有包含文本：开始体验')
            self.click_start_the_experience_631()

    @TestLogger.log()
    def click_start_the_experience_631(self):
        """点击引导页第三屏的立即体验（6.3.1版本）"""
        try:
            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present("立即体验")
            )
        except:
            raise AssertionError('页面没有包含文本：立即体验')
        self.click_text("立即体验", True)
        return self

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待页面进入引导页第一页（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present('解锁“免费通信”新攻略')
            )
        except:
            message = "引导页首页在限定的时间：{}s内没有加载完毕，或者没有包含文本：解锁“免费通信”新攻略".format(timeout)
            raise AssertionError(
                message
            )
        return self
