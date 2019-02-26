import random
import re
import time
import unittest
import uuid

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.me.MeEditUserProfile import MeEditUserProfilePage
from pages.me.MeViewUserProfile import MeViewUserProfilePage


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
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

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
        """
        从一键登录页面登录
        :return:
        """
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
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_in_me_all_page():
        """确保应用在消息页面"""

        # 如果在消息页，不做任何操作
        mess = MessagePage()
        mep = MePage()
        if mep.is_on_this_page():
            return
        if mess.is_on_this_page():
            mess.open_me_page()
            mep.is_on_this_page()
            return
        # 进入一键登录页
        Preconditions.make_already_in_message_page(reset=False)
        mess.open_me_page()

    @staticmethod
    def make_already_in_me_save_part_page():
        """确保编辑我的个人资料数据部分为空"""
        Preconditions.make_already_in_me_all_page()
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.点击进入编辑
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        mep1.input_name("姓名", "中国人123*#!!")
        mep1.edit_clear("公司")
        mep1.edit_clear("职位")
        # mep.swipe_up()
        mep1.edit_clear("邮箱")
        time.sleep(1)
        mep1.click_save()
        if mep1.is_toast_save_success():
            mep1.click_back()
        if mep1.is_toast_save():
            mep1.click_back()
            mup.click_back()
        else:
            pass

    @staticmethod
    def make_already_in_me_save_all_page():
        """确保编辑我的个人资料数据都完整"""
        Preconditions.make_already_in_me_all_page()
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.点击进入编辑
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        mep1.swipe_up()
        mep1.input_name("姓名", "中国人123*#!")
        mep1.input_name("公司", "中移科技有限公司")
        mep1.input_name("职位", "高级工程师123")
        # mep.swipe_up()
        mep1.input_name("邮箱", "958535269@qq.com")
        time.sleep(1)
        mep1.click_save()
        if mep1.is_toast_save_success():
            mep1.click_back()
        if mep1.is_toast_save():
            mep1.click_back()
            mup.click_back()
        else:
            pass


class MeAll(TestCase):
    """_
    模块：我的

    文件位置：全量/4.我模块全量测试用例-张淑丽.xlsx
    表格：我页面

    """

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_me_all_page()

    def default_tearDown(self):
        pass
        # current_mobile().disconnect_mobile()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_001(self):
        """我页面跳转验证"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        self.assertEquals(mep.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_002(self):
        """"我"模块页面信息显示验证"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        self.assertEquals(mep.is_on_this_page(), True)
        time.sleep(2.8)
        # 2.检查页面包含姓名，电话号码，查看并编辑人资料入口，个人头像，我的二维码入口,多方电话可用时长入口,和包支付,移动营业厅,福利
        self.assertEquals(mep.is_element_exist("姓名"), True)
        self.assertEquals(mep.is_element_exist("电话号码"), True)
        self.assertEquals(mep.is_element_exist("查看并编辑个人资料"), True)
        self.assertEquals(mep.is_element_exist("个人头像"), True)
        self.assertEquals(mep.is_element_exist("二维码入口"), True)
        self.assertEquals(mep.is_text_exist("多方电话可用时长"), True)
        self.assertEquals(mep.is_text_exist("和包支付"), True)
        self.assertEquals(mep.is_text_exist("移动营业厅"), True)
        self.assertEquals(mep.is_text_exist("福利"), True)
        mep.page_down()
        time.sleep(1)
        # 3.检查页面包含关于和飞信,推荐和飞信、帮助与反馈、设置
        self.assertEquals(mep.is_text_exist("关于和飞信"), True)
        self.assertEquals(mep.is_text_exist("推荐和飞信"), True)
        self.assertEquals(mep.is_text_exist("帮助与反馈"), True)
        self.assertEquals(mep.is_text_exist("设置"), True)
        mep.page_up()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_005(self):
        """个人资料界面信息显示验证"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.检查页面包含a、返回按钮，编辑按钮 .b、姓名，个人头像，手机号码，公司，职位，邮箱各字段信息显示正常  c、分享名片
        self.assertEquals(mup.is_element_exist("返回"), True)
        self.assertEquals(mup.is_text_exist("编辑"), True)
        self.assertEquals(mup.is_element_exist("姓名"), True)
        self.assertEquals(mup.is_element_exist("个人头像"), True)
        self.assertEquals(mup.is_text_exist("电话"), True)
        self.assertEquals(mup.is_text_exist("公司"), True)
        self.assertEquals(mup.is_text_exist("职位"), True)
        self.assertEquals(mup.is_text_exist("邮箱"), True)
        # 4.点击返回到我的页面
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_006(self):
        """个人资料界面信息显示验证"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.点击进入编辑
        mup.click_edit()
        mep = MeEditUserProfilePage()
        mep.wait_for_page_load()
        # 4.检验电话不能点击，姓名可以点击
        self.assertEquals(mep.element_is_click_able("电话"), False)
        self.assertEquals(mep.element_is_click_able("姓名"), True)
        # 5.检验姓名字符串不超过40个
        self.assertEquals(mep.get_element_text("姓名"), True)
        # 6.保存按钮灰色，点击弹框提示
        mep.click_save()
        self.assertEquals(mep.is_toast_save(), True)
        # 4.点击返回到我的页面
        mep.click_back()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_008(self):
        """个人资料详情-部分完善资料"""
        Preconditions.make_already_in_me_save_part_page()
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 4 a已完善的资料直接显示
        mup.element_contain_text("姓名", "中国人123*#!")
        mup.element_contain_text("电话", current_mobile().get_cards(CardType.CHINA_MOBILE)[0])
        # 4 b未补充的信息为空
        mup.element_contain_text("公司", "未设置")
        mup.element_contain_text("职位", "未设置")
        mup.element_contain_text("邮箱", "未设置")
        # 5.编辑个人信息
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.input_name("公司", "中移科技有限公司")
        mep1.click_save()
        self.assertEquals(mep1.is_toast_save_success(), True)
        mep1.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_009(self):
        """个人资料详情-全部完善资料"""
        Preconditions.make_already_in_me_save_all_page()
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 4 a已完善的资料直接显示
        self.assertEquals(mup.is_element_exist("个人头像"), True)
        mup.element_contain_text("姓名", "中国人123*#!")
        mup.element_contain_text("电话", current_mobile().get_cards(CardType.CHINA_MOBILE)[0])
        mup.element_contain_text("公司", "中移科技有限公司")
        mup.element_contain_text("职位", "高级工程师")
        mup.element_contain_text("邮箱", "958535269@qq.com")
        # 5.编辑个人信息
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.input_name("公司", "中移科技有限公司12")
        mep1.input_name("职位", "测试开发工程师12")
        mep1.click_save()
        self.assertEquals(mep1.is_toast_save_success(), True)
        mep1.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_010(self):
        """编辑个人资料-编辑状态"""
        Preconditions.make_already_in_me_save_all_page()
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 4.校验点
        mep1.input_name("姓名", "中国人321")
        self.assertEquals(mep1.element_is_enabled_able("保存"), True)
        self.assertEquals(mep1.element_is_enabled_able("编辑图片"), True)
        mep1.click_company()
        self.assertEquals(mep1.get_element_text("公司"), True)
        mep1.swipe_up()
        mep1.click_save()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_011(self):
        """进入“编辑资料”界面信息"""
        Preconditions.make_already_in_me_save_all_page()
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 4.校验点 a顶部显示返回按钮和保存按钮,b手机号不可编辑，可编辑的内容为：头像、姓名、公司、职位、邮箱
        self.assertEquals(mep1.is_element_exist("返回"), True)
        self.assertEquals(mep1.element_is_enabled_able("保存"), False)
        self.assertEquals(mep1.element_is_click_able("电话"), False)
        self.assertEquals(mep1.element_is_click_able("编辑图片"), True)
        self.assertEquals(mep1.element_is_click_able("姓名"), True)
        self.assertEquals(mep1.element_is_click_able("公司"), True)
        self.assertEquals(mep1.element_is_click_able("职位"), True)
        mep1.swipe_up()
        self.assertEquals(mep1.element_is_click_able("邮箱"), True)
        mep1.input_name("邮箱", "12345678@qq.com")
        self.assertEquals(mep1.element_is_enabled_able("保存"), True)
        # 5.点击编辑图像进入选择照片页面
        mep1.click_edit_pic()
        mep1.wait_for_select_pic_page_load()
        # 6.点击返回
        mep1.click_back()
        mep1.click_save()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_012(self):
        """“编辑资料” 头像设置"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 4.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        # 5.跳转到选择照片页面校验点
        # a隐藏弹窗
        mep1.click_back()
        mep1.wait_for_page_load()
        mep1.click_edit_pics()
        # b调起‘拍照窗口’
        mep1.click_take_pics()
        mep1.click_taking_pics()
        mep1.click_save_pics()
        mep1.click_back()
        time.sleep(1)
        # c跳转到选择照片页面
        mep1.click_select_pics(1)
        time.sleep(1)
        self.assertEquals(mep1.is_element_exist("照片框"), True)
        mep1.click_back()
        mep1.click_back()
        mep1.click_back()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_013(self):
        """“编辑资料” 头像设置"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        # 3. a点击拍照，重拍|使用照片
        mep1.click_take_pics()
        mep1.click_taking_pics()
        time.sleep(1)
        self.assertEquals(mep1.element_is_click_able("取消照片"), True)
        # 4. 点击拍照完成
        mep1.click_save_pics()
        # 5.返回
        mep1.click_back()
        mep1.click_back()
        mep1.click_back()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_014(self):
        """“编辑资料” 头像设置"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        # 3. a点击拍照，重拍|使用照片
        mep1.click_take_pics()
        mep1.click_taking_pics()
        time.sleep(2)
        self.assertEquals(mep1.element_is_click_able("取消照片"), True)
        # 4. 点击选择重拍
        mep1.click_cancel_pics()
        self.assertEquals(mep1.is_element_exist("拍照"), True)
        # 5.点击返回
        mep1.click_taking_pics()
        mep1.click_save_pics()
        mep1.click_back()
        mep1.click_back()
        mep1.click_back()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_015(self):
        """“编辑资料” 头像设置"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        # 3.a点击拍照，重拍|使用照片
        mep1.click_take_pics()
        mep1.click_taking_pics()
        time.sleep(2)
        self.assertEquals(mep1.element_is_click_able("取消照片"), True)
        # 4.点击完成，选择使用照片，跳转到“头像截取”界面
        mep1.click_save_pics()
        time.sleep(1)
        self.assertEquals(mep1.is_element_exist("照片框"), True)
        # 5.点击返回
        mep1.click_back()
        mep1.click_back()
        mep1.click_back()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_016(self):
        """“编辑资料” 头像设置"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        # 3.a点击拍照，重拍|使用照片
        mep1.click_take_pics()
        mep1.click_taking_pics()
        time.sleep(2)
        self.assertEquals(mep1.element_is_click_able("取消照片"), True)
        # 4.点击完成，选择使用照片，跳转到“头像截取”界面
        mep1.click_save_pics()
        time.sleep(1)
        self.assertEquals(mep1.is_element_exist("照片框"), True)
        # 5.点击保存截图,返回到资料编辑页面
        mep1.click_save_save_pics()
        mep1.wait_for_page_load()
        mep1.click_back()
        mep1.click_cancel_mod()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_017(self):
        """“编辑资料” 头像设置"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        # 3.a点击拍照，重拍|使用照片
        mep1.click_take_pics()
        mep1.click_taking_pics()
        time.sleep(2)
        self.assertEquals(mep1.element_is_click_able("取消照片"), True)
        # 4.点击完成，选择使用照片，跳转到“头像截取”界面
        mep1.click_save_pics()
        time.sleep(1)
        self.assertEquals(mep1.is_element_exist("照片框"), True)
        # 5.点击保存截图,返回到资料编辑页面
        mep1.click_save_save_pics()
        mep1.wait_for_page_load()
        mep1.click_save()
        self.assertEquals(mep1.is_toast_save_success(), True)
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_018(self):
        """“编辑资料” 头像设置"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        self.assertEquals(mep1.is_element_exist("点击拍照"), True)
        # 3.点击选择图片
        mep1.click_select_pics(1)
        time.sleep(2)
        self.assertEquals(mep1.is_element_exist("照片框"), True)
        # 4.点击返回
        mep1.click_back()
        mep1.click_back()
        mep1.click_back()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_020(self):
        """“编辑资料” 头像设置"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        self.assertEquals(mep1.is_element_exist("点击拍照"), True)
        # 3.点击选择图片，跳转到“头像截取”界面
        mep1.click_select_pics(1)
        time.sleep(2)
        self.assertEquals(mep1.is_element_exist("照片框"), True)
        # 4.选择使用照片，跳转到“头像截取”界面，点击保存
        mep1.click_save_save_pics()
        mep1.wait_for_page_load()
        mep1.click_save()
        self.assertEquals(mep1.is_toast_save_success(), True)
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_021(self):
        """“编辑资料” 头像设置-多次选择图片"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        self.assertEquals(mep1.is_element_exist("点击拍照"), True)
        # 3.点击选择图片，跳转到“头像截取”界面
        mep1.click_select_pics(0)
        time.sleep(2)
        self.assertEquals(mep1.is_element_exist("照片框"), True)
        # 4.点击返回按钮，重新选取照片
        mep1.click_back()
        time.sleep(1)
        mep1.click_select_pics(1)
        # 5.点击保存
        mep1.click_save_save_pics()
        mep1.wait_for_page_load()
        mep1.click_save()
        self.assertEquals(mep1.is_toast_save_success(), True)
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_024(self):
        """“编辑资料” 头像设置"""
        # 0-1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 0-2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 1.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        # 2.点击进入照相
        mep1.click_edit_pics()
        mep1.wait_for_select_pic_page_load()
        self.assertEquals(mep1.is_element_exist("点击拍照"), True)
        # 3.点击选择图片，跳转到“头像截取”界面
        mep1.click_select_pics(1)
        time.sleep(2)
        self.assertEquals(mep1.is_element_exist("照片框"), True)
        # 4.选择使用照片，跳转到“头像截取”界面，点击保存，上传头像
        mep1.click_save_save_pics()
        mep1.wait_for_page_load()
        # 5.在编辑个人资料页面点击返回按钮，不保存
        mep1.click_back()
        time.sleep(1)
        self.assertEquals(mep1.is_text_exist("当前资料已修改，是否保存"), True)
        mep1.click_cancel_mod()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_025(self):
        """“编辑资料” 所有输入栏 为空"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.所有输入栏信息为空
        mep1.edit_clear("姓名")
        mep1.edit_clear("公司")
        mep1.edit_clear("职位")
        mep1.edit_clear("邮箱")
        mep1.click_save()
        self.assertEquals(mep1.is_toast_save_null(), True)
        # 5.点击返回
        mep1.click_back()
        mep1.click_cancel_mod()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_026(self):
        """“编辑资料” 除了姓名,其他为空"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.所有输入栏信息为空
        mep1.input_name("姓名", "123")
        mep1.edit_clear("公司")
        mep1.edit_clear("职位")
        mep1.edit_clear("邮箱")
        mep1.click_save()
        self.assertEquals(mep1.is_toast_save_success(), True)
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_027(self):
        """“验证我-个人资料-编辑-编辑名称"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.正确输入并点击保存（中文、英文、特殊符号）
        mep1.input_name("姓名", "周星星123@！#")
        mep1.click_save()
        self.assertEquals(mep1.is_toast_save_success(), True)
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_028(self):
        """“验证我-个人资料-编辑-编辑名称"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        mep.set_network_status(0)
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.正确输入并点击保存（中文、英文、特殊符号）
        mep1.input_name("姓名", "周星星123@！#%12")
        mep1.click_save()
        self.assertEquals(mep1.is_toast_net(), True)
        # 5点击返回，并恢复网络
        mep1.click_back()
        mep1.click_cancel_mod()
        mup.click_back()
        mup.set_network_status(6)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_029(self):
        """“编辑资料” 姓名栏输入超长字符"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.姓名输入超长字符串，提示格式错误
        mep1.input_name("姓名", "周星星123@！#" * 50)
        self.assertEquals(mep1.is_toast_format("姓名"), True)
        self.assertEquals(mep1.get_element_text("姓名"), True)
        mep1.click_back()
        mep1.click_cancel_mod()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_030(self):
        """“编辑资料” 公司栏输入超长字符"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.姓名输入超长字符串，提示格式错误
        mep1.input_name("公司", "周星星123@！#" * 50)
        self.assertEquals(mep1.is_toast_format("公司"), True)
        # 5.点击返回
        mep1.click_back()
        mep1.click_cancel_mod()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_031(self):
        """“编辑资料” 职位栏输入超长字符"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.职位输入超长字符串，提示格式错误
        mep1.input_name("职位", "周星星123@！#" * 50)
        self.assertEquals(mep1.is_toast_format("职位"), True)
        # 5.点击返回
        mep1.click_back()
        mep1.click_cancel_mod()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_032(self):
        """“编辑资料” 邮箱栏输入超长字符"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.职位输入超长字符串，提示格式错误
        mep1.swipe_up()
        mep1.input_name("邮箱", "周星星123@！#" * 50)
        self.assertEquals(mep1.is_toast_format("邮箱"), True)
        # 5.点击返回
        time.sleep(1)
        mep1.click_back()
        mep1.click_cancel_mod()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_034(self):
        """“编辑资料” “编辑资料” 邮箱字段空格"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        # 4.职位输入带空格的字符串
        mep1.swipe_up()
        mep1.input_name("邮箱", " 9 58535269 @ qq.com ")
        mep1.click_save()
        # 5.点击返回
        if mep1.is_toast_save():
            mep1.click_back()
            mup.click_back()
        if mep1.is_toast_save_success():
            mup.click_back()
        else:
            pass

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_035(self):
        """编辑个人资料-编辑之后返回"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,保存按钮置灰不可点
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        self.assertEquals(mep1.element_is_enabled_able("保存"), False)
        # 5.编辑信息后，点击取消
        mep1.input_name("姓名", "我是周星星")
        self.assertEquals(mep1.element_is_enabled_able("保存"), True)
        mep1.click_back()
        time.sleep(1)
        self.assertEquals(mep1.is_text_exist("当前资料已修改，是否保存"), True)
        mep1.click_cancel_mod()
        # 6.编辑信息后，点击保存
        mup.click_edit()
        mep1.wait_for_page_load()
        mep1.input_name("姓名", "我是周星星")
        mep1.click_back()
        time.sleep(1)
        self.assertEquals(mep1.is_text_exist("当前资料已修改，是否保存"), True)
        mep1.click_save_mod()
        self.assertEquals(mep1.is_toast_save_success(), True)
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_036(self):
        """编辑个人资料-编辑之后断网保存"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入查看并编辑资料
        mep.click_view_edit()
        mup = MeViewUserProfilePage()
        mup.wait_for_page_load()
        # 3.进入个人编辑页面信息,保存按钮置灰不可点
        mup.click_edit()
        mep1 = MeEditUserProfilePage()
        mep1.wait_for_page_load()
        self.assertEquals(mep1.element_is_enabled_able("保存"), False)
        # 5.编辑信息后，点击取消
        mep1.input_name("姓名", "我是周星星54321")
        self.assertEquals(mep1.element_is_enabled_able("保存"), True)
        # 6.断网保存
        mep1.set_network_status(0)
        mep1.click_save()
        self.assertEquals(mep1.is_toast_net(), True)
        # 7.连网返回
        mep1.set_network_status(6)
        mep1.click_back()
        mep1.click_cancel_mod()
        mup.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_037(self):
        """我的二维码"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击进入二维码
        mep.click_qr_code_icon()
        qr_code = MyQRCodePage()
        qr_code.wait_for_loading_animation_end()
        self.assertEquals(qr_code.is_element_exist("二维码"), True)
        self.assertEquals(qr_code.is_element_exist("二维码中的名称"), True)
        self.assertEquals(qr_code.is_element_exist("二维码中的头像"), True)
        self.assertEquals(qr_code.is_element_exist("分享二维码"), True)
        self.assertEquals(qr_code.is_element_exist("保存二维码"), True)
        # 3.点击返回
        qr_code.click_back()
        time.sleep(1)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_038(self):
        """我的二维码-网络异常"""
        # 1.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 2.断网点击进入二维码
        mep.set_network_status(0)
        mep.click_qr_code_icon()
        qr_code = MyQRCodePage()
        self.assertEquals(qr_code.is_toast_exist("获取失败"), True)
        self.assertEquals(qr_code.is_text_present("二维码加载失败"), True)
        # 3.恢复网络后返回
        mep.set_network_status(6)
        qr_code.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_039(self):
        """我的二维码-分享"""
        # 0.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 1.点击个人二维码
        mep.click_qr_code_icon()
        qr_code = MyQRCodePage()
        qr_code.wait_for_loading_animation_end()
        # 2、点击“分享我的二维码”
        qr_code.click_forward_qr_code()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        # 3.点击返回
        scg.click_back()
        qr_code.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_040(self):
        """我的二维码分享-关键字搜索"""
        # 0.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 1.点击个人二维码
        mep.click_qr_code_icon()
        qr_code = MyQRCodePage()
        qr_code.wait_for_loading_animation_end()
        # 2、点击“分享我的二维码”
        qr_code.click_forward_qr_code()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        # 3、点击搜索框，输入信息
        scg.click_search_keyword()
        scg.input_search_keyword("给1234%6在$")
        time.sleep(1)
        # 4.检验有结果和无结果两种情况
        self.assertEquals(scg.page_contain_element('X'), True)
        self.assertEquals(scg.get_element_texts("最近聊天"), True)
        if scg.is_text_present("本地联系人"):
            self.assertEquals(scg.get_element_texts("local联系人"), True)
        # 5.点击返回
        scg.click_back()
        qr_code.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_041(self):
        """我的二维码分享-关键字搜索"""
        # 0.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 1.点击个人二维码
        mep.click_qr_code_icon()
        qr_code = MyQRCodePage()
        qr_code.wait_for_loading_animation_end()
        # 2、点击“分享我的二维码”
        qr_code.click_forward_qr_code()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        # 3、点击搜索框，输入信息
        scg.click_search_keyword()
        scg.input_search_keyword("+861591873097")
        time.sleep(1)
        # 4.检验有结果和无结果两种情况
        self.assertEquals(scg.page_contain_element('X'), True)
        self.assertEquals(scg.get_element_texts("最近聊天"), True)
        if scg.is_text_present("本地联系人"):
            self.assertEquals(scg.get_element_texts("聊天电话"), True)
        # 5.点击返回
        scg.click_back()
        qr_code.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_042(self):
        """我的二维码分享-非手机号码的数字搜索"""
        # 0.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 1.点击个人二维码
        mep.click_qr_code_icon()
        qr_code = MyQRCodePage()
        qr_code.wait_for_loading_animation_end()
        # 2、点击“分享我的二维码”
        qr_code.click_forward_qr_code()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        # 3、点击搜索框，输入信息
        scg.click_search_keyword()
        scg.input_search_keyword("15918730974")
        time.sleep(1)
        # 4.检验有结果和无结果两种情况
        self.assertEquals(scg.page_contain_element('X'), True)
        self.assertEquals(scg.get_element_texts("最近聊天"), True)
        if scg.is_text_present("本地联系人"):
            self.assertEquals(scg.get_element_texts("聊天电话"), True)
        # 5.点击返回
        scg.click_back()
        qr_code.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me1')
    def test_me_all_page_043(self):
        """我的二维码分享-无本地结果且二次查询无结果"""
        # 0.检验是否跳转到我页面
        mep = MePage()
        mep.is_on_this_page()
        # 1.点击个人二维码
        mep.click_qr_code_icon()
        qr_code = MyQRCodePage()
        qr_code.wait_for_loading_animation_end()
        # 2、点击“分享我的二维码”
        qr_code.click_forward_qr_code()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        # 3、点击搜索框，输入信息
        scg.click_search_keyword()
        scg.input_search_keyword("我们是谁？")
        time.sleep(1)
        # 4.检验无结果
        self.assertEquals(scg.page_contain_element('X'), True)
        self.assertEquals(scg.get_element_texts("最近聊天"), True)
        # 5.点击二次搜索
        scg.click_search_he_contact()
        time.sleep(1.8)
        self.assertEquals(scg.is_text_present("无搜索结果"), True)
        # 6.点击返回
        scg.click_element(["id", 'com.chinasofti.rcs:id/btn_back'])
        scg.click_back()
        qr_code.click_back()




