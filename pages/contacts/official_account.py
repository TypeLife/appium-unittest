import time
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
        '和飞信2': (MobileBy.XPATH, '//*[@text="和飞信"]'),

        '键盘': (MobileBy.ID, 'com.chinasofti.rcs:id/conversation_bottom_showCustomMenuView'),
        '底部菜单1': (MobileBy.ID, 'com.chinasofti.rcs:id/public_menu_name1'),
        '底部菜单2': (MobileBy.ID, 'com.chinasofti.rcs:id/public_menu_name2'),
        '底部菜单3': (MobileBy.ID, 'com.chinasofti.rcs:id/public_menu_name3'),
        '菜单1的菜单详情列表1': (MobileBy.ID, 'com.chinasofti.rcs:id/public_item_menu_name1'),
        '页面详情点击返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '表情详情': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_expression_image"]'),
        'message': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message"]'),
        '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
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


    @TestLogger.log()
    def select_one_account_by_name(self, name):
        """通过名称选择一个公众号"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/textview_user_name" and @text ="%s"]' % name))

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

    @TestLogger.log()
    def send_btn_is_clickable(self):
        """发送按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators["send_button"])

    @TestLogger.log()
    def page_contain_keyboard(self):
        """页面应该包含键盘"""
        return self.page_should_contain_element(self.__locators["键盘"])

    @TestLogger.log()
    def page_should_contain_element_menu(self):
        """页面应该包含底部菜单栏"""
        return self.page_should_contain_element(self.__locators["底部菜单1"])

    @TestLogger.log('底部菜单栏1')
    def click_menu_name1(self):
        self.click_element(self.__locators['底部菜单1'])

    @TestLogger.log('菜单1的菜单详情列表1')
    def click_menu_detail_name1(self):
        self.click_element(self.__locators['菜单1的菜单详情列表1'])

    @TestLogger.log('页面详情点击返回')
    def click_menu_detail_back(self):
        self.click_element(self.__locators['页面详情点击返回'])

    @TestLogger.log('点击键盘')
    def click_keyboard(self):
        self.click_element(self.__locators['键盘'])

    @TestLogger.log()
    def click_expression_detail(self):
        """点击表情详情"""
        self.click_element(self.__locators['表情详情'])

    @TestLogger.log()
    def click_send_detail(self, text):
        """点击发送的内容"""
        self.click_text(text)

    @TestLogger.log()
    def page_should_contain_element_unsent(self):
        """页面应该包含未发送成功图标"""
        return self.page_should_contain_element(self.__locators["发送失败"])

    @TestLogger.log()
    def click_element_unsent(self):
        """点击未发送成功图标"""
        self.click_element(self.__locators['发送失败'])

    @TestLogger.log()
    def click_sure_resent(self):
        """点击确定重发"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def click_not_resent(self):
        """点击取消重发"""
        self.click_element(self.__locators['取消'])

    @TestLogger.log()
    def page_not_contain_element_unsent(self):
        """页面不存在未发送成功图标"""
        self.page_should_not_contain_element(self.__locators['发送失败'])

    @TestLogger.log()
    def click_setting(self):
        """点击设置"""
        self.click_element(self.__locators['setting'])

    @TestLogger.log()
    def page_contain_element_message(self):
        """页面应该包含信息"""
        return self.page_should_contain_element(self.__locators["message"])

    @TestLogger.log()
    def page_not_contain_element_message(self):
        """页面不应该包含信息"""
        return self.page_should_not_contain_element(self.__locators["message"])

    @TestLogger.log('查看是否显示公众号')
    def is_public_in_list(self, name):
        time.sleep(1)
        groups = self.mobile.list_iterator(self.__locators['公众号列表'], self.__locators['公众号列表项'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/textview_user_name" and ' +
                                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log()
    def is_element_present_message(self):
        return self._is_element_present(self.__locators["message"])