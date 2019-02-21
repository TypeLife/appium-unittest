from appium.webdriver.common.mobileby import MobileBy

from library.core.TestLogger import TestLogger
from pages.components import FooterPage


class ContactsPage(FooterPage):
    """通讯录页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (
            MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
            MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '+号': (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/et_search'),
        'com.chinasofti.rcs:id/recyclerView_contactList': (
            MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_contactList'),
        '通讯录列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
        '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_list"]/*'),
        '群聊': (MobileBy.ID, 'com.chinasofti.rcs:id/first_item'),
        '标签分组': (MobileBy.ID, 'com.chinasofti.rcs:id/second_item'),
        '公众号': (MobileBy.ID, 'com.chinasofti.rcs:id/third_item'),
        'com.chinasofti.rcs:id/contact_group_chat_item_id': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_group_chat_item_id'),
        'com.chinasofti.rcs:id/contact_image': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_image'),
        '和通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        'com.chinasofti.rcs:id/rl_group_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
        'D': (MobileBy.ID, ''),
        'dx1645': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '15338821645': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_phone'),
        'F': (MobileBy.ID, ''),
        'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '18681151872': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_phone'),
        'H': (MobileBy.ID, ''),
        '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '12560': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_phone'),
        'X': (MobileBy.ID, ''),
        'xzq': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        'com.chinasofti.rcs:id/contact_index_bar_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
        'com.chinasofti.rcs:id/contact_index_bar_container': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
        'com.chinasofti.rcs:id/viewLine': (MobileBy.ID, 'com.chinasofti.rcs:id/viewLine'),
        'com.chinasofti.rcs:id/view_bg_home_tab': (MobileBy.ID, 'com.chinasofti.rcs:id/view_bg_home_tab'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
        '弹出框点击允许': (MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button'),
        '弹出框点击禁止': (MobileBy.ID, 'com.android.packageinstaller:id/permission_deny_button'),

    }

    @TestLogger.log("获取所有联系人名")
    def get_contacts_name(self):
        """获取所有联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        else:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        if "和通讯录" in contacts_name:
            contacts_name.remove("和通讯录")
        if "和飞信电话" in contacts_name:
            contacts_name.remove("和飞信电话")
        return contacts_name

    @TestLogger.log("通过人名选择一个联系人")
    def select_people_by_name(self, name):
        """通过人名选择一个联系人"""
        self.click_element((MobileBy.XPATH, '//*[@text ="%s"]' % name))

    @TestLogger.log('点击+号')
    def click_add(self):
        """点击+号"""
        self.click_element(self.__locators['+号'])

    @TestLogger.log('点击搜索框')
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__locators['搜索'])

    @TestLogger.log('打开群聊列表')
    def open_group_chat_list(self):
        self.click_element(self.__locators['群聊'])

    @TestLogger.log("滚动列表到顶部")
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['通讯录列表'])
        )
        if self._is_element_present(self.__locators['群聊']):
            return True
        while True:
            self.swipe_by_direction(self.__locators['通讯录列表'], 'up')
            if self._is_element_present(self.__locators['群聊']):
                break
        return True

    @TestLogger.log('判断列表是否存在XXX联系人')
    def is_contact_in_list(self, name):
        self.scroll_to_top()
        groups = self.mobile.list_iterator(self.__locators['通讯录列表'], self.__locators['列表项'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH,
                                   '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log("获取电话号码")
    def get_phone_number(self):
        """获取电话号码"""
        els = self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/contact_phone'))
        phones = []
        if els:
            for el in els:
                phones.append(el.text)
        else:
            raise AssertionError("m005_contacts is empty!")
        return phones

    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_direction(self.__class__.__locators['通讯录列表'], 'up')

    def swipe_half_page_up(self):
        """向上滑动半页"""
        self.swipe_by_percent_on_screen(50, 72, 50, 36, 800)

    @TestLogger.log()
    def get_all_contacts_name(self):
        """获取所有联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        else:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        flag = True
        while flag:
            self.swipe_half_page_up()
            els = self.get_elements(self.__class__.__locators["联系人名"])
            for el in els:
                if el.text not in contacts_name:
                    contacts_name.append(el.text)
                    flag = True
                else:
                    flag = False
        return contacts_name

    @TestLogger.log()
    def click_label_grouping(self):
        """点击标签分组1"""
        self.click_element(self.__class__.__locators['标签分组'])

    @TestLogger.log()
    def click_and_address(self):
        """点击和通讯录"""
        self.click_element(self.__class__.__locators['和通讯录'])


    @TestLogger.log('点击公众号图标')
    def click_official_account_icon(self):
        self.click_element(self.__locators['公众号'])

    @TestLogger.log('创建通讯录联系人')
    def create_contacts_if_not_exits(self, name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        from pages import ContactDetailsPage
        detail_page = ContactDetailsPage()

        self.wait_for_page_load()
        # 创建联系人
        self.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        if contact_search.is_contact_in_list(name):
            contact_search.click_back()
        else:
            contact_search.click_back()
            self.click_add()
            from pages import CreateContactPage
            create_page = CreateContactPage()
            create_page.wait_for_page_load()
            create_page.hide_keyboard_if_display()
            create_page.create_contact(name, number)
            detail_page.wait_for_page_load()
            detail_page.click_back_icon()

    @TestLogger.log()
    def click_and_address(self):
        """点击和通讯录"""
        self.click_element(self.__class__.__locators['和通讯录'])

    @TestLogger.log()
    def click_always_allowed(self):
        """获取通讯录权限点击始终允许"""
        self.click_element(self.__class__.__locators['弹出框点击允许'])

    @TestLogger.log()
    def click_forbidden(self):
        """点击禁止"""
        self.click_element(self.__class__.__locators['弹出框点击禁止'])