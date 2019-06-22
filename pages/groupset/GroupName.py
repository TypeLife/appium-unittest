from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupNamePage(BasePage):
    """群聊名称修改页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupNameActivity'

    __locators = {'': (MobileBy.ID, ''),
                  "返回": (MobileBy.ID, "com.chinasofti.rcs:id/back"),
                  "修改群聊名称": (MobileBy.ID, "com.chinasofti.rcs:id/change_name"),
                  "保存": (MobileBy.ID, "com.chinasofti.rcs:id/group_name_save"),
                  "群聊名称编辑框": (MobileBy.ID, "com.chinasofti.rcs:id/edit_query"),
                  "删除群聊名称": (MobileBy.ID, "com.chinasofti.rcs:id/iv_delect"),
                  "群聊名称输入框": (MobileBy.ID, "com.chinasofti.rcs:id/et_group_name"),
                  '删除': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_del'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
                  }

    @TestLogger.log()
    def input_group_name(self, group_name):
        """输入修改的群聊名称"""
        self.input_text(self.__class__.__locators["群聊名称编辑框"], group_name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_group_name_631(self, group_name):
        """输入修改的群聊名称"""
        self.input_text(self.__class__.__locators["群聊名称输入框"], group_name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def clear_input_group_name(self):
        """获取输入的群聊名称"""
        return self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        return self.click_element(self.__class__.__locators["确定"])


    @TestLogger.log()
    def del_group_name(self):
        """删除群聊名称"""
        el = self.get_element(self.__class__.__locators["群聊名称编辑框"])
        return el.text

    @TestLogger.log()
    def get_input_group_name(self):
        """获取输入的群聊名称"""
        el = self.get_element(self.__class__.__locators["群聊名称编辑框"])
        return el.text

    @TestLogger.log()
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])

    @TestLogger.log()
    def save_btn_is_enabled(self):
        """获取保存按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["保存"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_delete_group_name(self):
        """点击删除群聊名称"""
        self.click_element(self.__class__.__locators["删除群聊名称"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待修改群聊名称页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['群聊名称编辑框'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

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

    @TestLogger.log()
    def wait_for_page_load_631(self, timeout=8, auto_accept_alerts=True):
        """等待修改群聊名称页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['群聊名称输入框'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self