from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SingleChatSetPage(BasePage):
    """单聊设置页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.OneToOneSettingActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '聊天设置': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/iv_setting_avatar': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_setting_avatar'),
                  'com.chinasofti.rcs:id/ivCreateGroup': (MobileBy.ID, 'com.chinasofti.rcs:id/ivCreateGroup'),
                  'axz': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_setting_name'),
                  'com.chinasofti.rcs:id/manage_switch_undisturb': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/manage_switch_undisturb'),
                  '消息免打扰': (MobileBy.XPATH, '//*[@text="消息免打扰"]'),
                  '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_switch'),
                  '置顶聊天': (MobileBy.XPATH, '//*[@text="置顶聊天"]'),
                  '查找聊天内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_serarch_chat_record'),
                  }

    @TestLogger.log()
    def search_chat_record(self):
        """点击 查找聊天内容"""
        self.click_element(self.__class__.__locators['查找聊天内容'])

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators['返回'])
