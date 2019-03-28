from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class CallContactDetailPage(BasePage):
    """ContactDetail"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.ContactDetailActivity'

    __locators = {'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/iv_back': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  '给个红包2': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_name'),
                  'com.chinasofti.rcs:id/iv_star': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_star'),
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
                  '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card')
                  }

    @TestLogger.log()
    def click_normal_message(self):
        """点击消息"""
        self.click_element(self.__locators["消息"])

    @TestLogger.log()
    def click_normal_call(self):
        """点击电话"""
        self.click_element(self.__locators["电话"])
