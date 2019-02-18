from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class PickGroupPage(BasePage):
    """消息 -> 发起群聊 -> 选择联系人 -> 选择一个群"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatListMergaActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
            MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
        'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
            MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
        '选择一个群': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
        '搜索群组': (MobileBy.ID, 'com.chinasofti.rcs:id/et_search'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/recyclerView': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        'A': ('xpath',
              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]'),
        'com.chinasofti.rcs:id/contact_image': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_image'),
        'C': ('xpath',
              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[2]'),
        'chargourp3465': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        'G': ('xpath',
              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[3]'),
        '群名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        'com.chinasofti.rcs:id/contact_index': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index'),
        'Q': ('xpath',
              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[4]'),
        'com.chinasofti.rcs:id/contact_index_bar_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
        'com.chinasofti.rcs:id/contact_index_bar_container': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container')
    }

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['com.chinasofti.rcs:id/left_back'])

    @TestLogger.log('点击“搜索群组”输入框')
    def search_group(self):
        self.click_element(self.__locators['搜索群组'])

    @TestLogger.log('选择群组')
    def select_group(self, name):
        group_generator = self.mobile.list_iterator(self.__locators['com.chinasofti.rcs:id/recyclerView'],
                                                    ['xpath',
                                                     '//*[@resource-id="com.chinasofti.rcs:id/recyclerView"]/*'])
        for i in group_generator:
            name_elements = i.find_elements(*self.__locators['群名'])
            if name_elements:
                real_name = name_elements[0].text
                if real_name == name:
                    i.click()
                    return real_name
        raise NoSuchElementException('找不到名字等于“{}”的群聊'.format(name))
