from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetSeeQRCodePage(BasePage):
    """群二维码页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupQRActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '群二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/text_title'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/group_qr_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/group_qr_layout'),
                  'com.chinasofti.rcs:id/group_info': (MobileBy.ID, 'com.chinasofti.rcs:id/group_info'),
                  '群聊0010': (MobileBy.ID, 'com.chinasofti.rcs:id/group_qr_name'),
                  'com.chinasofti.rcs:id/photo': (MobileBy.ID, 'com.chinasofti.rcs:id/photo'),
                  'com.chinasofti.rcs:id/left_up': (MobileBy.ID, 'com.chinasofti.rcs:id/left_up'),
                  'com.chinasofti.rcs:id/group_qr_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/group_qr_icon'),
                  'com.chinasofti.rcs:id/right_up': (MobileBy.ID, 'com.chinasofti.rcs:id/right_up'),
                  'com.chinasofti.rcs:id/left_below': (MobileBy.ID, 'com.chinasofti.rcs:id/left_below'),
                  'com.chinasofti.rcs:id/right_below': (MobileBy.ID, 'com.chinasofti.rcs:id/right_below'),
                  '该二维码7天内(11月22日前)有效': (MobileBy.ID, 'com.chinasofti.rcs:id / group_qr_date'),
                  '群二维码分享': (MobileBy.ID, 'com.chinasofti.rcs:id/qecode_share_btn'),
                  '群二维码下载': (MobileBy.ID, 'com.chinasofti.rcs:id/qecode_save_btn')
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待群二维码页面页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['群二维码分享'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_qecode_share_btn(self):
        """点击群二维码分享"""
        self.click_element(self.__class__.__locators["群二维码分享"])

    @TestLogger.log()
    def click_qecode_save_btn(self):
        """点击群二维码下载"""
        self.click_element(self.__class__.__locators["群二维码下载"])

    @TestLogger.log()
    def wait_for_save_qecode_tips_load(self, timeout=8, auto_accept_alerts=True):
        """等待 已保存 提示加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_toast_exist("已保存", timeout)
            )
        except:
            message = "页面在{}s内，没有“已保存”提示加载".format(str(timeout))
            raise AssertionError(
                message
            )
        return self
