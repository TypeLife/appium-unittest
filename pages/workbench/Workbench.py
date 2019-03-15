from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class WorkbenchPage(FooterPage):
    """工作台主页"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
                  'com.chinasofti.rcs:id/home_tag_view_pager': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
                  'com.chinasofti.rcs:id/constraintLayout_home_tab': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
                  'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
                  'com.chinasofti.rcs:id/actionbar_main_enterprise': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/actionbar_main_enterprise'),
                  '当前团队名称:myteam02': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
                  'com.chinasofti.rcs:id/swipeToLoad': (MobileBy.ID, 'com.chinasofti.rcs:id/swipeToLoad'),
                  'com.chinasofti.rcs:id/swipe_target': (MobileBy.ID, 'com.chinasofti.rcs:id/swipe_target'),
                  'com.chinasofti.rcs:id/ll_viewpager': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_viewpager'),
                  '容器列表': (MobileBy.ID, 'com.chinasofti.rcs:id/viewpager'),
                  'com.chinasofti.rcs:id/card_view': (MobileBy.ID, 'com.chinasofti.rcs:id/card_view'),
                  '广告banner': (MobileBy.ID, 'com.chinasofti.rcs:id/card_banner_view'),
                  'com.chinasofti.rcs:id/image': (MobileBy.ID, 'com.chinasofti.rcs:id/image'),
                  'com.chinasofti.rcs:id/group': (MobileBy.ID, 'com.chinasofti.rcs:id/group'),
                  'com.chinasofti.rcs:id/fl_work_config': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_work_config'),
                  'com.chinasofti.rcs:id/rl_category': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_category'),
                  'com.chinasofti.rcs:id/iv_head': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
                  '管理控制台（仅管理员可见）': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '权益': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_expanded'),
                  'com.chinasofti.rcs:id/member_list': (MobileBy.ID, 'com.chinasofti.rcs:id/member_list'),
                  'com.chinasofti.rcs:id/rl_item': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_item'),
                  'com.chinasofti.rcs:id/view_header_space': (MobileBy.ID, 'com.chinasofti.rcs:id/view_header_space'),
                  'com.chinasofti.rcs:id/rl_icon_content': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_icon_content'),
                  'com.chinasofti.rcs:id/iv_iron': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_iron'),
                  '组织架构': (MobileBy.XPATH, '//*[@text="组织架构"]'),
                  '工作台管理': (MobileBy.XPATH, '//*[@text="工作台管理"]'),
                  '邀请成员': (MobileBy.XPATH, '//*[@text="邀请成员"]'),
                  '管理员指引': (MobileBy.XPATH, '//*[@text="管理员指引"]'),
                  'com.chinasofti.rcs:id/ll_content': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_content'),
                  '常用应用': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '公告信息': (MobileBy.XPATH, '//*[@text="公告信息"]'),
                  '企业新闻': (MobileBy.XPATH, '//*[@text="企业新闻"]'),
                  '企业通讯录': (MobileBy.XPATH, '//*[@text="企业通讯录"]'),
                  '团队通讯': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '超级会议': (MobileBy.XPATH, '//*[@text="超级会议"]'),
                  '群发信使': (MobileBy.XPATH, '//*[@text="群发信使"]'),
                  '语音通知': (MobileBy.XPATH, '//*[@text="语音通知"]'),
                  '139邮箱': (MobileBy.XPATH, '//*[@text="139邮箱"]'),
                  '协同办公': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '考勤打卡': (MobileBy.XPATH, '//*[@text="考勤打卡"]'),
                  '审批': (MobileBy.XPATH, '//*[@text="审批"]'),
                  '日志': (MobileBy.XPATH, '//*[@text="日志"]'),
                  '重要事项': (MobileBy.XPATH, '//*[@text="重要事项"]'),
                  '个人应用': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '咪咕影院': (MobileBy.XPATH, '//*[@text="咪咕影院"]'),
                  '帮助中心': (MobileBy.XPATH, '//*[@text="帮助中心"]'),
                  '岭南优品': (MobileBy.XPATH, '//*[@text="岭南优品"]'),
                  'com.chinasofti.rcs:id/rl_bottom': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_bottom'),
                  'com.chinasofti.rcs:id/recyclerView': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
                  '应用商城': (MobileBy.XPATH, '//*[@text="应用商城"]'),
                  'com.chinasofti.rcs:id/iv_logo': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_logo'),
                  '应用管理': (MobileBy.XPATH, '//*[@text="应用管理"]'),
                  '咨询客服': (MobileBy.XPATH, '//*[@text="咨询客服"]'),
                  '创建团队': (MobileBy.XPATH, '//*[@text="创建团队"]'),
                  '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
                  '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
                  '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
                  '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
                  '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
                  '解散团队': (MobileBy.XPATH, '//*[@text="解散团队"]'),
                  '确定1': (MobileBy.XPATH, '//*[@text="确定"]'),
                  '团队返回': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_listitem'),
                  # 未创建或者未加入团队时的页面元素
                  '马上创建团队': (MobileBy.XPATH, '//*[@text="马上创建团队"]'),
                  '欢迎创建团队': (MobileBy.XPATH, '//*[@text="欢迎创建团队"]'),
                  # 点击左上角的企业名称的倒三角形的团队元素定位
                  '团队列表': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_listitem'),
                  }

    def swipe_half_page_up(self):
        """向上滑动半页"""
        self.swipe_by_percent_on_screen(50, 80, 50, 30, 800)

    def swipe_half_page_down(self):
        """向下滑动半页"""
        self.swipe_by_percent_on_screen(50, 30, 50, 80, 800)

    def find_els(self, location):
        """查找元素"""
        els = self.get_elements(location)
        if len(els) > 0:
            return els
        while True:
            self.swipe_half_page_up()
            els = self.get_elements(location)
            if len(els) > 0:
                return els
            # 滑动到底部还未找到元素则终止滑动
            els = self.get_elements(self.__class__.__locators['创建团队'])
            if len(els) > 0:
                break
        while True:
            self.swipe_half_page_down()
            els = self.get_elements(location)
            if len(els) > 0:
                return els
            # 滑动到顶部还未找到元素则终止滑动
            els = self.get_elements(self.__class__.__locators['广告banner'])
            if len(els) > 0:
                break
        return False

    @TestLogger.log()
    def click_organization(self):
        """点击组织架构"""
        els = self.find_els(self.__class__.__locators['组织架构'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 组织架构 控件")

    @TestLogger.log()
    def click_workbench_manage(self):
        """点击工作台管理"""
        els = self.find_els(self.__class__.__locators['工作台管理'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 工作台管理 控件")

    @TestLogger.log()
    def click_invite_member(self):
        """点击邀请成员"""
        els = self.find_els(self.__class__.__locators['邀请成员'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 邀请成员 控件")

    @TestLogger.log()
    def click_manager_guide(self):
        """点击管理员指引"""
        els = self.find_els(self.__class__.__locators['管理员指引'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 管理员指引 控件")

    @TestLogger.log()
    def click_notice_info(self):
        """点击公告信息"""
        els = self.find_els(self.__class__.__locators['公告信息'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 公告信息 控件")

    @TestLogger.log()
    def click_company_news(self):
        """点击企业新闻"""
        els = self.find_els(self.__class__.__locators['企业新闻'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 企业新闻 控件")

    @TestLogger.log()
    def click_company_contacts(self):
        """点击企业通讯录"""
        els = self.find_els(self.__class__.__locators['企业通讯录'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 企业通讯录 控件")

    @TestLogger.log()
    def click_super_meeting(self):
        """点击超级会议"""
        els = self.find_els(self.__class__.__locators['超级会议'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 超级会议 控件")

    @TestLogger.log()
    def click_group_messenger(self):
        """点击群发信使"""
        els = self.find_els(self.__class__.__locators['群发信使'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 群发信使 控件")

    @TestLogger.log()
    def click_voice_notice(self):
        """点击语音通知"""
        els = self.find_els(self.__class__.__locators['语音通知'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 语音通知 控件")

    @TestLogger.log()
    def click_139email(self):
        """点击139邮箱"""
        els = self.find_els(self.__class__.__locators['139邮箱'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 139邮箱 控件")

    @TestLogger.log()
    def click_attendance_card(self):
        """点击考勤打卡"""
        els = self.find_els(self.__class__.__locators['考勤打卡'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 考勤打卡 控件")

    @TestLogger.log()
    def click_approve(self):
        """点击审批"""
        els = self.find_els(self.__class__.__locators['审批'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 审批 控件")

    @TestLogger.log()
    def click_journal(self):
        """点击日志"""
        els = self.find_els(self.__class__.__locators['日志'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 日志 控件")

    @TestLogger.log()
    def click_important_items(self):
        """点击重要事项"""
        els = self.find_els(self.__class__.__locators['重要事项'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 重要事项 控件")

    @TestLogger.log()
    def click_app_store(self):
        """点击应用商城"""
        els = self.find_els(self.__class__.__locators['应用商城'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 应用商城 控件")

    @TestLogger.log()
    def click_app_manage(self):
        """点击应用管理"""
        els = self.find_els(self.__class__.__locators['应用管理'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 应用管理 控件")

    @TestLogger.log()
    def click_custom_service(self):
        """点击咨询客服"""
        els = self.find_els(self.__class__.__locators['咨询客服'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 咨询客服 控件")

    @TestLogger.log()
    def click_create_team(self):
        """点击创建团队"""
        els = self.find_els(self.__class__.__locators['创建团队'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 创建团队 控件")

    @TestLogger.log()
    def click_rights(self):
        """点击权益"""
        els = self.find_els(self.__class__.__locators['权益'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 权益 控件")

    @TestLogger.log()
    def click_enterprise_name_triangle(self):
        """点击左上角的企业名称的倒三角形选择团队"""
        name = self.get_element(self.__class__.__locators['当前团队名称:myteam02']).text
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % name))

    @TestLogger.log()
    def get_team_names(self):
        """获取所有团队的名字"""
        names = []
        els = self.get_elements(self.__class__.__locators['团队列表'])
        for el in els:
            names.append(el.text)
        return names

    @TestLogger.log()
    def select_team_by_name(self, name):
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % name))

    @TestLogger.log()
    def click_now_create_team(self):
        """点击马上创建团队"""
        self.click_element(self.__class__.__locators['马上创建团队'])

    def is_on_welcome_page(self):
        """当前页面是否在 欢迎创建团队页面"""
        try:
            self.wait_until(
                timeout=3,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["欢迎创建团队"])
            )
            return True
        except:
            return False

    def is_on_this_page(self):
        """判断是否在此页面"""
        el = self.get_elements(self.__locators['工作台管理'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """工作台管理页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["当前团队名称:myteam02"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_press_enterprise_name(self):
        """点击并长按左上角的企业名称的倒三角"""
        name = self.get_element(self.__class__.__locators['当前团队名称:myteam02']).text
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % name))
        el = self.get_element((MobileBy.XPATH, '//*[@text="%s"]' % name))
        self.press(el)

    @TestLogger.log()
    def click_cancel_team(self):
        """点击解散团队"""
        self.click_element(self.__class__.__locators["解散团队"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定解散团队"""
        self.click_element(self.__class__.__locators["确定1"])

    @TestLogger.log()
    def click_back_team(self):
        """点击确定解散团队"""
        self.click_element(self.__class__.__locators["团队返回"])

    @TestLogger.log()
    def wait_for_workbench_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待工作台页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.driver.current_activity == self.ACTIVITY
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self




