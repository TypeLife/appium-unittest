import functools
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

    def _auto_click_permission_alert_wrapper(self, func):
        this = self

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if this.get_elements(('xpath', '//*[@text="允许" or @text="拒绝"]')).__len__() >= 2:
                need = True
                while need:
                    try:
                        alert = this.driver.switch_to.alert
                        alert.accept()
                        continue
                    except:
                        alert = this.get_elements(
                            [MobileBy.XPATH, '//android.widget.Button[@text="始终允许" or @text="允许"]'])
                        if alert:
                            alert[0].click()
                            continue
                    break
            return func(*args, **kwargs)

        return wrapper
