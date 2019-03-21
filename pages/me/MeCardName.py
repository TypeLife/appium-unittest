from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from selenium.common.exceptions import TimeoutException


class MeCardNamePage(BasePage):
    """我-》分享名片-》卡片"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatListMergaActivity'

    __locators = {'': (MobileBy.ID, ''),

                  '意见反馈': (MobileBy.XPATH, "//*[contains(@text, '意见反馈')]"),
                  '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/cancle_img'),
                  '个人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_card_img'),
                  '卡名': (MobileBy.ID, 'com.chinasofti.rcs:id/name_tv'),
                  '卡号码': (MobileBy.ID, 'com.chinasofti.rcs:id/phone_tv'),
                  '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/company_tv'),
                  '公司选框': (MobileBy.ID, 'com.chinasofti.rcs:id/company_image'),
                  '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/position_tv'),
                  '职位选框': (MobileBy.ID, 'com.chinasofti.rcs:id/position_image'),
                  '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/email_tv'),
                  '邮箱选框': (MobileBy.ID, 'com.chinasofti.rcs:id/email_image'),
                  '发送名片': (MobileBy.ID, 'com.chinasofti.rcs:id/send_tv'),
                  # 打开编辑图片
                  '编辑图片': (MobileBy.ID, 'com.chinasofti.rcs:id/change_photo'),
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待卡片页面弹框加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发送名片"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_el_text(self, locator):
        """点击字段选项 """
        self.click_element(self.__locators[locator])

    @TestLogger.log()
    def check_select_box(self, locator):
        """检查勾选框是否已勾选 """
        return self.get_coordinate_color_of_element(self.__locators[locator], 10, 10, by_percent=True)

    @TestLogger.log('获取名片信息')
    def get_name_cards_info(self):
        info = dict()
        info['name'] = self.get_text(self.__locators['卡名'])
        info['tel'] = self.get_text(self.__locators['卡号码'])
        info['company'] = self.get_text(self.__locators['公司'])
        info['position'] = self.get_text(self.__locators['职位'])
        info['email'] = self.get_text(self.__locators['邮箱'])
        return info
