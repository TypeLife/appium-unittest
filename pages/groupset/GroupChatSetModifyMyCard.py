from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetModifyMyCardPage(BasePage):
    """修改群名片页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupCardActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '修改群名片': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/group_card_save'),
                  '我的群名片': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
                  '删除': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=3, auto_accept_alerts=True):
        """等待修改群名片页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["修改群名片"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def input_my_name(self, name):
        """"输入我的群名片"""
        self.input_text(self.__class__.__locators["我的群名片"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])

    @TestLogger.log()
    def save_btn_is_enabled(self):
        """保存按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["保存"])

    @TestLogger.log()
    def click_delete_my_name(self):
        """点击删除我的群名片"""
        self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def wait_for_modify_ok_tips_load(self, timeout=8, auto_accept_alerts=True):
        """等待 修改成功 提示加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_toast_exist("修改成功", timeout)
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self
