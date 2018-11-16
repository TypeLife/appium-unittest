from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetPage(BasePage):
    """群聊名称修改页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupNameActivity'

    __locators = {'': (MobileBy.ID, ''),
                  "修改群聊名称": (MobileBy.ID, "com.chinasofti.rcs:id/change_name"),
                  "保存": (MobileBy.ID, "com.chinasofti.rcs:id/group_name_save"),
                  "群聊名称编辑框": (MobileBy.ID, "com.chinasofti.rcs:id/edit_query"),
                  "删除群聊名称": (MobileBy.ID, "com.chinasofti.rcs:id/iv_delect"),
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
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])
