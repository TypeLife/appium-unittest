from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from selenium.common.exceptions import TimeoutException


class MeViewUserProfilePage(BasePage):
    """我-》查看个人资料"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.UserProfileShowActivity'

    __locators = {'': (MobileBy.ID, ''),
                  '菜单区域': (MobileBy.CLASS_NAME, 'android.widget.ScrollView'),
                  '意见反馈': (MobileBy.XPATH, "//*[contains(@text, '意见反馈')]"),
                  '网上营业厅': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar_title_tv'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/proflie_edit'),
                  '姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_name'),
                  '电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_phone_number'),
                  '个人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo'),
                  '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_school'),
                  '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profession'),
                  '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_email'),
                  '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card'),
                  # 打开编辑图片
                  '编辑图片': (MobileBy.ID, 'com.chinasofti.rcs:id/change_photo'),
                  }

    @TestLogger.log("下一页")
    def page_down(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'up')

    @TestLogger.log("上一页")
    def page_up(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'down')

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待聊天语音页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["电话"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_text_exist(self, text):
        """当前页面是否包含此文本"""
        return self.is_text_present(text)

    @TestLogger.log()
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__locators[text])

    @TestLogger.log()
    def click_back1(self):
        """点击返回按钮"""
        self.click_element(self.__locators['返回'])

    @TestLogger.log()
    def click_edit(self):
        """点击编辑按钮"""
        self.click_element(self.__locators['编辑'])

    @TestLogger.log()
    def element_contain_text(self, locator, expected):
        """该元素是否包含文本"""
        self.element_should_contain_text(self.__locators[locator], expected, "该元素不是此文本")

    @TestLogger.log()
    def click_share_card(self):
        """点击分享名片"""
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log('获取名片信息')
    def get_name_cards_info(self):
        info = dict()
        info['name'] = self.get_text(self.__locators['姓名'])
        info['tel'] = self.get_text(self.__locators['电话'])
        info['company'] = self.get_text(self.__locators['公司'])
        info['position'] = self.get_text(self.__locators['职位'])
        info['email'] = self.get_text(self.__locators['邮箱'])
        return info
