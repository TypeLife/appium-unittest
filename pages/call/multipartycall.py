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
        'com.chinasofti.rcs:id/ivDecline': (MobileBy.ID, 'com.chinasofti.rcs:id/ivDecline')
    }

    @TestLogger.log('挂断')
    def hang_up(self):
        self.click_element(self.__locators['com.chinasofti.rcs:id/ivDecline'])

    @TestLogger.log('检查点：提示语“注意接听本机来电，返回和飞信可以管理通话状态哦”')
    def assert_caller_tips_is_display(self):
        self.mobile.assert_screen_contain_text('注意接听本机来电，返回和飞信可以管理通话状态哦')

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
