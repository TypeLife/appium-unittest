from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatNoticeDialog(BasePage):
    """消息 - 聊天 - 用户须知提示框"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {
        '提示框': (MobileBy.ID, 'android:id/content'),
        '用户须知': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '须知内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
        '我已阅读': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_check'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_btn_ok')
    }

    @TestLogger.log()
    def is_exist_tips(self):
        """是否存在用户须知"""
        return self._is_element_present(self.__class__.__locators["用户须知"])

    @TestLogger.log('判断是否显示用户须知提示框')
    def is_tips_display(self, max_wait_time=3):
        try:
            self.wait_until(
                condition=lambda d: self.is_text_present('用户须知'),
                timeout=max_wait_time
            )
            return True
        except TimeoutException:
            return False

    @TestLogger.log('勾选用户须知后点击确定')
    def accept_and_close_tips_alert(self):
        self.select_checkbox(self.__locators['我已阅读'])
        self.click_element(self.__locators['确定'])

    @TestLogger.log('不勾选用户须知直接关闭提示框')
    def directly_close_tips_alert(self):
        self.unselect_checkbox(self.__locators['我已阅读'])
        alert_box = self.get_element(self.__locators['提示框'])
        position = (alert_box.location.get('x'), alert_box.location.get('y') - 100)
        print('tap position: {}'.format(position))
        self.mobile.tap([position])


class DeleteConfirmDialog(BasePage):
    __locators = {
        '取消': (MobileBy.XPATH, '//*[@text="取消"]'),
        '删除': (MobileBy.XPATH, '//*[@text="刪除"]'),
    }

    @TestLogger.log('点击取消')
    def click_cancel(self):
        self.click_element(self.__locators['取消'])

    @TestLogger.log('点击删除')
    def click_delete(self):
        self.click_element(self.__locators['删除'])


class SuspendedTips(BasePage):
    """通讯录 - 标签分组 - 多方通话 - 悬浮窗权限授权提示"""
    ACTIVITY = 'com.cmicc.module_call.ui.multipartycall.MultipartyCallActivity'

    __locators = {
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'android:id/parentPanel': (MobileBy.ID, 'android:id/parentPanel'),
        'android:id/contentPanel': (MobileBy.ID, 'android:id/contentPanel'),
        'android:id/scrollView': (MobileBy.ID, 'android:id/scrollView'),
        'android:id/textSpacerNoTitle': (MobileBy.ID, 'android:id/textSpacerNoTitle'),
        '您的手机没有授予悬浮窗权限，请开启后再试': (MobileBy.ID, 'android:id/message'),
        'android:id/buttonPanel': (MobileBy.ID, 'android:id/buttonPanel'),
        '暂不开启': (MobileBy.ID, 'android:id/button2'),
        '现在去开启': (MobileBy.ID, 'android:id/button1')
    }

    @TestLogger.log('暂不开启')
    def click_not_open_now(self):
        self.click_element(self.__locators['暂不开启'])

    @TestLogger.log('现在去开启')
    def click_open_now(self):
        self.click_element(self.__locators['现在去开启'])
        self.click_element((MobileBy.ID, 'android:id/switch_widget'))
        self.click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))


    @TestLogger.log('如果弹出“您的手机没有授予悬浮窗权限”提示框，点击暂不开启')
    def ignore_tips_if_tips_display(self):
        try:
            self.click_not_open_now()
        except:
            print('没有提示框弹出或没找到提示框')

    @TestLogger.log('如果弹出“您的手机没有授予悬浮窗权限”提示框，点击现在去开启')
    def actionnow_tips_if_tips_display(self):
        try:
            self.click_open_now()
        except:
            print('没有提示框弹出或没找到提示框')


class MutiVideoTipsPage(BasePage):
    """多方视频 - 多方视频提示"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactSelectorActivity'

    __locators = {
        'com.chinasofti.rcs:id/pop_window_for_10g_root_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_for_10g_root_view'),
        'com.chinasofti.rcs:id/pop_window_for_10g_main_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_for_10g_main_view'),
        '每月10G免流特权': (MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_title'),
        '多方视频通话每分钟消耗约8MB流量，订购[每月10G]畅聊语音/视频通话': (MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_content'),
        '继续拨打': (MobileBy.ID, 'com.chinasofti.rcs:id/continue_call'),
        '订购免流特权': (MobileBy.ID, 'com.chinasofti.rcs:id/get_mian_liu_permission'),
        'com.chinasofti.rcs:id/pop_window_not_pop_btn_image': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_not_pop_btn_image'),
        '以后不再提示': (MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_not_pop_btn')
    }

    @TestLogger.log('继续拨打')
    def click_go_on(self):
        self.click_element(self.__locators['继续拨打'])

    @TestLogger.log('以后不再提示')
    def check_no_more_prompts(self):
        checked_color = (0, 0, 255, 255)
        uncheck_color = (255, 255, 255, 255)
        rgba_before_click = self.mobile.get_coordinate_color_of_element(
            self.__locators['com.chinasofti.rcs:id/pop_window_not_pop_btn_image'], x=50, y=50, by_percent=True)
        print(rgba_before_click)
        if rgba_before_click == uncheck_color:
            self.click_element(self.__locators['以后不再提示'])
        rgba_after_click = self.mobile.get_coordinate_color_of_element(
            self.__locators['com.chinasofti.rcs:id/pop_window_not_pop_btn_image'], x=50, y=50, by_percent=True)
        return rgba_after_click

    @TestLogger.log('勾选“以后不再提示”')
    def check_no_more_prompts(self):
        # checked_color = (0, 0, 255, 255)
        uncheck_color = (255, 255, 255, 255)
        rgba_before_click = self.mobile.get_coordinate_color_of_element(
            self.__locators['com.chinasofti.rcs:id/pop_window_not_pop_btn_image'], x=50, y=50, by_percent=True)
        print(rgba_before_click)
        if rgba_before_click == uncheck_color:
            self.click_element(self.__locators['以后不再提示'])
        rgba_after_click = self.mobile.get_coordinate_color_of_element(
            self.__locators['com.chinasofti.rcs:id/pop_window_not_pop_btn_image'], x=50, y=50, by_percent=True)
        return rgba_after_click

    @TestLogger.log('去勾选“以后不再提示”')
    def check_no_more_prompts(self):
        # checked_color = (0, 0, 255, 255)
        uncheck_color = (255, 255, 255, 255)
        rgba_before_click = self.mobile.get_coordinate_color_of_element(
            self.__locators['com.chinasofti.rcs:id/pop_window_not_pop_btn_image'], x=50, y=50, by_percent=True)
        print(rgba_before_click)
        if rgba_before_click != uncheck_color:
            self.click_element(self.__locators['以后不再提示'])
        rgba_after_click = self.mobile.get_coordinate_color_of_element(
            self.__locators['com.chinasofti.rcs:id/pop_window_not_pop_btn_image'], x=50, y=50, by_percent=True)
        return rgba_after_click

    @TestLogger.log('点击“订购免流特权”')
    def ordering_free_flow_privileges(self):
        self.click_element(self.__locators['订购免流特权'])

    @TestLogger.log('点击“订购免流特权”')
    def ordering_free_flow_privileges(self):
        self.click_element(self.__locators['订购免流特权'])

    @TestLogger.log('如果弹出提示对话框，点击继续')
    def go_on_if_tips_pop_out(self):
        try:
            self.click_go_on()
        except:
            print('没有提示框，或者没找到提示框')
