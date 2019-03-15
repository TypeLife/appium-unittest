from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec

from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class MessagePage(FooterPage):
    """主页 - 消息页"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        "+号": (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        'com.chinasofti.rcs:id/itemLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/itemLayout'),
        'com.chinasofti.rcs:id/pop_item_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/pop_item_layout'),
        'com.chinasofti.rcs:id/iconIV': (MobileBy.ID, 'com.chinasofti.rcs:id/iconIV'),
        '新建消息': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="新建消息"]'),
        '免费短信': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="免费短信"]'),
        '发起群聊': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="发起群聊"]'),
        '分组群发': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="分组群发"]'),
        '扫一扫': (
            MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/pop_navi_text" and @text ="扫一扫"]'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
            MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
        '页头-消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        '消息列表': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_conv_list'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/search_edit'),
        '消息项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        '消息头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        '消息名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '消息时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        '消息简要内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
        '消息免打扰': (MobileBy.XPATH,
                  '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="%s"]/../../*[@resource-id="com.chinasofti.rcs:id/ll_unread"]'),
        '置顶群': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name"]'),
        '消息发送失败感叹号': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_fail_status'),
        '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
        '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
        '删除聊天': (MobileBy.XPATH, "//*[contains(@text, '删除聊天')]"),
        # 消息页中点击已发送文件
        '文件': (MobileBy.XPATH, "//*[contains(@text, '文件')]"),
        '位置': (MobileBy.XPATH, "//*[contains(@text, '位置')]"),
        '发送名片': (MobileBy.XPATH, "//*[contains(@text, '发送名片')]"),
        '名片': (MobileBy.XPATH, "//*[contains(@text, '名片')]"),
    }

    @TestLogger.log('检查顶部搜索框是否显示')
    def assert_search_box_is_display(self, max_wait_time=5):
        try:
            self.wait_until(
                condition=lambda d: self._is_element_present(self.__locators['搜索']),
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('搜索框没有显示：{}'.format(self.__locators['搜索']))

    @TestLogger.log('检查顶部搜索框是否显示')
    def assert_search_box_text_is(self, text):
        self.mobile.assert_element_text_should_be(self.__locators['搜索'], text, '搜索框文本与"{}"不匹配'.format(text))

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在消息页"""
        try:
            self.wait_until(
                timeout=8,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_add_icon(self):
        """点击加号图标"""
        self.click_element(self.__locators['+号'])

    @TestLogger.log()
    def click_new_message(self):
        """点击新建消息"""
        self.click_element(self.__locators['新建消息'])

    @TestLogger.log()
    def assert_new_message_text_equal_to(self, expect):
        """检查新建消息菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['新建消息'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_free_sms(self):
        """点击免费短信"""
        self.click_element(self.__locators['免费短信'])

    @TestLogger.log()
    def assert_free_sms_text_equal_to(self, expect):
        """检查免费短信菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['免费短信'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log('点击发起群聊')
    def click_group_chat(self):
        """点击发起群聊"""
        self.click_element(self.__locators['发起群聊'])

    @TestLogger.log()
    def click_contacts(self):
        """点击通讯录"""
        self.click_element(self.__locators['通讯录'])

    @TestLogger.log()
    def assert_group_chat_text_equal_to(self, expect):
        """检查发起群聊菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['发起群聊'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_group_mass(self):
        """点击分组群发"""
        self.click_element(self.__locators['分组群发'])

    @TestLogger.log()
    def assert_group_mass_text_equal_to(self, expect):
        """检查分组群发菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['分组群发'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_take_a_scan(self):
        """点击扫一扫"""
        self.click_element(self.__locators['扫一扫'])

    @TestLogger.log()
    def assert_take_a_scan_text_equal_to(self, expect):
        """检查扫一扫菜单文本"""
        actual = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['扫一扫'])
        ).text
        if actual != expect:
            raise AssertionError('期望值:"{}"\n实际值:"{}"\n'.format(expect, actual))

    @TestLogger.log()
    def click_search(self):
        """搜索"""
        self.click_element(self.__locators['搜索'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_login_success(self, timeout=8, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""
        self.__unexpected_info = None

        def unexpected():
            result = self.get_text(
                [MobileBy.XPATH,
                 '//*[@text="当前网络不可用(102101)，请检查网络设置" or' +
                 ' @text="服务器繁忙或加载超时,请耐心等待" or' +
                 ' contains(@text,"一键登录暂时无法使用") or' +
                 ' contains(@text,"登录失败") or' +
                 ' @text="网络连接超时(102102)，请使用短信验证码登录"' +
                 ']'])
            self.__unexpected_info = result
            return result

        try:
            self.wait_condition_and_listen_unexpected(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["+号"]),
                unexpected=unexpected
            )
        except TimeoutException:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        except AssertionError:
            raise AssertionError("检查到页面报错：{}".format(self.__unexpected_info))
        return self

    @TestLogger.log('检查是否收到某个号码的短信')
    def assert_get_sms_of(self, phone_number, content, max_wait_time=30):
        try:
            self.click_message(phone_number, max_wait_time)
        except NoSuchElementException:
            raise AssertionError('没有收到{}的消息'.format(phone_number))

    @TestLogger.log("检查列表第一项消息标题")
    def assert_first_message_title_in_list_is(self, title, max_wait_time=5):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.get_text(self.__locators['消息名称']) == title,
                timeout=max_wait_time,
                auto_accept_permission_alert=False
            )
        except TimeoutException:
            raise AssertionError('"{} != {}"'.format(self.get_text(self.__locators['消息名称']), title))

    @TestLogger.log('检查页面有没有出现139邮箱消息')
    def assert_139_message_not_appear(self, max_wait_time=30):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.is_text_present('139邮箱助手'),
                timeout=max_wait_time
            )
        except TimeoutException:
            return
        raise AssertionError('消息列表中不应该显示139邮箱消息，但实际上有显示')

    @TestLogger.log('点击消息')
    def click_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        self.find_message(title, max_wait_time)
        self.click_element(locator)

    @TestLogger.log('置顶消息')
    def set_top_for_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        self.find_message(title, max_wait_time)
        message = self.get_element(locator)
        position_x, position_y = message.location.get('x'), message.location.get('y')
        self.mobile.tap([(position_x, position_y)], 1000)
        if self.is_text_present('取消置顶'):
            el = self.get_element([MobileBy.XPATH, '//*[@text="取消置顶"]'])
            position_y, position_y = el.location.get('x'), el.location.get('y') - 100
            self.mobile.tap([(position_x, position_y)])
            return
        if self.is_text_present('置顶聊天'):
            self.click_text('置顶聊天')
        else:
            raise NoSuchElementException('没找到“置顶消息”菜单')

    @TestLogger.log("检查最新的一条消息的Title")
    def assert_the_first_message_is(self, title, max_wait_time=5):
        self.scroll_to_top()
        try:
            self.wait_until(
                condition=lambda d: self.get_text(self.__locators['消息名称']) == title,
                timeout=max_wait_time
            )
        except TimeoutException:
            raise AssertionError('{}秒内没有找到"{}"的最新消息'.format(max_wait_time, title))

    @TestLogger.log("寻找定位消息")
    def find_message(self, title, max_wait_time=5):
        locator = [MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/rl_conv_list_item" and ' +
                   './/*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text="{}"]]'.format(title)]
        if not self._is_element_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            if self._is_element_present(locator):
                return
            if not self.get_elements(self.__locators['消息项']):
                try:
                    self.wait_until(
                        condition=lambda d: self.get_element(locator),
                        timeout=max_wait_time,
                        auto_accept_permission_alert=False
                    )
                    return
                except TimeoutException:
                    raise NoSuchElementException('页面找不到元素：{}'.format(locator))
            max_try = 20
            current = 0
            while current < max_try:
                first_item = self.get_element(self.__locators['消息项'])
                current += 1
                self.page_down()
                if self._is_element_present(locator):
                    return
                if not ec.staleness_of(first_item)(True):
                    break
            self.scroll_to_top()
            try:
                self.wait_until(
                    condition=lambda d: self.get_element(locator),
                    timeout=max_wait_time,
                    auto_accept_permission_alert=False
                )
                return
            except TimeoutException:
                raise NoSuchElementException('页面找不到元素：{}'.format(locator))

    @TestLogger.log("回到列表顶部")
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['消息列表'])
        )
        # 如果找到“短信设置”菜单，则当作已经滑到底部
        if self._is_on_the_start_of_list_view():
            return True
        max_try = 50
        current = 0
        while current < max_try:
            current += 1
            self.page_up()
            if self._is_on_the_start_of_list_view():
                break
        return True

    @TestLogger.log("下一页")
    def page_down(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['消息列表'])
        )
        self.swipe_by_direction(self.__locators['消息列表'], 'up')

    @TestLogger.log("下一页")
    def page_up(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['消息列表'])
        )
        self.swipe_by_direction(self.__locators['消息列表'], 'down')

    def _is_on_the_start_of_list_view(self):
        """判断是否列表开头"""
        return self._is_element_present(self.__locators['搜索'])

    @TestLogger.log()
    def is_exist_undisturb(self, group_name):
        """某群是否存在消息免打扰标志"""
        path = self.__class__.__locators["消息免打扰"][1]
        self.__class__.__locators["xpath"] = (self.__class__.__locators["消息免打扰"][0], path % group_name)
        return self._is_element_present(self.__class__.__locators["xpath"])

    @TestLogger.log()
    def get_top_news_name(self):
        """获取置顶群的名字"""
        return self.get_element(self.__class__.__locators['置顶群']).text

    @TestLogger.log()
    def click_element_by_text(self,text):
        """点击指定元素"""
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % text))

    @TestLogger.log()
    def is_iv_fail_status_present(self):
        """判断消息发送失败“！”标致是否存在"""
        return self._is_element_present(self.__locators['消息发送失败感叹号'])

    @TestLogger.log()
    def press_file_to_do(self, file, text):
        """长按指定文件进行操作"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def look_detail_news_by_name(self, name):
        """查看详细消息"""
        self.click_element((MobileBy.XPATH, "//*[@text='%s']" % name))

    @TestLogger.log()
    def click_msg_by_content(self, text):
        """点击消息"""
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_content" and @text="%s"]' % text))

    @TestLogger.log('判断该页面是否有元素')
    def page_contain_element(self, locator):
        return self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log("判断消息列表的消息是否包含省略号")
    def msg_is_contain_ellipsis(self):
        contents = []
        els = self.get_elements(self.__locators['消息简要内容'])
        for el in els:
            contents.append(el.text)
        for msg in contents:
            if "…" in msg:
                return True
        raise AssertionError("消息列表的消息无省略号")

    @TestLogger.log()
    def click_set_message(self, locator):
        """点击已发文件类型"""
        self.click_element(self.__locators[locator])

    @TestLogger.log()
    def choose_chat_by_name(self, name):
        """通过名字选择一个聊天"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name)
        max_try = 10
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.page_down()
        self.click_element(locator)

    @TestLogger.log()
    def click_workbench(self):
        """点击工作台"""
        self.click_element(self.__class__.__locators["工作台"])

