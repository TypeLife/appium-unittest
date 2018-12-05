import re

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MessageSearchPage(BasePage):
    """搜索结果大于1条时打开进入该页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageSearchActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '对话名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '共2条与 “测” 相关的聊天记录': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        '列表': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
        '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/result_list"]/*'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '消息发送者': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '消息时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        '消息内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('获取列表条数')
    def get_message_count(self):
        text = self.get_text(self.__locators['共2条与 “测” 相关的聊天记录'])
        result = re.findall(r'\D+(\d+)\D+', text)
        if result:
            return int(result[0])
        else:
            return 0

    @TestLogger.log('获取列表条数')
    def get_message_keyword(self):
        text = self.get_text(self.__locators['共2条与 “测” 相关的聊天记录'])
        result = re.findall(r'“(.+)”', text)
        if result:
            return result[0]
        else:
            return ''

    @TestLogger.log('检查搜索结果条数与内容是否与统计栏描述一致')
    def assert_list_data_match_statistic_bar(self):
        expect_count = self.get_message_count()
        actual_count = 0
        keyword = self.get_message_keyword()
        messages = self.mobile.list_iterator(self.__locators['列表'], self.__locators['列表项'])
        for message in messages:
            actual_count += 1
            message_content = message.find_element(*self.__locators['消息内容']).text
            if keyword not in message_content:
                raise AssertionError('消息"{}"没有找到关键字"{}"'.format(message_content, keyword))
        if actual_count != expect_count:
            raise AssertionError('列表中实际消息数量：{} 不等于显示数量：{}'.format(actual_count, expect_count))
