import re

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class OneKeyLoginPage(BasePage):
    """一键登录页"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.OneKeyLoginActivity'

    __locators = {
        "电话号码": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        "一键登录": (MobileBy.ID, 'com.chinasofti.rcs:id/one_key_login'),
        "切换另一号码登录": (MobileBy.ID, "com.chinasofti.rcs:id/change_to_smslogin"),
        "已阅读并同意复选框": (MobileBy.ID, "com.chinasofti.rcs:id/agreement_checkbox"),
        "客户端头像": (MobileBy.ID, "com.chinasofti.rcs:id/login_iron"),
        "和飞信软件许可及服务协议": (MobileBy.ID, "com.chinasofti.rcs:id/agreement_text"),
        '提示内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        '查看详情': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_check_detail'),
        '语言': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_language'),
        '用户协议与隐私保护': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_dialog_title'),
    }

    @TestLogger.log()
    def click_language(self):
        """点击语言"""
        self.click_element(self.__locators["语言"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在一键登录页"""
        el = self.get_elements(self.__locators['一键登录'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def assert_phone_number_equals_to(self, phone_number):
        """等待手机号读取成功"""
        self.element_text_should_be(self.__locators["电话号码"], phone_number)
        return self

    @TestLogger.log()
    def click_one_key_login(self):
        """点击一键登录"""
        self.click_element(self.__locators["一键登录"])

    @TestLogger.log()
    def have_read_agreement_detail(self):
        """是否弹出 查看详情"""
        try:
            self.wait_until(
                timeout=3,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["查看详情"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def have_read_agreement_detail_631(self):
        """是否弹出 用户协议与隐私保护（6.3.1版本）"""
        try:
            self.wait_until(
                timeout=3,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["用户协议与隐私保护"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_read_agreement_detail(self):
        """点击查看详情"""
        self.click_element(self.__locators['查看详情'])

    @TestLogger.log()
    def choose_another_way_to_login(self):
        """选择验证码登录"""
        self.click_element(self.__locators["切换另一号码登录"])

    @TestLogger.log()
    def check_the_agreement(self):
        """勾选我已阅读XXX协议复选框"""
        self.select_checkbox(self.__locators["已阅读并同意复选框"])
        self.checkbox_should_be_selected(self.__locators["已阅读并同意复选框"])
        return self

    @TestLogger.log()
    def uncheck_the_agreement(self):
        """去勾选我已阅读XXX协议复选框"""
        self.unselect_checkbox(self.__locators["已阅读并同意复选框"])
        self.checkbox_should_not_be_selected(self.__locators["已阅读并同意复选框"])
        return self

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待一键登录页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["一键登录"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_login_number(self, specify_card_slot=0):
        """获取一键登录界面的电话号码"""
        number = self.get_text(self.__locators['电话号码'])
        if number and re.match(r'^\d+$', number.strip()):
            return number
        else:
            print('一键登录页面可能加载手机号失败（{}），改为从配置获取手机号'.format(number))
            card_type, number = self.mobile.get_card(specify_card_slot)
            del card_type
            return number

    @TestLogger.log()
    def wait_for_tell_number_load(self, timeout=60, auto_accept_alerts=True):
        """等待一键登录页面的‘将以本机号码登录’变成 手机号码 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_text_match(self.__locators["电话号码"], r"\d+", regex=True)
            )
        except:
            message = "电话号码在{}s内，没有加载成功".format(timeout)
            print('Warn: ' + message)
        return self

    @TestLogger.log()
    def click_client_logo_pic(self):
        """点击客户端头像"""
        self.click_element(self.__locators["客户端头像"])

    @TestLogger.log()
    def click_license_agreement(self):
        """点击和飞信软件许可及服务协议"""
        self.click_element(self.__locators["和飞信软件许可及服务协议"])

    @TestLogger.log()
    def wait_one_key_or_sms_login_page_load(self, timeout=20):
        def determine_login_page(d):
            if self.get_elements(self.__locators['一键登录']):
                return 'one_key'
            elif self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/edt_phone_number')):
                return 'sms'
            else:
                return False

        try:
            page_name = self.wait_until(
                condition=determine_login_page,
                timeout=timeout
            )
            return page_name
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )

    @TestLogger.log()
    def page_should_contain_client_logo_pic(self):
        """登录页客户端头像检查"""
        self.page_should_contain_element(self.__locators["客户端头像"])

    @TestLogger.log('关闭应用')
    def kill_flyme_app(self):
        self.execute_shell_command('am','force','-stop','com.chinasofti.rcs')

    @TestLogger.log('点按手机Home键')
    def press_home_key(self,times=1):
        try:
            for i in range(times):
                self.execute_shell_command('input','keyevent',3)
            return
        except:
            raise NotImplementedError('该API不支持android/ios以外的系统')