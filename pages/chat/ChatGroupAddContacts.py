from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatGroupAddContactsPage(BasePage):
    """添加群成员页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {'': (MobileBy.ID, ''),
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
                  'com.chinasofti.rcs:id/contact_selection_list_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/contact_selection_list_view'),
                  '容器列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
                  'com.chinasofti.rcs:id/contact_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
                  'com.chinasofti.rcs:id/asp_selecttion_contact_content': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/asp_selecttion_contact_content'),
                  'D': (MobileBy.ID, ''),
                  'dx1645': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '15338821645': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'F': (MobileBy.ID, ''),
                  'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '18681151872': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'H': (MobileBy.ID, ''),
                  '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '12560': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'X': (MobileBy.ID, ''),
                  'xzq': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '13510772034': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  '联系人名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '电话号码': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
                  'com.chinasofti.rcs:id/contact_index_bar_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
                  'com.chinasofti.rcs:id/contact_index_bar_container': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
                  # 删除成员
                  '确定删除': (MobileBy.XPATH, '//*[@text="确定"]'),
                  # 分享群二维码时选择联系人后的弹窗页面
                  '确定分享': (MobileBy.XPATH, '//*[@text="确定"]'),
                  '取消分享': (MobileBy.XPATH, '//*[@text="取消"]'),
                  '发送给:xxx': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
                  # 群主转让
                  '确定转让': (MobileBy.XPATH, '//*[@text="确定"]'),
                  '取消转让': (MobileBy.XPATH, '//*[@text="取消"]'),
                  # 选择一个本地联系人转发消息时的弹框
                  '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
                  '取消转发': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
                  '确定转发': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
                  '添加群成员': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '发出群邀请提示':(MobileBy.ID,'com.chinasofti.rcs:id/tv_sys_msg')
                  }


    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["添加群成员"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_contacts_name(self):
        """获取联系人名"""
        els = self.get_elements(self.__class__.__locators["联系人名"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        return contacts_name

    @TestLogger.log()
    def select_one_member_by_name(self, name):
        """通过人名选择一个联系人"""
        self.click_element((MobileBy.XPATH, '//*[@text ="%s"]' % name))

    @TestLogger.log()
    def sure_btn_is_enabled(self):
        """确定按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])