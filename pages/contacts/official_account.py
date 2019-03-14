from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class OfficialAccountPage(BasePage):
    """公众号"""
    ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountsListActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '公众号': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
        '加号': (MobileBy.ID, 'com.chinasofti.rcs:id/menu_add_btn'),
        '订阅/服务号': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_tab_title" and @text="订阅/服务号"]'),
        '企业号': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_tab_title" and @text="企业号"]'),

        '公众号列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '公众号列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView"]/*'),
        '公众号头像': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_user_photo'),
        '公众号名称': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_user_name'),
        '公众号描述': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_user_info'),
        '未关注任何企业号': (MobileBy.ID, 'com.chinasofti.rcs:id/empty_hint_view'),
        '订阅/服务号': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tab_title'),
        '和飞信': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_user_name'),
        '和飞信团队': (MobileBy.XPATH, '//*[@text="和飞信团队"]'),
        '和飞信新闻': (MobileBy.XPATH, '//*[@text="和飞信新闻"]'),
        '中国移动10086': (MobileBy.XPATH, '//*[@text="中国移动10086"]'),
        'input_box': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
        'send_button': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'),
        'setting': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
        'expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
        'expression_keyboard': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression_keyboard'),
        '发送失败': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
        '[微笑1]': (MobileBy.XPATH, '//*[@text="[微笑1]"]'),
        '信息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
        '删除': (MobileBy.XPATH, '//*[@text="删除"]'),
        '收藏': (MobileBy.XPATH, '//*[@text="收藏"]'),
        '转发': (MobileBy.XPATH, '//*[@text="转发"]'),
        '复制': (MobileBy.XPATH, '//*[@text="复制"]'),

    }

    @TestLogger.log('点击添加')
    def click_add(self):
        self.click_element(self.__locators['加号'])

    @TestLogger.log('点击tag标签')
    def click_tag(self, tag_name):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/tv_tab_title" and @text="{}"]'.format(tag_name)]
        self.click_element(locator)

    @TestLogger.log('检查企业号列表是否为空')
    def assert_enterprise_account_list_is_empty(self):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators['未关注任何企业号'])
            )
            self.element_text_should_be(
                self.__locators['未关注任何企业号'],
                '未关注任何企业号', '检查点：列表为空时显示默认文案：未关注任何企业号'
            )
        except TimeoutException:
            raise AssertionError("检查点：企业号列表为空")

    @TestLogger.log("setting")
    def page_contain_setting(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['setting'])

    @TestLogger.log("input_box")
    def page_contain_input_box(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['input_box'])

    @TestLogger.log("send_button")
    def page_contain_send_button(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['send_button'])

    @TestLogger.log("expression")
    def page_contain_expresssion(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['expression'])

    @TestLogger.log("和飞信新闻")
    def page_contain_news(self):
        """检查该页面是否包含某元素"""
        return self.page_should_contain_element(self.__locators['和飞信新闻'])

    @TestLogger.log('检查发送失败按钮')
    def page_should_not_contain_sendfail_element(self):
        return self.page_should_not_contain_element(self.__locators['发送失败'])

    @TestLogger.log('使用坐标点击')
    def click_coordinate(self, x=1300, y=2450):
        # width = self.driver.get_window_size()["width"]
        # height = self.driver.get_window_size()["height"]

        # x_start = float(x) / 100 * width
        # y_end = float(y) / 100 * width
        x_start = x
        y_end = y
        self.tap_coordinate([(x_start, y_end)])

    @TestLogger.log('和飞信')
    def click_officel_account(self):
        self.click_element(self.__locators['和飞信新闻'], 30)

    @TestLogger.log('点击输入框')
    def click_input_box(self):
        self.click_element(self.__locators['input_box'])

    @TestLogger.log('点击发送')
    def click_send_button(self):
        self.click_element(self.__locators['send_button'])

    @TestLogger.log('输入框信息')
    def input_message(self, text='good news'):
        self.input_text(self.__locators['input_box'], text)

    @TestLogger.log('点击表情按钮')
    def click_expression(self, text='expression'):
        self.click_element(self.__locators[text])

    @TestLogger.log('删除信息')
    def remove_message(self):
        if self.page_should_contain_element(self.__locators['信息']):
            self.click_element(self.__locators['信息'])
            el = self.get_element(self.__locators['信息'])
            self.driver.long_press(el, 1, 1, 2000)
