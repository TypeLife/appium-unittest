from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class CreateTeamPage(BasePage):
    """创建团队页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/rl_webview_content': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_webview_content'),
        'com.chinasofti.rcs:id/actionbar_main_enterprise': (
        MobileBy.ID, 'com.chinasofti.rcs:id/actionbar_main_enterprise'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '创建团队': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '请输入团队名称': (MobileBy.ID, 'qy_name'),
        '选择行业': (MobileBy.XPATH, '//*[@content-desc="选择行业"]'),
        '选择所在地': (MobileBy.XPATH, '//*[@content-desc="选择所在地"]'),
        '请务必填写真实姓名': (MobileBy.ID, 'gly_name'),
        '14775290489@139.com': (MobileBy.ID, 'gly_email'),
        '立即创建团队': (MobileBy.XPATH, '//*[@content-desc="立即创建团队"]'),
        # 创建成功后页面
        '创建成功': (MobileBy.XPATH, '//*[@content-desc="创建成功"]'),
        '登录后台可体验更全面的管理功能': (MobileBy.XPATH, '//*[@content-desc="登录后台可体验更全面的管理功能"]'),
        '进入工作台': (MobileBy.XPATH, '//*[@content-desc="进入工作台"]'),
        # 未输入姓名时的弹窗提示
        '请输入管理员姓名': (MobileBy.XPATH, '//*[@content-desc="请输入管理员姓名"]'),
        '确定': (MobileBy.XPATH, '//*[@content-desc="确定"]'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 创建团队页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("立即创建团队")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_enter_workbench(self):
        """点击进入工作台"""
        self.click_element(self.__class__.__locators['进入工作台'])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def choose_location(self, city="北京市", area="西城"):
        """选择所在地"""
        self.click_element(self.__class__.__locators['选择所在地'])
        try:
            self.click_element((MobileBy.XPATH, '//*[@content-desc="%s"]' % city))
        except:
            self.click_element((MobileBy.XPATH, '//*[@content-desc="选择地区"]/../android.view.View/android.view.View[1]'))
        try:
            self.click_element((MobileBy.XPATH, '//*[@content-desc="%s"]' % area))
        except:
            self.click_element((MobileBy.XPATH, '//*[@content-desc="上一级"]/../android.view.View/android.view.View[1]'))

    @TestLogger.log()
    def choose_industry(self, hy="计算机软件"):
        """选择行业"""
        self.click_element(self.__class__.__locators['选择行业'])
        try:
            self.click_element((MobileBy.XPATH, '//*[@content-desc="%s"]' % hy))
        except:
            self.click_element((MobileBy.XPATH, '//*[@content-desc="选择行业"]/../android.view.View/android.view.View[2]'))

    @TestLogger.log()
    def input_team_name(self, name):
        """输入团队名字"""
        self.input_text(self.__class__.__locators["请输入团队名称"], name)

    @TestLogger.log()
    def input_real_name(self, name):
        """输入真实姓名"""
        self.input_text(self.__class__.__locators["请务必填写真实姓名"], name)

    @TestLogger.log()
    def click_immediately_create_team(self):
        """点击立即创建团队"""
        self.click_element(self.__class__.__locators['立即创建团队'])
