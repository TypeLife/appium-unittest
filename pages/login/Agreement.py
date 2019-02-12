from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AgreementPage(BasePage):
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.AgreementActivity'
    locators = {}

    @TestLogger.log()
    def wait_for_license_agreement_load(self, timeout=10, auto_accept_alerts=True):
        """等待 和飞信软件许可及服务协议 加载"""
        text = """和飞信业务是中国移动提供的个人通信服务升级及移动办公应用服务，用户首次登录和飞信客户端即表示同意开通本业务，本业务不收取订购费用。如使用和飞信进行发送短信、拨打电话等功能可能会收取一定的费用。"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present(text)
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self
