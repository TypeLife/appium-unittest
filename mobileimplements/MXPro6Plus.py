from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait

from library.core.common.simcardtype import CardType
from library.core.mobile.mobiledriver import MobileDriver


class MXPro6Plus(MobileDriver):
    """魅族Pro 6 Plus"""

    def supported_card_types(self):
        return [
            CardType.CHINA_MOBILE,
            CardType.CHINA_UNION,
        ]

    def total_card_slot(self):
        return 2

    def wait_until(self, condition, timeout=8, auto_accept_permission_alert=True):
        this = self

        def execute_condition(driver):
            """如果有弹窗，自动允许"""

            def get_accept_permission_handler(d):
                """获取允许权限弹窗的方法句柄"""
                try:
                    alert = d.switch_to.alert
                    return alert.accept
                except:
                    alert = this.get_elements((MobileBy.XPATH, '//android.widget.Button[@text="始终允许" or @text="允许"]'))
                    if not alert:
                        return False
                    return alert[0].click

            if auto_accept_permission_alert:
                if this.get_elements(('xpath', '//*[@text="允许" or @text="拒绝"]')).__len__() >= 2:
                    need = True
                    while need:
                        try:
                            WebDriverWait(this.driver, 1).until(
                                get_accept_permission_handler
                            )()
                        except:
                            need = False
            return condition(driver)

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(execute_condition)
