from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SelectGroupChatPage(BasePage):
    """选择联系人页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/top_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/top_layout'),
                  'com.chinasofti.rcs:id/layout_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_search'),
                  '搜索或输入手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  'com.chinasofti.rcs:id/bottom_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/bottom_layout'),
                  'com.chinasofti.rcs:id/recyclerView_recently_person': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_recently_person'),
                  'com.chinasofti.rcs:id/local_contacts': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contacts'),
                  '选择一个群': (MobileBy.XPATH, '//*[@text ="选择一个群"]'),
                  'com.chinasofti.rcs:id/arrow_right': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_right'),
                  '选择和通讯录联系人': (MobileBy.XPATH, '//*[@text ="选择和通讯录联系人"]'),
                  '本地联系人': (MobileBy.XPATH, '//*[@text ="本地联系人"]'),
                  '最近聊天': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint')
                  }

    @TestLogger.log()
    def click_select_one_group(self):
        """点击 选择一个群"""
        self.click_element(self.__class__.__locators["选择一个群"])

    @TestLogger.log()
    def click_he_contacts(self):
        """点击 选择和通讯录联系人"""
        self.click_element(self.__class__.__locators["选择和通讯录联系人"])

    @TestLogger.log()
    def click_local_contacts(self):
        """点击 本地联系人"""
        self.click_element(self.__class__.__locators["本地联系人"])
