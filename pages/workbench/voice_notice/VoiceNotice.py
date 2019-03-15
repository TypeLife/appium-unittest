from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class VoiceNoticePage(BasePage):
    """语音通知页面/超级会议页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        # 语音通知页面
        '语音通知标题': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '？': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_right1'),
        'X': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '创建语音通知': (MobileBy.XPATH, '//*[@text="创建语音通知"]'),
        '我创建的': (MobileBy.XPATH, '//*[@text="我创建的"]'),
        '我接受的': (MobileBy.XPATH, '//*[@text="我接受的"]'),
        # 打开语音通知使用指引页面
        '语音通知使用指导': (MobileBy.XPATH, '//*[@text="语音通知使用指导"]'),
        '发起语音通知': (MobileBy.XPATH, '//*[@text="发起语音通知"]'),
        '接听通知': (MobileBy.XPATH,  "//*[contains(@text,'3、接听通知')]"),
        '查看通知详情': (MobileBy.XPATH, '//*[@text="查看通知详情"]'),
        # 超级会议页面
        '超级会议': (MobileBy.XPATH, '//*[@text="超级会议"]'),
        '会场管理': (MobileBy.XPATH, "//*[contains(@text,'4、会场管理')]"),
    }

    @TestLogger.log()
    def wait_for_page_loads(self, text, timeout=60):
        """等待 语音通知页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present(text),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_enter_more(self):
        """点击进入工作台"""
        self.click_element(self.__class__.__locators['？'])

    @TestLogger.log()
    def click_close_more(self):
        """点击进入工作台"""
        self.click_element(self.__class__.__locators['X'])

    def swipe_half_page_up(self):
        """向上滑动半页"""
        self.swipe_by_percent_on_screen(50, 80, 50, 30, 800)

    def swipe_half_page_down(self):
        """向下滑动半页"""
        self.swipe_by_percent_on_screen(50, 30, 50, 80, 800)

    def find_els_h5(self, location):
        """查找元素"""
        els = self.get_elements(self.__locators[location])
        if len(els) > 0:
            return True
        else:
            raise AssertionError("该页面没有定位到该元素")



