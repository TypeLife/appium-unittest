from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ContactDetailsPage(BasePage):
    """个人详情"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.ContactDetailActivity'

    __locators = {
        '返回上一页': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '名片标题': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_name'),
        '星标': (MobileBy.ID, 'com.chinasofti.rcs:id/star'),
        '编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/txt_call_detail_edit'),
        '好久不见~打个招呼吧': (MobileBy.ID, 'com.chinasofti.rcs:id/recent_contact_hint'),
        '名片号码': (MobileBy.ID, 'com.chinasofti.rcs:id/phone'),
        '名片首字母': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo_tv'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_photo_tv'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_normal_message'),
        '电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_normal_call'),
        '语音通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_voice_call'),
        '视频通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_call'),
        '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_dial_hefeixin'),
        '详细信息列表容器': (MobileBy.ID, 'com.chinasofti.rcs:id/sv_info'),
        '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '公司名': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '职位名': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '邮箱地址': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card'),
        'com.chinasofti.rcs:id/btn_share_card_line': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card_line'),
        '邀请使用': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_invitation_to_use'),
        '大图': (MobileBy.ID, 'com.chinasofti.rcs:id/img_smooth'),
    }

    @TestLogger.log("点击返回按钮")
    def click_back_icon(self):
        """点击返回"""
        self.click_element(self.__locators['返回上一页'])

    @TestLogger.log("点击编辑")
    def click_edit_contact(self):
        """点击编辑按钮"""
        self.click_element(self.__locators['编辑'])


    @TestLogger.log("获取名片名称")
    def get_contact_name(self, wait_time=0):
        title = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['名片标题']),
            timeout=wait_time
        )
        return title.text

    @TestLogger.log('获取名片号码')
    def get_contact_number(self, wait_time=0):
        number = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['名片号码']),
            timeout=wait_time
        )
        return number.text

    @TestLogger.log("点击消息图标")
    def click_message_icon(self):
        self.click_element(self.__locators['消息'])

    @TestLogger.log('点击电话图标')
    def click_call_icon(self):
        self.click_element(self.__locators['电话'])

    @TestLogger.log("点击语音通话图标")
    def click_voice_call_icon(self):
        self.click_element(self.__locators['语音通话'])

    @TestLogger.log("点击视频通话图标")
    def click_video_call_icon(self):
        self.click_element(self.__locators['视频通话'])

    @TestLogger.log("点击和飞信电话菜单")
    def click_hefeixin_call_menu(self):
        self.click_element(self.__locators['和飞信电话'])

    @TestLogger.log("点击头像查看大图")
    def click_avatar(self):
        """点击头像查看大图"""
        self.click_element(self.__locators['头像'])

    @TestLogger.log("点击大图")
    def click_big_avatar(self):
        """点击大图"""
        self.click_element(self.__locators['大图'])

    @TestLogger.log("点击分享名片")
    def click_share_business_card(self):
        """点击分享名片"""
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log("邀请使用")
    def click_invitation_use(self):
        """邀请使用"""
        self.click_element(self.__locators['邀请使用'])

    @TestLogger.log()
    def message_btn_is_clickable(self):
        """消息按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["消息"])

    @TestLogger.log()
    def call_btn_is_clickable(self):
        """电话按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators["电话"])

    @TestLogger.log()
    def voice_btn_is_clickable(self):
        """语音通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["语音通话"])

    @TestLogger.log()
    def video_call_btn_is_clickable(self):
        """视频通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["视频通话"])

    @TestLogger.log()
    def hefeixin_call_btn_is_clickable(self):
        """和飞信通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["和飞信电话"])