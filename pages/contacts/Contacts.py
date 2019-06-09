from appium.webdriver.common.mobileby import MobileBy

from library.core.TestLogger import TestLogger
from pages.components import FooterPage
import time
from library.core.utils.applicationcache import current_mobile

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
        '+号': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_add'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/et_search'),
        'com.chinasofti.rcs:id/recyclerView_contactList': (
            MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_contactList'),
        '通讯录列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
        '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_list"]/*'),
        '手机联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/first_item'),
        '群聊': (MobileBy.ID, 'com.chinasofti.rcs:id/second_item'),
        '标签分组': (MobileBy.XPATH, '//*[@text="标签分组"]'),
        '公众号': (MobileBy.ID, 'com.chinasofti.rcs:id/third_item'),
        '创建团队': (MobileBy.XPATH, '//*[@text="创建团队"]'),
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
        '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
        '18681151872': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_phone'),
        'H': (MobileBy.ID, ''),
        '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '12560': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_phone'),
        'sim标志': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_sim'),
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
        '始终允许': (MobileBy.XPATH, "//*[contains(@text, '始终允许')]"),
        '和通讯录联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
        '和通讯录更多': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_more'),
        '团队管理': (MobileBy.ID, 'com.chinasofti.rcs:id/quit_confirm_tv'),
        '显示':(MobileBy.ID,'com.chinasofti.rcs:id/btn_ok'),
        '不显示': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '企业群标识': (MobileBy.ID, 'com.chinasofti.rcs:id/group_ep'),
        '群聊列表返回': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
        '团队名称': (MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_department'),
        '索引字母容器': (MobileBy.ID, 'com.chinasofti.rcs:id/indexbarview'),
        '新建手机联系人-确定': (MobileBy.ID, 'android:id/icon2'),
        "新建手机联系人-姓名": (MobileBy.XPATH, "//*[@text='姓名']"),
        "新建手机联系人-电话号码": (MobileBy.XPATH, "//*[@text='电话号码']"),
        '新建手机联系人': (MobileBy.ID, 'com.android.contacts:id/hw_fab'),
        '新建手机联系人-下拉按钮': (MobileBy.ID, 'com.android.contacts:id/account_arrow'),


        '已加入团队名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
        '团队联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
    }

    @TestLogger.log("获取所有联系人名")
    def get_contacts_name(self):
        """获取所有联系人名"""
        max_try = 5
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["联系人名"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
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
        if "本机" in contacts_name:
            contacts_name.remove("本机")
        return contacts_name

    @TestLogger.log("获取所有团队名称")
    def get_all_group_name(self):
        """获取所有团队名"""
        max_try = 5
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["已加入团队名称"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        els = self.get_elements(self.__class__.__locators["已加入团队名称"])
        group_name = []
        if els:
            for el in els:
                group_name.append(el.text)
        else:
            raise AssertionError("No m005_group, please add m005_group in address book.")
        return group_name


    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=15):
        """找不到元素就滑动"""
        if self._is_element_present(self.__class__.__locators[locator]):
            return self.get_element(self.__class__.__locators[locator])
        else:
            c = 0
            while c < times:
                self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
                if self._is_element_present(self.__class__.__locators[locator]):
                    return self.get_element(self.__class__.__locators[locator])
                c += 1
            return None

    @TestLogger.log("通过人名选择一个联系人")
    def select_people_by_name(self, name):
        """通过人名选择一个联系人"""
        self.click_element((MobileBy.XPATH, '//*[@text ="%s"]' % name))

    @TestLogger.log('点击+号')
    def click_add(self):
        """点击+号"""
        self.click_element(self.__locators['+号'])

    @TestLogger.log('点击消息')
    def click_message_icon(self):
        """点击消息按钮"""
        self.click_element(self.__locators['消息'])

    @TestLogger.log('点击我页面')
    def click_me_icon(self):
        """点击进入我页面"""
        self.click_element(self.__locators['我'])

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
        current = 0
        while True:
            current += 1
            if current > 20:
                return
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
        els = self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/tv_number'))
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
        current = 0
        while flag:
            current += 1
            if current > 20:
                return
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
        """点击标签分组"""
        self.click_element(self.__class__.__locators['标签分组'])

    @TestLogger.log()
    def click_and_address(self):
        """点击和通讯录"""
        self.click_element(self.__class__.__locators['和通讯录'])

    @TestLogger.log()
    def click_mobile_contacts(self):
        """点击手机联系人"""
        self.click_element(self.__class__.__locators["手机联系人"])

    @TestLogger.log('点击公众号图标')
    def click_official_account_icon(self):
        self.click_element(self.__locators['公众号'])

    # @TestLogger.log('创建通讯录联系人')
    # def create_contacts_if_not_exits(self, name, number, company='', position='', email=''):
    #     """
    #     导入联系人数据
    #     :param name:
    #     :param number:
    #     :return:
    #     """
    #     from pages import ContactDetailsPage
    #     detail_page = ContactDetailsPage()
    #
    #     self.wait_for_page_load()
    #     # 创建联系人
    #     self.click_search_box()
    #     from pages import ContactListSearchPage
    #     contact_search = ContactListSearchPage()
    #     contact_search.wait_for_page_load()
    #     contact_search.input_search_keyword(name)
    #     if contact_search.is_contact_in_list(name):
    #         contact_search.click_back()
    #     else:
    #         contact_search.click_back()
    #         self.click_add()
    #         from pages import CreateContactPage
    #         create_page = CreateContactPage()
    #         create_page.wait_for_page_load()
    #         create_page.hide_keyboard_if_display()
    #         create_page.create_contact(name, number, company, position, email)
    #         detail_page.wait_for_page_load()
    #         detail_page.click_back_icon()

    @TestLogger.log('创建通讯录联系人')
    def create_contacts_if_not_exits(self, name, number, company='', position='', email=''):
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
            self.click_mobile_contacts()
            time.sleep(1)
            self.click_add()
            from pages import CreateContactPage
            create_page = CreateContactPage()
            create_page.wait_for_page_load()
            create_page.hide_keyboard_if_display()
            create_page.create_contact(name, number, company, position, email)
            detail_page.wait_for_page_load()
            detail_page.click_back_icon()
            time.sleep(1)
            detail_page.click_back_by_android()

    @TestLogger.log()
    def click_and_address(self):
        """点击和通讯录"""
        self.click_element(self.__class__.__locators['和通讯录'])

    @TestLogger.log()
    def click_always_allowed(self):
        """获取通讯录权限点击始终允许"""
        if self.get_elements(self.__class__.__locators['弹出框点击允许']):
            self.click_element(self.__class__.__locators['弹出框点击允许'])

    @TestLogger.log()
    def click_forbidden(self):
        """点击禁止"""
        if self.get_elements(self.__class__.__locators['弹出框点击禁止']):
            self.click_element(self.__class__.__locators['弹出框点击禁止'])

    @TestLogger.log()
    def is_exist_allow_button(self):
        """是否存在始终允许"""
        return self._is_element_present(self.__class__.__locators["弹出框点击允许"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通讯录页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["群聊"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_allow(self):
        """点击始终允许"""
        self.click_element(self.__class__.__locators['始终允许'])

    @TestLogger.log()
    def click_one_he_contacts(self):
        """获取和通讯录联系人"""
        els=self.get_elements(self.__class__.__locators['和通讯录联系人'])
        if els:
            els[0].click()
        else:
            raise AssertionError("和通迅录没有联系人，请添加")

    @TestLogger.log()
    def click_he_more(self):
        """点击和通讯录联系人更多"""
        self.click_element(self.__class__.__locators['和通讯录更多'])

    @TestLogger.log("处理SIM联系人弹框")
    def click_sim_contact(self):
        """点击不显示sim卡联系人"""
        time.sleep(2)
        if self.get_elements(self.__class__.__locators['不显示']):
            self.click_element(self.__class__.__locators['不显示'])

    @TestLogger.log("处理SIM联系人弹框")
    def click_sim_contact_ok(self):
        """点击显示sim卡联系人"""
        time.sleep(2)
        if self.get_elements(self.__class__.__locators['显示']):
            self.click_element(self.__class__.__locators['显示'])


    @TestLogger.log()
    def is_exist_enterprise_group(self):
        """是否存在企业群"""
        max_try = 10
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["企业群标识"]):
                return True
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return False

    @TestLogger.log()
    def click_return(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['群聊列表返回'])

    @TestLogger.log()
    def click_one_firm(self):
        """点击一个团队"""
        self.click_element(self.__class__.__locators['团队名称'])

    @TestLogger.log()
    def wait_for_contacts_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通讯录页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def select_contacts_by_name(self, name):
        """根据名字选择一个联系人"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def select_group_by_name(self, name):
        """根据名字选择一个团队"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_department" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def select_group_contact_by_name(self, name):
        """根据名字选择一个团队内的联系人"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name_personal_contactlist" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)



    @TestLogger.log()
    def page_contain_element_add(self):
        """页面包含元素+号"""
        self.page_should_contain_element(self.__class__.__locators['+号'])


    @TestLogger.log('判断元素是否存在')
    def is_page_contain_element(self, locator,times=10):
        # el=self.find_element_by_swipe(self.__class__.__locators[locator])
        if self._is_element_present(self.__class__.__locators[locator]):
             self.page_should_contain_element(self.__class__.__locators[locator])
        else:
            c = 0
            while c < times:
                self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
                if self._is_element_present(self.__class__.__locators[locator]):
                    return self.page_should_contain_element(self.__class__.__locators[locator])
                c += 1
            return self.page_should_contain_element(self.__class__.__locators[locator])


    @TestLogger.log("根据导航栏的第一个字母定位")
    def choose_index_bar_click_element(self):
        self.click_element(
            ('xpath','//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView[1]'))
        elements = self.get_elements(self.__class__.__locators["群聊名"])
        elements[0].click()

    def get_letters_index(self):
        """获取所有索引字母"""
        container_el = self.get_element(self.__class__.__locators['索引字母容器'])
        letter_els = container_el.find_elements(MobileBy.XPATH, "//android.view.View")
        if not letter_els:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        letters = []
        for el in letter_els:
            letters.append(el.text)
        return letters

    @TestLogger.log()
    def click_letter_index(self, letter):
        """点击字母索引"""
        container_el = self.get_element(self.__class__.__locators['索引字母容器'])
        container_el.find_element(MobileBy.XPATH, "//android.view.View[@text='%s']" % letter).click()


    @TestLogger.log('点击新建SIM联系人界面-确定')
    def click_sure_SIM(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['新建手机联系人-确定'])

    @TestLogger.log('输入文本内容-手机联系人姓名')
    def input_contact_text(self,text):
        self.input_text(self.__class__.__locators["新建手机联系人-姓名"],text)

    @TestLogger.log('输入文本内容-手机联系人电话')
    def input_contact_number(self,text):
        self.input_text(self.__class__.__locators["新建手机联系人-电话号码"],text)

    @TestLogger.log('点击新建SIM联系人')
    def click_creat_contacts(self):
        """点击新建联系人"""
        self.click_element(self.__class__.__locators['新建手机联系人'])

    @TestLogger.log()
    def select_contacts_by_number(self, number):
        """根据号码选择一个联系人"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_number" and @text ="%s"]' % number)
        max_try = 20
        current = 0
        while current < max_try:

            if self._is_element_present(locator):
                break
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
            current += 1
        self.click_element(locator)

    @TestLogger.log()
    def is_exit_element_by_text_swipe(self, number):
        """通过电话号码,滑动判断特定元素是否存在"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_number" and @text ="%s"]' % number)
        max_try = 20
        current = 0
        while current < max_try:
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
            if self._is_element_present(locator):
                return self.page_should_contain_element(locator)
            else:
                # break
                current += 1

    @TestLogger.log()
    def is_contacts_exist(self, name):
        """通过联系人名判断联系人是否存在"""
        max_try = 20
        current = 0
        while current < max_try:
            if self.is_text_present(name):
                return True
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
            current += 1
            # self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return False

    @TestLogger.log()
    def click_SIM_identification(self):
        """点击sim标志"""
        self.click_element(self.__class__.__locators['sim标志'])

    @TestLogger.log()
    def click_drop_down_button(self):
        """点击下拉按钮"""
        self.click_element(self.__class__.__locators['新建手机联系人-下拉按钮'])

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @TestLogger.log('添加系统联系人')
    def add_system_contacts(self,name="系统1",number='13813813801'):
        self.background_app()
        time.sleep(2)
        self.click_text('拨号')
        time.sleep(2)
        self.click_text('联系人')
        time.sleep(1)
        self.click_creat_contacts()
        time.sleep(1)
        self.hide_keyboard()
        if self.is_text_present('保存至: 手机'):
            pass
        else:
            self.click_drop_down_button()
            time.sleep(1)
            self.click_text('仅保存在手机')
            time.sleep(2)
        self.click_text('姓名')
        self.input_contact_text(name)
        self.click_text('电话号码')
        self.input_contact_number(number)
        self.click_sure_SIM()
        time.sleep(2)

    @TestLogger.log('添加系统联系人')
    def add_SIM_contacts(self,name="sim联系人",number='12345678912'):
        self.background_app()
        time.sleep(2)
        self.click_text('拨号')
        time.sleep(2)
        self.click_text('联系人')
        time.sleep(1)
        self.click_creat_contacts()
        time.sleep(1)
        self.hide_keyboard()
        self.click_drop_down_button()
        time.sleep(1)
        self.click_text('SIM卡')
        time.sleep(2)
        self.click_text('姓名')
        self.input_contact_text(name)
        self.click_text('电话号码')
        self.input_contact_number(number)
        self.click_sure_SIM()
        time.sleep(2)


    @TestLogger.log("是否在当前页面")
    def is_on_this_page(self):
        time.sleep(2)
        return self.is_text_present('分享名片')

    @TestLogger.log("滚动通讯录顶部(显示搜索框)")
    def swipe_to_page_top(self):
        if self._is_element_present(self.__locators['搜索']):
            return True
        current = 0
        while current < 20:
            current += 1
            self.swipe_by_percent_on_screen(50, 30, 50, 70, 700)
        return True
