from xml.sax import saxutils

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SearchPage(BasePage):
    """快速搜索"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.SearchActivity'

    __locators = {
        '返回上一页': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'),
        '输入关键词快速搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query01'),
        '搜索结果列表': (MobileBy.ID, 'com.chinasofti.rcs:id/single_result_list'),
        '删除搜索框文本按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect01'),
        '搜索和通讯录联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/content'),
        '联系人分割线': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '联系人项列表项': (MobileBy.ID, 'com.chinasofti.rcs:id/root_view'),
        '联系人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
        '联系人名字': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
        '联系人号码': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_phone'),

        '公众号分割线': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '公众号列表项': (MobileBy.XPATH, '//android.widget.RelativeLayout[*[@resource-id="com.chinasofti.rcs:id/svd_head"]]'),
        '公众号头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '公众号名字': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
    }

    @TestLogger.log("点击返回")
    def click_back_button(self):
        """点击返回"""
        self.click_element(self.__locators['返回上一页'])

    @TestLogger.log("搜索和通讯录联系人")
    def click_search_contacts(self):
        """搜索和通讯录联系人"""
        self.click_element(self.__locators['搜索和通讯录联系人'])

    @TestLogger.log('输入搜索关键字')
    def input_search_keyword(self, keyword):
        """输入搜索关键字"""
        self.input_text(self.__locators['输入关键词快速搜索'], keyword)

    @TestLogger.log('检查搜索到的联系人名字')
    def assert_contact_name_display(self, name, timeout=0):
        """检查搜索到的联系人名字"""
        locator = [MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="{}"]'.format(
            saxutils.escape(name, {"'": "&apos;", '"': "&quot;"}))]
        try:
            self.wait_until(
                condition=lambda d: self.get_elements(locator),
                timeout=timeout
            )
        except:
            raise AssertionError("找不到名字等于：{}的联系人".format(name))

    @TestLogger.log('检查搜索到的号码')
    def assert_contact_number_display(self, number, timeout=0):
        """检查搜索到的号码"""
        locator = [MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_phone" and @text="{}"]'.format(
            saxutils.escape(number, {"'": "&apos;", '"': "&quot;"}))]
        try:
            self.wait_until(
                condition=lambda d: self.get_elements(locator),
                timeout=timeout
            )
        except:
            raise AssertionError("找不到号码等于：{}的联系人".format(number))

    @TestLogger.log("点击名字为XXX的联系人")
    def click_contact_whose_name_is(self, name):
        """
        点击名字为XXX的联系人
        :param name: 联系人名字
        :return: 联系人名字、号码信息
        """
        locator = \
            [MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/root_view" '
             + 'and *//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="{}"]]'.format(
                 saxutils.escape(name, {"'": "&apos;", '"': "&quot;"}))]
        contact_info = self.get_contact_info(locator)
        self.click_element(locator)
        return contact_info

    @TestLogger.log("点击名字为XXX的联系人")
    def click_contact_whose_number_is(self, number):
        """
        点击名字为XXX的联系人
        :param number: 联系人号码
        :return: 联系人名字、号码信息
        """
        locator = \
            [MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/root_view" '
             + 'and *//*[@resource-id="com.chinasofti.rcs:id/tv_phone" and @text="{}"]]'.format(
                 saxutils.escape(number, {"'": "&apos;", '"': "&quot;"}))]
        contact_info = self.get_contact_info(locator)
        self.click_element(locator)
        return contact_info

    @TestLogger.log("获取联系人信息")
    def get_contact_info(self, locator):
        """
        获取联系人名称、号码信息
        :param locator: 联系人父容器的定位器
        :return:
        """
        contact = self.get_element(locator)
        name = contact.find_element(*self.__locators['联系人名字'])
        number = contact.find_element(*self.__locators['联系人号码'])
        return dict(
            name=name.text,
            number=number.text
        )

    @TestLogger.log("滚动到下一页")
    def page_down(self):
        """滚动到下一页"""
        self.swipe_by_direction(self.__locators['搜索结果列表'], 'up')

    @TestLogger.log("滚动到上一页")
    def page_up(self):
        """滚动到上一页"""
        self.swipe_by_direction(
            self.__locators['搜索结果列表'],
            'down'
        )

    @TestLogger.log("判断是否滚动到底部")
    def is_now_on_last_page(self):
        """
        判断是否滚动到底部
        :return:
        """
        container = self.get_element(self.__locators['搜索结果列表'])
        last_item = self.get_elements(
            [MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/single_result_list"]/*[last()]']
        )
        if len(last_item) == 0:
            return True

        # 容器底部底部y轴坐标
        container_bottom = container.location.get('y') + container.size.get('height')

        # 最后一项底部y轴坐标
        item_bottom = last_item[0].location.get('y') + last_item[0].size.get('height')

        # 检查列表是否有内容
        content = self.get_elements(
            [MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/single_result_list"]'
             + '/*[@resource-id="com.chinasofti.rcs:id/root_view"'
             + ' or *[@resource-id="com.chinasofti.rcs:id/svd_head"]]']
        )
        if len(content) == 0:
            return True
        if container_bottom - item_bottom > 0:
            return True
        else:
            return False
