from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupListPage(BasePage):
    """群组列表"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatListActivity2'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),

        '群聊': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '新建群组': (MobileBy.ID, 'com.chinasofti.rcs:id/menu_add_btn'),
        '搜索群组': (MobileBy.XPATH, '//*[contains(@resource-id,"search")]'),
        'com.chinasofti.rcs:id/fragment_container': (MobileBy.ID, 'com.chinasofti.rcs:id/fragment_container'),
        '群列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '列表项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
        '列表项首字母': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index'),
        '群名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '滚动条字符': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/*'),
        '标题新建分组': (MobileBy.ID, 'com.chinasofti.rcs:id/label_toolbar_title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '为你的分组创建一个名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sub_title'),
        '请输入标签分组名称': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_group_name'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '标签分组': (MobileBy.ID, 'com.chinasofti.rcs:id/second_item'),
        '新建分组':(MobileBy.ID,'com.chinasofti.rcs:id/group_name'),
        '知道了':(MobileBy.ID,'com.chinasofti.rcs:id/btn_cancel'),
        '设置':(MobileBy.ID,'com.chinasofti.rcs:id/iv_label_setting'),
        '删除标签':(MobileBy.XPATH,'//*[@text="删除标签"]'),
        '刪除按钮':(MobileBy.ID,'com.chinasofti.rcs:id/btn_ok'),
        'back_contact':(MobileBy.ID,'com.chinasofti.rcs:id/back'),
        'back_gouppage':(MobileBy.ID,'com.chinasofti.rcs:id/rl_label_left_back'),

    }


    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击创建群')
    def click_create_group(self):
        self.click_element(self.__locators['新建群组'])

    @TestLogger.log('搜索群')
    def click_search_input(self):
        self.click_element(self.__locators['搜索群组'])

    @TestLogger.log('判断列表是否存在群XXX')
    def is_group_in_list(self, name):
        groups = self.mobile.list_iterator(self.__locators['群列表'], self.__locators['列表项'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH,
                                   '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log('点击群')
    def click_group(self, name):
        if self.is_group_in_list(name):
            self.click_element((MobileBy.XPATH,
                                '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                '@text="{}"]'.format(name)))
        else:
            raise NoSuchElementException('找不到群：{}'.format((MobileBy.XPATH,
                                                           '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                                           '@text="{}"]'.format(name))))

    @TestLogger.log('等待群聊列表页面加载')
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['新建群组']),
            timeout=timeout,
            auto_accept_permission_alert=auto_accept_alerts
        )

    @TestLogger.log('创建群聊')
    def create_group_chats_if_not_exits(self, name, members_list):
        """
        导入群聊数据
        :param members_list:
        :param name:
        :return:
        """

        self.click_search_input()

        from pages import GroupListSearchPage
        group_search = GroupListSearchPage()
        group_search.input_search_keyword(name)
        if group_search.is_group_in_list(name):
            group_search.click_back()
        else:
            group_search.click_back()

            self.click_create_group()

            from pages import SelectContactPage
            select_page = SelectContactPage()
            select_page.search_and_select_contact(*members_list)

            from pages import BuildGroupChatPage
            build_page = BuildGroupChatPage()
            build_page.create_group_chat(name)

            from pages import ChatWindowPage
            chat = ChatWindowPage()
            if chat.is_tips_display():
                chat.directly_close_tips_alert()
            chat.wait_for_page_load()
            chat.click_back()

    @TestLogger.log()
    def click_label_grouping(self):
        """点击标签分组1"""
        self.click_element(self.__class__.__locators['标签分组'])

    @TestLogger.log()
    def open_contacts_page(self):
        """切换到标签页：通讯录"""
        self.click_element(self.__locators['通讯录'])

    @TestLogger.log()
    def check_if_contains_element(self,text="确定"):
        '''检查指定元素是否存在，默认是确定按钮'''
        return self.page_should_contain_element(self.__locators['确定'])

    @TestLogger.log("点击确定")
    def click_sure_element(self):
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log("点击新建分组")
    def click_new_group(self):
        self.click_element(self.__class__.__locators['新建分组'])

    @TestLogger.log("点击输入框")
    def click_input_element(self):
        self.click_element(self.__class__.__locators['请输入标签分组名称'])

    @TestLogger.log("输入内容")
    def input_content(self,text='祝一路顺风幸福美满'):
        self.input_text(self.__class__.__locators['请输入标签分组名称'],text)

    @TestLogger.log('使用坐标点击')
    def click_coordinate(self, x=1/2, y=15/16):

        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        print("width : ",width,height)
        x_start = width*x
        y_end = height*y
        self.tap_coordinate([(x_start, y_end)])

    @TestLogger.log('删除分组标签')
    def delete_group(self,name='祝一路顺风幸福美满'):
        if self.is_text_present(name):
            self.click_text(name)
            self.click_element(self.__class__.__locators['知道了'])
            self.click_element(self.__class__.__locators['设置'])
            self.click_element(self.__class__.__locators['删除标签'])
            self.click_element(self.__class__.__locators['刪除按钮'])
        else:
            print('标签不存在')

    @TestLogger.log('返回按钮')
    def click_back_button(self):
        try:
            self.click_element(self.__class__.__locators['back_contact'])
        except :
            self.click_element(self.__class__.__locators['back_gouppage'])


