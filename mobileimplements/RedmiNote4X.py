import re

from appium.webdriver.common.mobileby import MobileBy

from library.core.TestLogger import TestLogger
from library.core.common.simcardtype import CardType
from library.core.mobile.mobiledriver import MobileDriver


class RedmiNote4X(MobileDriver):
    """红米 Note 4X"""

    def supported_card_types(self):
        return [
            CardType.CHINA_MOBILE,
            CardType.CHINA_UNION,
            CardType.CHINA_TELECOM,
        ]

    def total_card_slot(self):
        return 2

    def _actions_before_send_get_code_request(self):
        """打开通知栏并清空消息"""
        self.open_notifications()
        # 点击清空通知按钮
        if self._is_element_present((MobileBy.ID, 'com.android.systemui:id/clear_all_button')):
            self.click_element((MobileBy.ID, 'com.android.systemui:id/clear_all_button'))
        # self.back()

    def _actions_after_send_get_code_request(self, context, max_wait_time):
        self.open_notifications()
        message = self.wait_until(
            condition=lambda d: self.get_text((MobileBy.XPATH, '//*[contains(@text,"登录验证")]')),
            timeout=max_wait_time
        )
        code = re.findall(r'【登录验证】尊敬的用户：(\d+)', message)
        self.back()
        if code:
            return code[0]
        raise Exception("等待{}秒仍未获取到验证码".format(max_wait_time))

    @TestLogger.log('获取手机型号')
    def get_mobile_model_info(self):
        try:
            result = self.execute_shell_command('getprop', 'ro.product.model')
        except:
            result = "暂无信息"
        return result.strip()
