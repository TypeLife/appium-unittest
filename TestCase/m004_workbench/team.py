import unittest
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from library.core.common.simcardtype import CardType
from pages import *
import time

from pages.workbench.create_team.CreateTeam import CreateTeamPage
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from TestCase.m001_login.login import *


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def enter_create_team_page(reset=False):
        """从消息进入创建团队页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_create_team()
        team = CreateTeamPage()
        team.wait_for_page_load()

    @staticmethod
    def get_team_name():
        """获取团队"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        team_name = "ateam" + phone_number[-4:]
        return team_name

    @staticmethod
    def create_team(team_name=None, user_name="admin"):
        """创建团队"""
        if not team_name:
            team_name = Preconditions.get_team_name()
        team = CreateTeamPage()
        team.input_team_name(team_name)
        team.choose_location()
        team.choose_industry()
        team.input_real_name(user_name)
        # 立即创建团队
        team.click_immediately_create_team()
        # 点击完成设置工作台
        team.click_finish_setting_workbench()
        team.wait_for_create_team_success_page_load()
        # 进入工作台
        team.click_enter_workbench()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()


class TeamTest(TestCase):
    """团队 模块"""

    def default_setUp(self):
        """进入创建团队页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_create_team_page()
            return
        team = CreateTeamPage()
        if team.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().reset_app()
            Preconditions.enter_create_team_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'workbench')
    def test_CJTD_0001(self):
        """检查创建团队界面是否正确返回到工作台主界面"""
        # 1、点击最底部的“创建团队”
        # 2、点击左上角【<】返回
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', 'workbench')
    def test_CJTD_0002(self):
        """创建团队"""
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = Preconditions.get_team_name()
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        Preconditions.create_team()
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', 'workbench')
    def test_CJTD_0003(self):
        """创建团队-团队名称为空"""
        team = CreateTeamPage()
        team.choose_location()
        team.choose_industry()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("请输入团队名称")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', 'workbench')
    def test_CJTD_0004(self):
        """创建团建-所在地为空"""
        team = CreateTeamPage()
        team.input_team_name("测试团队")
        team.choose_industry()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("请选择所在地")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', 'workbench')
    def test_CJTD_0005(self):
        """创建团建-行业为空"""
        team = CreateTeamPage()
        team.input_team_name("测试团队")
        team.choose_location()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("请选择行业")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', 'workbench')
    def test_CJTD_0006(self):
        """创建团建-姓名为空"""
        team = CreateTeamPage()
        team.input_team_name("测试团队")
        team.choose_location()
        team.choose_industry()
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("管理员姓名不能为空")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', 'workbench')
    def test_CJTD_0007(self):
        """创建团建-邮箱为空"""
        team = CreateTeamPage()
        team.input_team_name("测试团队")
        team.choose_location()
        team.choose_industry()
        team.input_real_name('admin')
        team.input_email('')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("请输入邮箱地址")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @staticmethod
    def setUp_test_workbench_GGXX_0005():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.create_team_message("天气预报","晴天转多云")
        time.sleep(1)

    @tags('ALL', 'Login', "workbench")
    def test_workbench_GGXX_0005(self):
        '验证公告信息首页搜索是否正确'
        pg = CreateTeamPage()
        pg.click_enter_search()
        pg.input_search_text()
        pg.is_text_present('天气预报')

    @staticmethod
    def tearDown_test_workbench_GGXX_0005():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_0006():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.save_team__message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL', 'Login', "workbench")
    def test_workbench_GGXX_0006(self):
        '验证未发公告页搜索是否正确'
        pg = CreateTeamPage()
        pg.click_no_publish()
        pg.click_enter_search()
        pg.input_search_text()
        pg.is_text_present('天气预报')

    @staticmethod
    def tearDown_test_workbench_GGXX_0006():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_0007():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.create_team_message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL', 'Login', "workbench")
    def test_workbench_GGXX_0007(self):
        '已发布公告下线'
        pg = CreateTeamPage()
        pg.click_list_message()
        pg.click_remove_message()
        time.sleep(2)
        pg.page_should_not_contain_text('天气预报')

    @staticmethod
    def tearDown_test_workbench_GGXX_0007():
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)


    @staticmethod
    def setUp_test_workbench_GGXX_0008():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.save_team__message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL', 'Login', "workbench")
    def test_workbench_GGXX_0008(self):
        '公告存草稿'
        pg = CreateTeamPage()
        pg.click_no_publish()
        time.sleep(1)
        pg.page_should_contain_text("天气预报")

    @staticmethod
    def tearDown_test_workbench_GGXX_0008():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_0009():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.save_team__message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL', 'Login', "workbench")
    def test_workbench_GGXX_0009(self):
        """
        发布未发布中公告
        :return:
        """
        pg = CreateTeamPage()
        pg.click_no_publish()
        time.sleep(1)
        pg.click_list_message()
        pg.click_publish()
        pg.click_sure()
        time.sleep(2)
        pg.page_should_contain_text("天气预报")
        time.sleep(1)

    @staticmethod
    def tearDown_test_workbench_GGXX_0009():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_00010():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.save_team__message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL', 'Login', "workbench")
    def test_workbench_GGXX_00010(self):
        """
        删除,公告中草稿
        """
        pg = CreateTeamPage()
        time.sleep(1)
        pg.click_no_publish()
        time.sleep(1)
        pg.remove_message()
        time.sleep(2)
        flag=pg.page_should_not_contain_text("天气预报")

    @staticmethod
    def tearDown_test_workbench_GGXX_00010():
        oklp = OneKeyLoginPage()
        time.sleep(10)
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)
