from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.TestLogger import TestLogger
from library.core.common.simcardtype import CardType
from library.core.mobile.mobiledriver import MobileDriver


class HuaweiP20(MobileDriver):
    """HUAWEI P20"""

    def supported_card_types(self):
        return [
            CardType.CHINA_MOBILE,
            CardType.CHINA_UNION,
            CardType.CHINA_TELECOM,
        ]

    def total_card_slot(self):
        return 2

    @TestLogger.log('获取手机型号')
    def get_mobile_model_info(self):
        try:
            result = self.execute_shell_command('getprop', 'ro.config.marketing_name')
        except:
            result = "暂无信息"
        return result.strip()

    @TestLogger.log('开启飞行模式')
    def turn_on_airplane_mode(self):
        """
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.AIRPLANE_MODE_SETTINGS 打开WIFI设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        params = 'settings put global airplane_mode_on 1'.split(' ')
        params1 = 'am broadcast -a android.intent.action.AIRPLANE_MODE'.split(' ')
        self.execute_shell_command(*params)
        self.execute_shell_command(*params1)
        return True

    @TestLogger.log('关闭飞行模式')
    def turn_off_airplane_mode(self):
        """
        由于appium set_network_connection接口不靠谱，所有有关网络状态的设置需要在UI层面操作
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.AIRPLANE_MODE_SETTINGS 打开WIFI设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """

        params = 'settings put global airplane_mode_on 0'.split(' ')
        params1 = 'am broadcast -a android.intent.action.AIRPLANE_MODE'.split(' ')
        self.execute_shell_command(*params)
        self.execute_shell_command(*params1)
        return True

    @TestLogger.log('开启WIFI')
    def turn_on_wifi(self):
        """
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.WIFI_SETTINGS 打开WIFI设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        params = 'am start -a android.settings.WIFI_SETTINGS'.split(' ')
        self.execute_shell_command(*params)
        switch_locator = [MobileBy.XPATH, '//android.widget.Switch']
        if self.get_element_attribute(switch_locator, 'checked', 5) == 'false':
            self.click_element(switch_locator, auto_accept_permission_alert=False)
        try:
            self.wait_until(
                condition=lambda d: self.get_element_attribute(switch_locator, 'checked') == 'true',
                auto_accept_permission_alert=False
            )
        except TimeoutException:
            print(self.get_element_attribute(switch_locator, 'checked'))
            raise RuntimeError('开关的checked属性没有置为"true"')
        # try:
        #     self.wait_until(
        #         condition=lambda d: self.is_text_present('已连接'),
        #         timeout=30,
        #         auto_accept_permission_alert=False
        #     )
        # except TimeoutException:
        #     raise RuntimeError('手机WIFI 已开启，但没有自动连接到 WIFI 热点')
        self.back()
        return True

    @TestLogger.log('关闭WIFI')
    def turn_off_wifi(self):
        """
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.WIFI_SETTINGS 打开WIFI设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        params = 'am start -a android.settings.WIFI_SETTINGS'.split(' ')
        self.execute_shell_command(*params)
        switch_locator = [MobileBy.XPATH, '//android.widget.Switch']
        if self.get_element_attribute(switch_locator, 'checked', 5) == 'true':
            self.click_element(switch_locator, auto_accept_permission_alert=False)
        try:
            self.wait_until(
                condition=lambda d: self.get_element_attribute(switch_locator, 'checked') == 'false',
                auto_accept_permission_alert=False
            )
        except TimeoutException:
            print(self.get_element_attribute(switch_locator, 'checked'))
            raise RuntimeError('开关的checked属性没有置为"false"')
        self.back()
        return True
