from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time


class CallContactDetailPage(BasePage):
    """ContactDetail"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.ContactDetailActivity'

    __locators = {'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'profileName': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_name'),
                  '星标': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_star'),
                  '编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_call_detail_edit'),
                  '好久不见~打个招呼吧': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_recent_contact_hint'),
                  '138 0013 8001': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_phone'),
                  'G': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_photo_tv'),
                  'com.chinasofti.rcs:id/recyclesafeimageview_profile_photo': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/recyclesafeimageview_profile_photo'),
                  '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_normal_message'),
                  '电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_normal_call'),
                  '语音通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_voice_call'),
                  '视频通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_call'),
                  'com.chinasofti.rcs:id/sv_info': (MobileBy.ID, 'com.chinasofti.rcs:id/sv_info'),
                  'com.chinasofti.rcs:id/rl_andfetion_call': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_andfetion_call'),
                  '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_dial_hefeixin'),
                  'com.chinasofti.rcs:id/call_detail_hefeixin_call': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/call_detail_hefeixin_call'),
                  'com.chinasofti.rcs:id/rv_call_record_detail': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/rv_call_record_detail'),
                  '15:45': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallTime'),
                  '未接通': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallDuration'),
                  'com.chinasofti.rcs:id/ivCallType': (MobileBy.ID, 'com.chinasofti.rcs:id/ivCallType'),
                  '[电话]': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallManner'),
                  '拨出电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallType'),
                  'com.chinasofti.rcs:id/call_detail_divide_line_two': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/call_detail_divide_line_two'),
                  '15:31': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallTime'),
                  '未接通d6f39f43-fa83-403f-9d64-475aaa22ef38': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallDuration'),
                  'com.chinasofti.rcs:id/ivCallType943d39a2-3020-409f-aefa-496bacd8067d': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/ivCallType'),
                  '[电话]d4999267-b770-4815-8675-68a1856f27da': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallManner'),
                  '拨出电话0596d57b-afb9-4a9e-af43-53aa0d1aa9d5': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallType'),
                  'com.chinasofti.rcs:id/call_detail_divide_line_twof592dde0-a29f-40d1-aa34-e22b5c501be0': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/call_detail_divide_line_two'),
                  'com.chinasofti.rcs:id/ll_share_card': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_share_card'),
                  '分享名片/保存到通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card'),
                  '视频缩放按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_switch'),
                  '语音缩放按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_voice_hide'),
                  '正在视频通话': (MobileBy.XPATH, "//*[contains(@text, '视频通话')]"),
                  '正在语音通话': (MobileBy.XPATH, "//*[contains(@text, '语音通话')]"),
                  '和飞信电话免费': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_andfetion_call'),
                  }

    @TestLogger.log()
    def click_normal_message(self):
        """点击消息"""
        self.click_element(self.__locators["消息"])

    @TestLogger.log()
    def click_normal_call(self):
        """点击电话"""
        self.click_element(self.__locators["电话"])

    @TestLogger.log()
    def click_voice_call(self):
        """点击语音通话"""
        self.click_element(self.__locators["语音通话"])

    @TestLogger.log()
    def click_video_call(self):
        """点击视频通话"""
        self.click_element(self.__locators["视频通话"])

    @TestLogger.log()
    def click_dial_hefeixin(self):
        """点击和飞信电话"""
        self.click_element(self.__locators["和飞信电话"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__locators["返回"])

    @TestLogger.log()
    def wait_for_profile_name(self, timeout=30, auto_accept_alerts=True):
        """等待profile页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["profileName"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_share_card(self):
        """点击分享名片/保存到通讯录"""
        self.click_element(self.__locators["分享名片/保存到通讯录"])

    @TestLogger.log()
    def click_call_detail_edit(self):
        """点击编辑"""
        self.click_element(self.__locators["编辑"])

    @TestLogger.log()
    def is_exist_star(self):
        """是否存在星标"""
        flag = False
        el = self.get_elements(self.__locators["星标"])
        if len(el) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_switch(self):
        """点击视频缩放按钮"""
        self.click_element(self.__locators["视频缩放按钮"])

    @TestLogger.log()
    def click_smart_voice_hide(self):
        """点击语音缩放按钮"""
        self.click_element(self.__locators["语音缩放按钮"])

    @TestLogger.log()
    def click_video_call_status(self):
        """点击正在视频通话"""
        self.click_element(self.__locators["正在视频通话"])

    @TestLogger.log()
    def click_voice_call_status(self):
        """点击正在语音通话"""
        self.click_element(self.__locators["正在语音通话"])

    @TestLogger.log()
    def is_exist_video_call(self):
        """等待视频通话消失"""
        mark = 30
        while mark > 0:
            time.sleep(1)
            if not self._is_element_present(self.__class__.__locators["正在视频通话"]):
                break
            mark -= 1

    @TestLogger.log()
    def is_exist_voice_call(self):
        """等待语音通话消失"""
        mark = 30
        while mark > 0:
            time.sleep(1)
            if not self._is_element_present(self.__class__.__locators["正在语音通话"]):
                break
            mark -= 1

    @TestLogger.log()
    def call_fetion_call(self):
        """个人profile页面点击和飞信电话（免费）"""
        self.click_element(self.__locators["和飞信电话免费"])
