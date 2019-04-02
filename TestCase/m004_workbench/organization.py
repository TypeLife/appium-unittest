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

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0001(self):
        """工作台管理员权限可看到组织架构入口"""
        #1、进入工作台页面 2、点击组织架构
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        time.sleep(1)
        current_mobile().back()
        mess = MessagePage()
        mess.open_message_page()

    @staticmethod
    def setUp_test_ZZJG_0002():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        preconditions.force_close_and_launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0002(self):
        """从通讯录中进入组织架构"""
        #1、进入通讯录-和通讯录
        # 2、找到自己是管理员权限的企业通讯录
        # 3、点击右上角【...】
        # 4、点击【团队管理】
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(3)
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_allow()
        contacts.wait_for_page_load()
        contacts.click_and_address()
        time.sleep(5)
        contacts.click_one_he_contacts()
        time.sleep(1)
        contacts.click_he_more()
        time.sleep(2)
        contacts.click_text("团队管理")
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        time.sleep(3)
        current_mobile().back()
        time.sleep(1)
        current_mobile().back()
        time.sleep(1)
        current_mobile().back()
        mess.open_message_page()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0004(self):
        """手动添加联系人"""
        #1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“手动输入添加”
        # 4、不输入姓名或主手机号码
        # 5、点击“完成”
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加联系人")
        time.sleep(1)
        osp.click_text("手动输入添加")
        time.sleep(1)
        osp.click_text("完成")
        if not osp.is_toast_exist("请输入姓名"):
            raise AssertionError("没有出现toast提示")
        time.sleep(1)
        current_mobile().back()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0005(self):
        """从手机通讯录添加联系人"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“从手机通讯录添加”
        # 4、选择通讯录中的成员，点击【确定】
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        slc = SelectLocalContactsPage()
        if osp.is_text_present("和飞信电话"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            slc.click_one_contact("和飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("1个联系人联系人在库中已存在"):
                raise AssertionError("操作不成功")
            time.sleep(2)
            if not osp.is_on_this_page():
                raise AssertionError("没有返回上一级")
        else:
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            slc.click_one_contact("和飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("操作成功"):
                raise AssertionError("操作不成功")
            time.sleep(2)
            if not osp.is_on_this_page():
                raise AssertionError("没有返回上一级")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0006(self):
        """从手机通讯录添加搜索的联系人"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“从手机通讯录添加”
        # 4、在搜索框输入关键字
        # 5、点击联系人
        # 6、点击【确定】
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        slc = SelectLocalContactsPage()
        if osp.is_text_present("和飞信电话"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            sc = SelectContactsPage()
            # 搜索联系人
            sc.input_search_contact_message("和飞信")
            # 选择“和飞信电话”联系人进行转发
            sc.click_one_contact("和飞信电话")
            # slc.click_one_contact("和飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("1个联系人联系人在库中已存在"):
                raise AssertionError("操作不成功")
            time.sleep(2)
            if not osp.is_on_this_page():
                raise AssertionError("没有返回上一级")
        else:
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            sc = SelectContactsPage()
            # 搜索联系人
            sc.input_search_contact_message("和飞信")
            # 选择“和飞信电话”联系人进行转发
            sc.click_one_contact("和飞信电话")
            # slc.click_one_contact("和飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("操作成功"):
                raise AssertionError("操作不成功")
            time.sleep(2)
            if not osp.is_on_this_page():
                raise AssertionError("没有返回上一级")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0007(self):
        """点击邀请小伙伴正常跳转到邀请成员页面"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“邀请小伙伴”
        # 4、操作页面的各个按钮
        # 5、点返回
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加联系人")
        time.sleep(1)
        osp.click_text("邀请小伙伴")
        osp.wait_for_invite_page_load()
        osp.click_invite_mode_switch()
        time.sleep(2)
        if not osp.is_text_present("加入企业后仅可见自己"):
            raise AssertionError("访客模式开关不可用")
        osp.click_invite_save()
        if not osp.is_toast_exist("保存图片成功"):
            raise AssertionError("保存二维码按钮不可用")
        time.sleep(1)
        osp.click_invite_share()
        time.sleep(1)
        if not osp.is_exist_element_by_locatorname("点击右上角即可分享"):
            raise AssertionError("分享按钮不可用")
        current_mobile().back()
        osp.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0008(self):
        """点击取消，弹窗隐藏"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“取消”
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加联系人")
        time.sleep(1)
        osp.click_text("取消")
        time.sleep(2)
        if osp.is_text_present("邀请小伙伴"):
            raise AssertionError("弹窗隐藏失败")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0009(self):
        """成功添加一个子部门"""
        # 1、点击“组织架构”应用
        # 2、点击“添加子部门”
        # 3、输入部门名称：“测试部”
        # 4、点击完成
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加子部门")
        osp.wait_for_sub_department_page_load()
        osp.input_sub_department_name("哈哈")
        osp.click_text("完成")
        if osp.is_toast_exist("部门已存在，请勿重复添加"):
            current_mobile().back()
            osp.wait_for_page_load()
        else:
            osp.wait_for_page_load()

