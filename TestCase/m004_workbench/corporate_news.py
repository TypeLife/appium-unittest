import preconditions
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.corporate_news.CorporateNews import CorporateNewsPage
import time

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

class Preconditions(object):
    """前置条件"""

    @staticmethod
    def select_mobile(category, reset=False):
        """选择手机"""

        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        if reset:
            current_mobile().reset_app()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""

        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        current_mobile().hide_keyboard_if_display()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.click_submit_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """从一键登录页面登录"""

        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        one_key.click_read_agreement_detail()

        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def enter_corporate_news_page():
        """进入企业新闻首页"""

        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_company_news()

    @staticmethod
    def create_unpublished_news():
        """创建未发新闻"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        time.sleep(10)
        # 点击链接发布
        cnp.click_link_publishing()
        time.sleep(2)
        # 输入新闻标题
        cnp.input_news_title("test_news")
        # 输入链接新闻
        cnp.input_link_news("https://10086.com")
        # 点击保存
        cnp.click_save()
        # 点击确定
        cnp.click_sure()
        cnp.wait_for_page_load()

class CorporateNewsTest(TestCase):
    """
    模块：工作台->企业新闻
    文件位置：移动端自动化用例整理20190304(工作台部分).xlsx
    表格：工作台->企业新闻
    """

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在企业新闻应用首页
        """

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        wbp = WorkbenchPage()
        cnp = CorporateNewsPage()
        mess = MessagePage()
        if cnp.is_on_corporate_news_page():
            return
        if not mess.is_on_this_page():
            preconditions.force_close_and_launch_app()
            mess.wait_for_page_load()
        mess.click_workbench()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()


    def default_tearDown(self):

        pass

    @tags('ALL', 'workbench', 'LXD')
    def test_QYXW_0005(self):
        """保存新闻"""

        cnp = CorporateNewsPage()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        time.sleep(10)
        # 点击链接发布
        cnp.click_link_publishing()
        time.sleep(2)
        # 输入新闻标题
        cnp.input_news_title("test_news")
        # 输入链接新闻
        cnp.input_link_news("https://10086.com")
        # 点击保存
        cnp.click_save()
        # 点击确定
        cnp.click_sure()
        # 是否提示保存成功,等待企业新闻首页加载
        self.assertEquals(cnp.is_exist_save_successfully(), True)
        cnp.wait_for_page_load()

    @tags('ALL', 'workbench', 'LXD')
    def test_QYXW_0007(self):
        """验证删除未发新闻是否正确"""

        cnp = CorporateNewsPage()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        time.sleep(2)
        # 确保未发新闻列表存在数据
        if not cnp.is_exist_no_news():
            cnp.click_back()
            Preconditions.create_unpublished_news()
            cnp.click_no_news()
            time.sleep(2)
        title = cnp.get_first_news_title()
        # 点击一条未发新闻
        cnp.click_first_news()
        time.sleep(2)
        # 点击删除
        cnp.click_delete()
        # 点击确定
        cnp.click_sure()
        # 1.是否提示删除成功,等待未发新闻页面加载
        self.assertEquals(cnp.is_exist_delete_successfully(), True)
        cnp.wait_for_page_load()
        # 2.验证未发新闻列表是否存在该记录信息
        self.assertEquals(cnp.is_exist_news_by_name(title), False)





