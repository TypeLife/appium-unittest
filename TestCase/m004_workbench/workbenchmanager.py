import unittest

from pages.workbench.manager_console.WorkbenchManagerPage import WorkBenchManagerPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import *
import time

from pages.workbench.create_team.CreateTeam import CreateTeamPage
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from TestCase.m001_login.login import *


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    pass

class WorkBenchManagerTest(TestCase):
    """
    模块：工作台->工作台管理
    文件位置：20190313工作台全量用例整理.xlsx
    表格：工作台管理
    """

    def default_setUp(self):
        """进入工作台管理页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_workbench_manager_page()
            return
        wmp = WorkBenchManagerPage()
        if wmp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_workbench_manager_page()

    def default_tearDown(self):
        pass

    @tags('ALL', "CMCC", 'workbench', 'GZTGL')
    def test_GZTGL_0003(self):
        """搜索不存在的应用名称"""
        # 1、点击“工作台管理”
        # 2、点击页面“常用应用”下的“+”号
        # 3、搜索应用商城不存在的应用名称
        wmp = WorkBenchManagerPage()
        wmp.wait_for_page_load()
        time.sleep(1)
        wmp.click_add()
        wmp.wait_for_store_page_load()
        time.sleep(2)
        wmp.click_search_store()
        time.sleep(2)
        wmp.input_store_name("哈哈")
        time.sleep(2)
        wmp.click_search()
        time.sleep(6)
        if not wmp.is_text_present("暂无相关的应用"):
            raise AssertionError("搜索不成功")
        wmp.click_close()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()




