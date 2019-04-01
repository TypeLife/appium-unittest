import unittest

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

class OrganizationTest(TestCase):
    """
    模块：工作台->组织架构
    文件位置：20190313工作台全量用例整理.xlsx
    表格：组织架构
    """

    def default_setUp(self):
        """进入组织架构页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_organization_page()
            return
        osp = OrganizationStructurePage()
        if osp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            preconditions.force_close_and_launch_app()
            Preconditions.enter_organization_page()

    def default_tearDown(self):
        pass