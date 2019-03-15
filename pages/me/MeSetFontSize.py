from appium.webdriver.common.mobileby import MobileBy


from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeSetFontSizePage(BasePage):
    """我-》设置-》设置字体大小"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.FontSettingActivity'

    __locators = {
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/title_bar': (MobileBy.ID, 'com.chinasofti.rcs:id/title_bar'),
                'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                    MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                '设置字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                '确认': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_send'),
                'com.chinasofti.rcs:id/text_font_group1': (MobileBy.ID, 'com.chinasofti.rcs:id/text_font_group1'),
                '预览字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/font_size_text'),
                'com.chinasofti.rcs:id/font_setting_avatar_view': (
                    MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_avatar_view'),
                'com.chinasofti.rcs:id/text_font_group2': (MobileBy.ID, 'com.chinasofti.rcs:id/text_font_group2'),
                '拖动下面的滑动，可设置字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/font_size_text_2'),
                'com.chinasofti.rcs:id/font_setting_avatar_view_2': (
                    MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_avatar_view_2'),
                'com.chinasofti.rcs:id/text_font_group3': (MobileBy.ID, 'com.chinasofti.rcs:id/text_font_group3'),
                '设置好，会改变聊天，菜单的字体大小。如果在使用过程中存在问题和意见，可反馈给我们团队': (MobileBy.ID, 'com.chinasofti.rcs:id/font_size_text_3'),
                'com.chinasofti.rcs:id/font_setting_avatar_view_3': (
                    MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_avatar_view_3'),
                'com.chinasofti.rcs:id/font_size_setting_view': (
                    MobileBy.ID, 'com.chinasofti.rcs:id/font_size_setting_view'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground')
                }

    @TestLogger.log('鼠标点击操作')
    def target_click(self, x1, y1):  # x1,y1为你编写脚本时适用设备的实际坐标
        x_1 = x1 / 1080  # 计算坐标在横坐标上的比例，其中375为iphone6s的宽
        y_1 = y1 / 2250  # 计算坐标在纵坐标667为iphone6s的高
        x = self.driver.get_window_size()['width']  # 获取设备的屏幕宽度
        y = self.driver.get_window_size()['height']  # 获取设备屏幕的高度
        self.driver.tap([(x_1 * x, y_1 * y)], 500)  # 模拟单手点击操作

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待聊天语音页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["设置字体大小"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('点击确认')
    def click_sure(self):
        self.click_element(self.__locators["确认"])
