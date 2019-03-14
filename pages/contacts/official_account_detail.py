from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from .components.menu_more import MenuMore


class OfficialAccountDetailPage(MenuMore, BasePage):
    """公众号详情"""
    ACTIVITY = 'com.rcs.rcspublicaccount.PublicAccountDetailActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '公众号名称': (MobileBy.ID, 'com.chinasofti.rcs:id/public_name'),
        '更多菜单': (MobileBy.ID, 'com.chinasofti.rcs:id/menu_more'),
        'com.chinasofti.rcs:id/public_scrollview_detail': (
            MobileBy.ID, 'com.chinasofti.rcs:id/public_scrollview_detail'),
        'com.chinasofti.rcs:id/public_header': (MobileBy.ID, 'com.chinasofti.rcs:id/public_header'),
        '公共账号：4011020490': (MobileBy.ID, 'com.chinasofti.rcs:id/public_account'),
        'com.chinasofti.rcs:id/public_introduction': (MobileBy.ID, 'com.chinasofti.rcs:id/public_introduction'),
        '功能介绍': (MobileBy.ID, 'com.chinasofti.rcs:id/intro_title'),
        '介绍整形美容知识，介绍美容整形情况！': (MobileBy.ID, 'com.chinasofti.rcs:id/intro_text'),
        'com.chinasofti.rcs:id/rl_public_auth': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_public_auth'),
        '认证主体': (MobileBy.ID, 'com.chinasofti.rcs:id/public_auth_text'),
        'com.chinasofti.rcs:id/public_auth_image': (MobileBy.ID, 'com.chinasofti.rcs:id/public_auth_image'),
        'com.chinasofti.rcs:id/ll_accept_message_push': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_accept_message_push'),
        '接收消息推送': (MobileBy.ID, ''),
        '开启': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_receive'),
        'com.chinasofti.rcs:id/ll_totop': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_totop'),
        '置顶公众号': (MobileBy.ID, ''),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_totop'),
        'com.chinasofti.rcs:id/ll_history_message': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_history_message'),
        '查看历史资讯': (MobileBy.ID, ''),
        'com.chinasofti.rcs:id/my_group_name_right_arrow': (
            MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name_right_arrow'),
        '进入公众号': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_into_public'),
        '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
        '输入框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
        '表情': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
        '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'),
        '键盘': (MobileBy.ID, 'com.chinasofti.rcs:id/conversation_bottom_showCustomMenuView'),
        '底部菜单1': (MobileBy.ID, 'com.chinasofti.rcs:id/public_menu_name1'),
        '底部菜单2': (MobileBy.ID, 'com.chinasofti.rcs:id/public_menu_name2'),
        '底部菜单3': (MobileBy.ID, 'com.chinasofti.rcs:id/public_menu_name3'),
        '菜单1的菜单详情列表1': (MobileBy.ID, 'com.chinasofti.rcs:id/public_item_menu_name1'),
        '页面详情点击返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '表情详情': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_expression_image"]'),
        '发送内容': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message"]'),
        '回复内容': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message"]'),
        '不成功图标':(MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
        '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
    }

    @TestLogger.log('点击返回')
    def click_menu_more(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击打开更多菜单')
    def click_menu_more(self):
        self.click_element(self.__locators['更多菜单'])

    @TestLogger.log()
    def send_btn_is_clickable(self):
        """发送按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators["发送"])

    @TestLogger.log()
    def page_should_contain_element_setting(self):
        """页面应该包含设置按钮"""
        return self.page_should_contain_element(self.__locators["设置"])

    @TestLogger.log()
    def page_should_contain_element_input(self):
        """页面应该包含输入框"""
        return self.page_should_contain_element(self.__locators["输入框"])

    @TestLogger.log()
    def page_should_contain_element_expression(self):
        """页面应该包含表情按钮"""
        return self.page_should_contain_element(self.__locators["表情"])

    @TestLogger.log()
    def page_should_contain_element_send(self):
        """页面应该包含发送按钮"""
        return self.page_should_contain_element(self.__locators["发送"])

    @TestLogger.log()
    def page_should_contain_element_keyboard(self):
        """页面应该包含键盘"""
        return self.page_should_contain_element(self.__locators["键盘"])

    @TestLogger.log()
    def page_should_contain_element_menu(self):
        """页面应该包含底部菜单栏"""
        return self.page_should_contain_element(self.__locators["底部菜单1"])

    @TestLogger.log('点击键盘')
    def click_keyboard(self):
        self.click_element(self.__locators['键盘'])

    @TestLogger.log('底部菜单栏1')
    def click_menu_name1(self):
        self.click_element(self.__locators['底部菜单1'])

    @TestLogger.log('菜单1的菜单详情列表1')
    def click_menu_detail_name1(self):
        self.click_element(self.__locators['菜单1的菜单详情列表1'])

    @TestLogger.log('页面详情点击返回')
    def click_menu_detail_back(self):
        self.click_element(self.__locators['页面详情点击返回'])

    @TestLogger.log('点击输入框')
    def click_input_box(self):
        self.click_element(self.__locators['输入框'])

    @TestLogger.log('输入内容')
    def input_keyword(self, keyword):
        """输入文本内容"""
        self.input_text(self.__locators['输入框'], keyword)

    @TestLogger.log()
    def click_expression(self):
        """点击表情"""
        self.click_element(self.__locators['表情'])

    @TestLogger.log()
    def click_send(self):
        """点击发送文本"""
        self.click_element(self.__locators['发送'])

    @TestLogger.log()
    def click_expression_detail(self):
        """点击表情详情"""
        self.click_element(self.__locators['表情详情'])

    @TestLogger.log()
    def click_send_detail(self,text):
        """点击发送的内容"""
        self.click_text(text)

    @TestLogger.log()
    def page_should_contain_element_unsent(self):
        """页面应该包含未发送成功图标"""
        return self.page_should_contain_element(self.__locators["不成功图标"])

    @TestLogger.log()
    def click_element_unsent(self):
        """点击未发送成功图标"""
        self.click_element(self.__locators['不成功图标'])

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
        self.page_should_not_contain_element(self.__locators['不成功图标'])