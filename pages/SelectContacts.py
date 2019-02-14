from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SelectContactsPage(BasePage):
    """选择联系人页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
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
        '最近聊天': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        # 分享二维码的选择联系人页面
        '选择本地联系人': (MobileBy.XPATH, '//*[@text ="选择本地联系人"]'),
        # 未知号码
        '未知号码': (MobileBy.XPATH, '//*[contains(@text,"未知号码")]'),
        # 选择一个联系人转发消息时的弹框
        '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
        '取消转发': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
        '确定转发': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
        'local联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
    }

    @TestLogger.log()
    def search(self, text):
        """搜索联系人"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], text)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

    @TestLogger.log()
    def is_present_unknown_member(self, timeout=3, auto_accept_alerts=True):
        """是否是未知号码（陌生号码）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["未知号码"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_unknown_member(self):
        """点击 未知号码（陌生号码）"""
        self.click_element(self.__class__.__locators["未知号码"])

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定转发"""
        self.click_element(self.__class__.__locators['确定转发'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消转发"""
        self.click_element(self.__class__.__locators['取消转发'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=3, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择一个群"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators["返回"])

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

    @TestLogger.log()
    def select_local_contacts(self):
        """选择本地联系人"""
        self.click_element(self.__class__.__locators["选择本地联系人"])

    @TestLogger.log()
    def click_one_local_contacts(self):
        """点击一个本地联系人"""
        els=self.get_elements(self.__class__.__locators["local联系人"])
        contactnames=[]
        if els:
            for el in els:
                contactnames.append(el.text)
            self.select_one_contact_by_name(contactnames[0])
        else:
            raise AssertionError("没有本地联系人可转发")

    @TestLogger.log()
    def select_one_contact_by_name(self, name):
        """通过名称选择一个联系人"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def wait_for_page_local_contact_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def catch_message_in_page(self,text):
        return self.is_toast_exist(text)

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=10):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)

    @TestLogger.log()
    def click_one_contact(self,contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)


