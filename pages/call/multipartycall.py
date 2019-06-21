from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.dialogs import SuspendedTips


class MultipartyCallPage(SuspendedTips, BasePage):
    """多方通话主叫页面"""
    ACTIVITY = 'com.cmicc.module_call.ui.multipartycall.MultipartyCallActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/viewBgTips': (MobileBy.ID, 'com.chinasofti.rcs:id/viewBgTips'),
        'com.chinasofti.rcs:id/smart_multi_call_hide': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_multi_call_hide'),
        'com.chinasofti.rcs:id/ivAvatar': (MobileBy.ID, 'com.chinasofti.rcs:id/ivAvatar'),
        '我 (主叫)': (MobileBy.ID, 'com.chinasofti.rcs:id/tvLocation'),
        'com.chinasofti.rcs:id/recyclerView': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '最多9人': (MobileBy.ID, 'com.chinasofti.rcs:id/tvName'),
        'com.chinasofti.rcs:id/ivStateBg': (MobileBy.ID, 'com.chinasofti.rcs:id/ivStateBg'),
        '呼叫中': (MobileBy.ID, 'com.chinasofti.rcs:id/tvState'),
        '给个红包1': (MobileBy.ID, 'com.chinasofti.rcs:id/tvName'),
        '给个红包2': (MobileBy.ID, 'com.chinasofti.rcs:id/tvName'),
        'com.chinasofti.rcs:id/ivTips': (MobileBy.ID, 'com.chinasofti.rcs:id/ivTips'),
        '注意接听本机来电，返回和飞信可以管理通话状态哦': (MobileBy.ID, 'com.chinasofti.rcs:id/tvTips'),
        '00:00': (MobileBy.ID, 'com.chinasofti.rcs:id/chronometer'),
        'com.chinasofti.rcs:id/ll_groupcall_mute': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_groupcall_mute'),
        'com.chinasofti.rcs:id/iv_group_mute': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_group_mute'),
        '全员禁音': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_group_mute_text'),
        'com.chinasofti.rcs:id/ivDecline': (MobileBy.ID, 'com.chinasofti.rcs:id/ivDecline'),
        '请先接听来电，随后将自动呼叫对方': (MobileBy.ID, 'com.chinasofti.rcs:id/accept_tip'),
        '+': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.ImageView'),
        '最小化': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_multi_call_hide'),
        '全员禁言': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_groupcall_mute'),
        # '呼叫中': (MobileBy.XPATH, '//*[contains(@text,"呼叫中")]'),
        '未接通': (MobileBy.XPATH, '//*[contains(@text,"未接通")]'),
        '重新拨号': (MobileBy.XPATH, '//*[contains(@text,"重新拨号")]'),
        '移除成员': (MobileBy.XPATH, '//*[contains(@text,"移除成员")]'),
        '取消': (MobileBy.XPATH, '//*[contains(@text,"取消")]'),
    }

    @TestLogger.log('挂断')
    def hang_up(self):
        self.click_element(self.__locators['com.chinasofti.rcs:id/ivDecline'])

    @TestLogger.log('检查点：提示语“注意接听本机来电，返回和飞信可以管理通话状态哦”')
    def assert_caller_tips_is_display(self):
        self.mobile.assert_screen_contain_text('注意接听本机来电，返回和飞信可以管理通话状态哦')

    @TestLogger.log('检查点：提示语“请先接听来电，随后将自动呼叫对方”')
    def assert_accepttips_is_display(self):
        self.mobile.assert_screen_contain_text('请先接听来电，随后将自动呼叫对方')

    @TestLogger.log('等待回拨电话呼入')
    def wait_for_call_back(self, max_wait_time=8):
        self.wait_until(
            condition=lambda d: self.mobile.is_phone_in_calling_state(),
            timeout=max_wait_time
        )

    @TestLogger.log('等待页面自动跳转')
    def wait_for_page_jump_out_automatically(self, max_wait_time=8):
        self.wait_until(
            condition=lambda d: self.mobile.current_activity == self.__class__.ACTIVITY,
            timeout=max_wait_time,
        )

    @TestLogger.log('呼叫人状态为“呼叫中”')
    def assert_caller_status_is_display(self):
        self.mobile.assert_element_should_contain_text(self.__locators['呼叫中'], '呼叫中')

    @TestLogger.log('显示左上角按钮')
    def assert_hide_icon_is_display(self):
        self.mobile.assert_screen_should_contain_element(self.__locators['com.chinasofti.rcs:id/smart_multi_call_hide'])

    @TestLogger.log('+号显示最多9人')
    def assert_caller_max_count_is_display(self):
        self.mobile.assert_element_should_contain_text((MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView'), '最多9人')

    @TestLogger.log('主叫人展示“我（主叫）”')
    def assert_caller_me_is_display(self):
        self.mobile.assert_element_should_contain_text(self.__locators['我 (主叫)'], '我 (主叫)')

    @TestLogger.log('点击+号')
    def click_caller_add_icon(self):
        self.click_element(self.__locators['+'])

    @TestLogger.log('点击呼叫中成员头像')
    def click_caller_image(self):
        self.click_element(self.__locators['呼叫中'])

    @TestLogger.log()
    def is_exist_accept_feixincall_then_tryagain(self):
        """弹框-请接听和飞信电话后再试"""
        return self.is_toast_exist("请接听飞信电话后再试")

    @TestLogger.log('点击最小化窗口')
    def click_min_window(self):
        self.click_element(self.__locators['最小化'])

    @TestLogger.log('点击全员禁言')
    def click_groupcall_mute(self):
        self.click_element(self.__locators['全员禁言'])

    @TestLogger.log('点击呼叫中')
    def click_calling(self):
        self.click_element(self.__locators['呼叫中'])

    @TestLogger.log('点击未接通')
    def click_not_access(self):
        self.click_element(self.__locators['未接通'])

    @TestLogger.log('点击重新拨号')
    def click_call_again(self):
        self.click_element(self.__locators['重新拨号'])

    @TestLogger.log('点击移除成员')
    def click_remove_caller(self):
        self.click_element(self.__locators['移除成员'])

    @TestLogger.log('点击取消')
    def click_cancel(self):
        self.click_element(self.__locators['取消'])

    @TestLogger.log('检查点：name联系人的通话状态是否为status”')
    def assert_caller_status(self, name, status):
        self.mobile.assert_screen_contain_text('注意接听本机来电，返回和飞信可以管理通话状态哦')
