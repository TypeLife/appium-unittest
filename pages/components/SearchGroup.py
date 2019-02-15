from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SearchGroupPage(BasePage):
    """消息 -> 发起群聊 -> 选择联系人 -> 选择一个群 -> 搜索"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatSearchActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/search_bar': (MobileBy.ID, 'com.chinasofti.rcs:id/search_bar'),
        'com.chinasofti.rcs:id/iv_back': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '群': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
        'com.chinasofti.rcs:id/iv_clear': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_clear'),
        'com.chinasofti.rcs:id/fragment_container': (MobileBy.ID, 'com.chinasofti.rcs:id/fragment_container'),
        'com.chinasofti.rcs:id/title_ll': (MobileBy.ID, 'com.chinasofti.rcs:id/title_ll'),
        '群聊': ('xpath',
               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView'),
        'com.chinasofti.rcs:id/recyclerView': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        'com.chinasofti.rcs:id/contact_image': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_image'),
        '群名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
    }

    @TestLogger.log('搜索')
    def search(self, name):
        self.input_text(self.__locators['群'], name)

    @TestLogger.log('点击群')
    def click_group(self, name):
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

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['com.chinasofti.rcs:id/iv_back'])
