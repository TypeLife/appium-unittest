import unittest
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import *
import time


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    pass


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
