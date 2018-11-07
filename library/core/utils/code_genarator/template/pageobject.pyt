from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class %(PageName)sPage(BasePage):
    """%(PageDescription)s"""
    ACTIVITY = '%(Activity)s'

    __locators = %(Locator)s
