from appium.webdriver.common.mobileby import MobileBy
import re
import copy
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
        'X': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
        '聊天电话': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        # 分享二维码的选择联系人页面
        '选择本地联系人': (MobileBy.XPATH, '//*[@text ="选择本地联系人"]'),
        'tel:+86': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_number"]'),

        # 未知号码
        '未知号码': (MobileBy.XPATH, '//*[contains(@text,"未知号码")]'),
        # 选择一个联系人转发消息时的弹框
        '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
        '取消转发': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
        '确定转发': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
        'local联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/send_tv'),
        '联系人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
        '右侧字母索引': (MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView'),
        '左侧字母索引': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/index_text"]'),
        '查看更多': (MobileBy.XPATH, '//*[@text ="查看更多"]'),
        '和通讯录返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
        "最近聊天消息名称": (MobileBy.ID, "com.chinasofti.rcs:id/tv_name"),
        "联系人横框": (MobileBy.ID, "com.chinasofti.rcs:id/contact_list_item"),
        "搜索框左边选中联系人": (MobileBy.ID, "com.chinasofti.rcs:id/image"),
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
    def click_he_back(self):
        """点击 和通讯录返回"""
        self.click_element(self.__class__.__locators["和通讯录返回"])

    @TestLogger.log('点击分享名片')
    def click_share_card(self):
        """点击分享名片"""
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log('搜索或输入手机号')
    def click_search_contact(self):
        """点击搜索或输入手机号"""
        self.click_element(self.__locators['搜索或输入手机号'])

    @TestLogger.log('搜索或输入手机号')
    def input_search_keyword(self, keyword):
        """输入搜索内容"""
        self.input_text(self.__locators['搜索或输入手机号'], keyword)

    @TestLogger.log()
    def click_search_keyword(self):
        """点击搜索或输入手机号"""
        self.click_element(self.__class__.__locators["搜索或输入手机号"])

    @TestLogger.log('点击联系人')
    def click_contact(self, name):
        """点击联系人"""
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and ' +
                            '@text="{}"]'.format(name)))

    @TestLogger.log('点击联系人头像')
    def click_cantact_avatar(self):
        """点击联系人头像"""
        self.click_element(self.__locators['联系人头像'])

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
        els = self.get_elements(self.__class__.__locators["local联系人"])
        contactnames = []
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
    def select_one_group_by_name(self, name):
        """通过群名选择一个群"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def select_one_recently_contact_by_name(self, name):
        """通过名称选择一个最近聊天的联系人"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text ="%s"]' % name))

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
    def catch_message_in_page(self, text):
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
    def click_one_contact(self, contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)

    @TestLogger.log()
    def input_search_contact_message(self, message):
        """输入查询联系人查询信息"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log('检验搜索名称')
    def get_element_text_net_name(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        text = text + "(未知号码)"
        return self.element_should_contain_text(self.__locators[locator], text)

    @TestLogger.log('检验搜索号码')
    def get_element_text_net_number(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        text = "tel: +86" + text
        return self.element_should_contain_text(self.__locators[locator], text)

    @TestLogger.log('获取元素文本内容')
    def get_element_texts(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        locator = self.get_text(self.__locators[locator])
        if text.startswith("+86"):
            text = text[3:]
        if text.startswith("+852"):
            text = text[4:]
        if text.startswith("+"):
            text = text[1:]
        if text in locator:
            return True
        return False

    @TestLogger.log('判断该页面是否有元素')
    def page_contain_element(self, locator):
        return self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log('点击最近聊天')
    def click_search_he_contact(self):
        self.click_element(self.__locators["最近聊天"])

    @TestLogger.log()
    def click_x_icon(self):
        """点击 X"""
        self.click_element(self.__class__.__locators["X"])

    @TestLogger.log()
    def click_read_more(self):
        """点击查看更多"""
        self.click_element(self.__class__.__locators["查看更多"])

    @TestLogger.log()
    def wait_for_create_msg_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 '消息页面 点击+ ->新建消息->选择联系人页面' 加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log()
    def is_left_letters_sorted(self):
        """左侧字母是否顺序排序"""
        els = self.get_elements(self.__locators['左侧字母索引'])
        letters = []
        for el in els:
            letters.append(el.text)
        # 过滤特殊字符
        for item in letters:
            if not re.match(r'[A-Za-z]', item):
                letters.remove(item)
        arrs = copy.deepcopy(letters)
        letters = sorted(letters)
        return arrs == letters

    @TestLogger.log()
    def is_right_letters_sorted(self):
        """右侧字母是否顺序排序"""
        els = self.get_elements(self.__locators['右侧字母索引'])
        letters = []
        for el in els:
            letters.append(el.text)
        for item in letters:
            if not re.match(r'[A-Za-z]', item):
                letters.remove(item)
        arrs = copy.deepcopy(letters)
        letters = sorted(letters)
        return arrs == letters

    @TestLogger.log()
    def select_recent_chat_by_number(self, number):
        """选择某一条最近聊天记录"""
        if self._is_element_present(self.__class__.__locators["最近聊天消息名称"]):
            els = self.get_elements(self.__class__.__locators["最近聊天消息名称"])
            els[number].click()

    @TestLogger.log()
    def is_page_more_text(self, menu):
        """选择某一条最近聊天记录"""
        for text in menu:
            self.is_text_present(text)
        return True

    @TestLogger.log()
    def click_sure_bottom(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def result_is_more_tree(self):
        """点击确定"""
        els = self.get_elements(self.__class__.__locators["local联系人"])
        if len(els) > 3:
            return True
        else:
            return False

    @TestLogger.log()
    def is_element_present_by_locator(self,text):
        """判断指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def swipe_and_find_element(self, text):
        """滑动并查找特定元素"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % text))
        if el:
            return True
        else:
            return False
