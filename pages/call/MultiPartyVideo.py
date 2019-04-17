from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MultiPartyVideoPage(BasePage):
    """MultipartyVideoPage"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactSelectorActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '多方视频': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '呼叫': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '搜索或输入号码': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/local_contact_lv': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contact_lv'),
        'com.chinasofti.rcs:id/contact_list': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
        'com.chinasofti.rcs:id/local_contacts': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contacts'),
        '选择和通讯录联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        'com.chinasofti.rcs:id/arrow_right': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_right'),
        '联系人item': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
        'D': (MobileBy.ID, 'com.chinasofti.rcs:id/index_text'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
        'com.chinasofti.rcs:id/contact_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_icon'),
        '大佬1': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138005': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '大佬2': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138006': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '大佬3': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138007': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '大佬4': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138008': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        'G': (MobileBy.ID, 'com.chinasofti.rcs:id/index_text'),
        '给个红包1': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138000': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '给个红包2': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138001': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '给个红包3': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '已选择成员': (MobileBy.ID, 'com.chinasofti.rcs:id/hor_contact_selection')
    }

    @TestLogger.log()
    def click_contact_head(self, index=0):
        """点击联系人头像"""
        el = self.get_elements(self.__locators["头像"])
        el[index].click()

    @TestLogger.log()
    def is_exist_contact_head(self):
        """是否存在搜索结果"""
        return self._is_element_present(self.__locators["头像"])

    @TestLogger.log()
    def is_on_multi_party_video_page(self):
        """判断当前是否在多方视频选择界面"""
        return self._is_element_present(self.__locators["多方视频"])

    @TestLogger.log()
    def is_exist_contact_selection(self):
        """判断当前是否存在已选择成员"""
        return self._is_element_present(self.__locators["已选择成员"])

    @TestLogger.log()
    def click_tv_sure(self):
        """点击呼叫"""
        self.click_element(self.__locators["呼叫"])

    @TestLogger.log()
    def input_contact_search(self, text):
        """输入电话号码并搜索"""
        self.input_text(self.__locators["搜索或输入号码"], text)
