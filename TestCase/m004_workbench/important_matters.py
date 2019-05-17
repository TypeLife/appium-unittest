import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile, current_driver
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.important_matters.ImportantMatters import ImportantMattersPage
from preconditions.BasePreconditions import WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def enter_important_matters_page():
        """进入重要事项首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        # 查找并点击所有展开元素
        wbp.find_and_click_open_element()
        wbp.click_add_important_matters()
        imp = ImportantMattersPage()
        # 解决工作台不稳定问题
        time.sleep(5)
        n = 1
        while imp.is_text_present("统一认证接口返回异常"):
            imp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_important_items()
            time.sleep(5)
            n += 1
            if n > 10:
                break

    @staticmethod
    def ensure_have_item():
        """确保已有事项"""

        imp = ImportantMattersPage()
        if not imp.is_exists_item():
            imp.click_new_item()
            # 等待创建事项页面加载
            imp.wait_for_create_item_page_load()
            # 输入创建事项标题
            title = "测试事项"
            imp.input_create_item_title(title)
            # 输入创建事项描述
            imp.input_create_item_describe("描述内容12345")
            imp.click_add_icon()
            sccp = SelectCompanyContactsPage()
            sccp.wait_for_page_load()
            # 选择参与人
            sccp.click_contacts_by_name("大佬1")
            sccp.click_sure_button()
            imp.wait_for_create_item_page_load()
            imp.click_create_item()
            imp.wait_for_page_load()

@unittest.skip("跳过")
class ImportantMattersAllTest(TestCase):
    """
    模块：工作台->重要事项
    文件位置：20190313工作台全量用例整理.xlsx
    表格：工作台->重要事项
    Author：刘晓东
    """

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在重要事项首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_important_matters_page()
            return
        imp = ImportantMattersPage()
        if imp.is_on_important_matters_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_important_matters_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0001(self):
        """验证点击返回按钮是否正确"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 点击返回
        imp.click_back()
        wbp = WorkbenchPage()
        # 等待工作台页面加载
        wbp.wait_for_workbench_page_load()
        wbp.click_important_items()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0002(self):
        """新建事项"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 清空进行中的事项，确保不影响验证
        imp.clear_item()
        imp.click_new_item()
        # 1.等待创建事项页面加载
        imp.wait_for_create_item_page_load()
        # 输入创建事项标题
        title = "测试事项0002"
        imp.input_create_item_title(title)
        # 输入创建事项描述
        imp.input_create_item_describe("描述内容0002")
        imp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 选择参与人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_sure_button()
        imp.wait_for_create_item_page_load()
        imp.click_create_item()
        imp.wait_for_page_load()
        # 2.显示刚刚创建的事项
        self.assertEquals(imp.is_text_present(title), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0003(self):
        """修改事项标题"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        # Preconditions.ensure_have_item()
        # imp.click_first_item()
        imp.click_text("创建")
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 2.点击查看事项页面标题
        imp.click_check_item_title()
        time.sleep(2)
        modify_title = "修改后的测试事项标题0003"
        imp.input_modify_content(modify_title)
        imp.click_save()
        # 3.等待查看事项页面加载，界面事项标题显示为修改后的标题
        imp.wait_for_check_item_page_load()
        self.assertEquals(imp.is_text_present(modify_title), True)
        imp.click_back()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0004(self):
        """修改事项描述"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        Preconditions.ensure_have_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        # 2.点击查看事项页面描述
        imp.click_check_item_describe()
        time.sleep(2)
        modify_describe = "修改后的测试事项描述0004"
        imp.input_modify_content(modify_describe)
        imp.click_save()
        # 3.等待查看事项页面加载，界面事项描述显示为修改后的内容
        imp.wait_for_check_item_page_load()
        self.assertEquals(imp.is_text_present(modify_describe), True)
        imp.click_back()
        # 等待重要事项首页加载
        imp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0005(self):
        """修改增加事项参与人"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        Preconditions.ensure_have_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        imp.click_personnel_status()
        # 2.等待人员状态页面加载
        imp.wait_for_personnel_status_page_load()
        imp.click_add_personnel()
        sccp = SelectCompanyContactsPage()
        # 3.等待选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬2"
        sccp.input_search_message(search_name)
        time.sleep(2)
        # 4.显示搜索结果
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        sccp.click_contacts_by_name(search_name)
        sccp.click_sure_button()
        # 5.添加成功，等待人员状态页面加载，界面显示刚刚添加的联系人信息
        self.assertEquals(imp.is_toast_exist("添加成功"), True)
        imp.wait_for_personnel_status_page_load()
        self.assertEquals(imp.is_text_present("佬2"), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_ZYSX_0006(self):
        """修改删除事项参与人"""

        imp = ImportantMattersPage()
        imp.wait_for_page_load()
        # 确保已有事项
        Preconditions.ensure_have_item()
        imp.click_first_item()
        # 1.等待查看事项页面加载
        imp.wait_for_check_item_page_load()
        imp.click_personnel_status()
        # 2.等待人员状态页面加载
        imp.wait_for_personnel_status_page_load()
        # 确保有人员可移除
        imp.click_add_personnel()
        sccp = SelectCompanyContactsPage()
        # 等待选择联系人页面加载
        sccp.wait_for_page_load()
        add_name = "大佬3"
        sccp.click_contacts_by_name(add_name)
        sccp.click_sure_button()
        imp.wait_for_personnel_status_page_load()
        imp.click_delete_personnel()
        # 3.界面未读人员显示可删除按钮
        self.assertEquals(imp.is_exists_delete_icon_by_name("佬3"), True)
        imp.click_delete_icon_by_name("佬3")
        # 4.删除的联系人从界面消失
        self.assertEquals(imp.is_text_present("佬3"), False)
        # 5.退出删除状态
        imp.click_delete_personnel()
        imp.click_back()
        imp.wait_for_check_item_page_load()
        imp.click_back()
        # 等待重要事项首页加载
        imp.wait_for_page_load()




