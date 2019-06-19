from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class WebMsgLoad(BasePage):
    """打开的网页消息界面"""
    # ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.QRCodeActivity'

    __locators = {
        '百度一下': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        'com.chinasofti.rcs:id/btn_more': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_more'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar')

    }

    @TestLogger.log('等待加载完毕')
    def wait_for_loading_animation_end(self):
        self.mobile.wait_until(
            condition=lambda d: self.get_element(self.__locators['com.chinasofti.rcs:id/btn_more']),
            timeout=60
        )

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('更多')
    def click_more(self):
        self.click_element(self.__locators['com.chinasofti.rcs:id/btn_more'])

    @TestLogger.log()
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__locators[text])
