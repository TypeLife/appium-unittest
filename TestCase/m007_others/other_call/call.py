import time
from appium.webdriver.common.mobileby import MobileBy
from library.core.utils.applicationcache import current_mobile
from pages.components import ContactsSelector
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, ContactSecltorPage, \
    SelectContactsPage, CalllogBannerPage, MessagePage, SearchPage, LabelGroupingPage, GroupListPage, \
    GroupListSearchPage, LableGroupDetailPage
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags


class Preconditions(LoginPreconditions):
    """前置条件"""


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_call_wangqiong_0057():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0057(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.click_one_contact('联系人3')
        selectcontacts.click_one_contact('联系人4')
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))
        time.sleep(3)
        # 接听和飞信电话  为自动接听
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(6)
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0059(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.click_one_contact('联系人3')
        selectcontacts.click_one_contact('联系人4')
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))
        time.sleep(5)
        # 接听和飞信电话  为自动接听
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(3)
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(4)
        # 挂断电话返回到通话页面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0063(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.click_one_contact('联系人3')
        selectcontacts.click_one_contact('联系人4')
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 点击多方通话详情
        call_page.click_element((MobileBy.XPATH,
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout[2]'),
                                auto_accept_permission_alert=False)

        time.sleep(3)
        # 再次呼叫并接听和飞信电话
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/call_again'))
        time.sleep(5)
        # 挂断电话
        callcontact._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        callcontact.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        time.sleep(3)
        # 挂断电话回到多方通话界面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @staticmethod
    def setUp_test_call_wangqiong_0071():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0071(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    labellist.click_one_contact('联系人3')
                if not b:
                    labellist.click_one_contact('联系人4')
                labellist.click_sure()
        else:
            labellist.click_one_contact('联系人3')
            labellist.click_one_contact('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))
        labellist.click_one_contact('联系人3')
        labellist.click_one_contact('联系人4')
        time.sleep(3)
        labellist.click_sure()
        time.sleep(8)
        # 接听和飞信电话后挂断电话
        labellist._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        labellist.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @staticmethod
    def setUp_test_call_wangqiong_0073():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0073(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    labellist.click_one_contact('联系人3')
                if not b:
                    labellist.click_one_contact('联系人4')
                labellist.click_sure()
        else:
            labellist.click_one_contact('联系人3')
            labellist.click_one_contact('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        # 进入群发消息界面并点击多方通话

        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_second_colum'),
                                auto_accept_permission_alert=False)
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                                auto_accept_permission_alert=False)
        labellist.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and ' + '@text="多方电话"]'))
        time.sleep(3)
        labellist.click_one_contact('联系人3')
        labellist.click_one_contact('联系人4')
        time.sleep(3)
        labellist.click_sure()
        time.sleep(8)
        # 接听和飞信电话后挂断电话
        labellist._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        labellist.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @staticmethod
    def setUp_test_call_wangqiong_0080():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0080(self):
        # 通讯录界面搜索姓名
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("联系人3")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '联系人3')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))

    @staticmethod
    def setUp_test_call_wangqiong_0081():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18351994357')
        contactspage.create_contacts_if_not_exits('联系人4', '18351994307')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0081(self):
        # 通讯录界面搜索姓名
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("联系人")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '联系人')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))

    @staticmethod
    def setUp_test_call_wangqiong_0086():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0086(self):
        # 通讯录界面搜索姓名
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("18311111111")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("联系人3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18311111111')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))
        call_page.click_back()
        call_page.click_back()

        # 打开拨号键
        call_page.click_call()
        call_page.dial_number('18311111111')
        self.assertTrue(current_mobile().is_text_present('联系人3'))
        # 选择联系人正常展示
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' + '@text="联系人3"]'))

    @staticmethod
    def setUp_test_call_wangqiong_0087():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0087(self):
        # 通讯录界面搜索姓名
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(3)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '1')
        call_page.hide_keyboard()

        # 输入11位数字进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18311111111')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]')))
        # 点击搜素到的结果
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))

        call_page.click_back()

        # 打开拨号键
        call_page.click_call()
        call_page.dial_number('18311111111')
        self.assertTrue(current_mobile().is_text_present('联系人3'))
        # 选择联系人正常展示
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' + '@text="联系人3"]'))

    @staticmethod
    def setUp_test_call_wangqiong_0088():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0088(self):
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(3)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18312345678')
        call_page.hide_keyboard()

        # 校验是否搜索到未知号码
        SelectContactsPage().is_present_unknown_member()
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="18312345678(未知号码)"]'))
        time.sleep(3)
        call_page.click_back()

    @staticmethod
    def setUp_test_call_wangqiong_0119():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0119(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('联系人3')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0120():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0120(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('联系人')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0126():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0126(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('18311111111')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @staticmethod
    def setUp_test_call_wangqiong_0127():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0127(self):
        # 通讯录界面搜索姓名
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        # 输入9位数 查看是否正匹配到数据
        contact_search.input_search_keyword('18311111')
        self.assertTrue(contact_search.is_contact_in_list('联系人3'))
        contact_search.click_contact('联系人3')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0145(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.click_one_contact('联系人3')
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        time.sleep(4)
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(2)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' +
                                       '@text="联系人3"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0146(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人1', '18312345678')
        contactspage.create_contacts_if_not_exits('联系人2', '18323456789')
        contactspage.create_contacts_if_not_exits('联系人3', '13812345678')
        contactspage.create_contacts_if_not_exits('联系人4', '13823456789')
        contactspage.create_contacts_if_not_exits('联系人5', '13811111111')
        contactspage.create_contacts_if_not_exits('联系人6', '13822222222')
        contactspage.create_contacts_if_not_exits('联系人7', '13833333333')
        contactspage.create_contacts_if_not_exits('联系人8', '13844444444')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人1')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人1"]'))
        selectcontacts.search('联系人2')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人2"]'))
        selectcontacts.search('联系人3')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人3"]'))
        selectcontacts.search('联系人4')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人4"]'))
        selectcontacts.search('联系人5')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人5"]'))
        selectcontacts.search('联系人6')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人6"]'))
        selectcontacts.search('联系人7')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人7"]'))
        selectcontacts.search('联系人8')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人8"]'))
        time.sleep(5)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(3)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallTime" and ' +
                                       '@text="刚刚"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0147(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人1', '18312345678')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        time.sleep(4)
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人1')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人1"]'))
        selectcontacts.search('18311111111')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18322222222')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18333333333')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18333333333')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18344444444')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18355555555')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18366666666')
        selectcontacts.click_unknown_member()

        time.sleep(5)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(4)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallTime" and ' +
                                       '@text="刚刚"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @staticmethod
    def setUp_test_call_wangqiong_0155():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入群聊分组页签
        contactspage.open_group_chat_list()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0155(self):
        # 创建标签分组
        grouppage = GroupListPage()
        # 创建群聊1
        grouppage.create_group_chats_if_not_exits('群聊1', ["联系人3", "联系人4"])
        # 进入群聊的多方电话
        grouppage.click_group('群聊1')
        grouppage.click_mult_call_icon()
        time.sleep(3)
        grouppage.click_element((MobileBy.XPATH, "//*[@text='多方电话']"))

        # 选择成员进行多方电话

        time.sleep(10)

    @staticmethod
    def setUp_test_call_wangqiong_0157():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入群聊分组页签
        contactspage.open_group_chat_list()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0157(self):
        # 创建标签分组
        grouppage = GroupListPage()
        # 创建群聊1
        grouppage.create_group_chats_if_not_exits('群聊1', ["联系人3", "联系人4"])
        # 进入群聊的多方电话
        grouppage.click_search_input()
        groupserch = GroupListSearchPage()
        groupserch.input_search_keyword('群聊1')
        # 点击群聊1
        groupserch.click_group('群聊1')
        grouppage.click_mult_call_icon()
        time.sleep(3)
        grouppage.click_element((MobileBy.XPATH, "//*[@text='多方电话']"))

        contactselect = ContactsSelector()
        # 选择自己进行多方电话,弹框该联系人不可选择,呼叫按钮任然置灰
        contactselect.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/index_text'))
        current_mobile().assert_element_should_be_disabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

    @staticmethod
    def setUp_test_call_wangqiong_0171():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        # contactspage.create_contacts_if_not_exits('A联系人', '18311111111')
        # contactspage.create_contacts_if_not_exits('B联系人', '18322222222')
        # contactspage.create_contacts_if_not_exits('C联系人', '18333333333')
        # contactspage.create_contacts_if_not_exits('D联系人', '18344444444')
        # contactspage.create_contacts_if_not_exits('E联系人', '18355555555')
        # contactspage.create_contacts_if_not_exits('F联系人', '18366666666')
        # contactspage.create_contacts_if_not_exits('G联系人', '18377777777')
        # contactspage.create_contacts_if_not_exits('H联系人', '18388888888')
        # contactspage.create_contacts_if_not_exits('I联系人', '18399999999')
        # contactspage.create_contacts_if_not_exits('J联系人', '13822222222')
        # contactspage.create_contacts_if_not_exits('K联系人', '13811111111')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0171(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组A')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组A')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    labellist.click_one_contact('联系人3')
                if not b:
                    labellist.click_one_contact('联系人4')
                labellist.click_sure()

        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.create_group('分组A', ["A联系人", "B联系人", "C联系人"])
        # labellist.create_group('分组A', ['A联系人', 'B联系人', 'C联系人', 'D联系人', 'E联系人', 'F联系人', 'G联系人', 'H联系人', 'I联系人', 'J联系人', 'K联系人'])
        labellist.click_label_group('分组A')
        # 进入多方通话
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))
        # 查看时长
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs: id/multi_time_tip'))
        self.assertTrue(labellist.is_text_present((MobileBy.XPATH, '//*[contains(@text, "分钟")]')))

        # 按照字母滑动
        contact = ContactsPage()
        contact.click_element(
            ('xpath', '//*[@resource-id="com.chinasofti.rcs:id/indexbarview"]'))
        elements = contact.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'))
        for i in range(len(elements)):
            elements[i].click()
        # 判断右侧字符是否按顺序排列
        current_mobile().is_right_letters_sorted()

    @staticmethod
    def setUp_test_call_wangqiong_0179():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0179(self):
        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    labellist.click_one_contact('联系人3')
                if not b:
                    labellist.click_one_contact('联系人4')
                labellist.click_sure()
        else:
            # 新建分组 选择分组成员
            labellist.click_one_contact('联系人3')
            labellist.click_one_contact('联系人4')
            labellist.click_sure()
            labellist.select_group('分组1')
        # 点击多方电话
        labeldeatilpage = LableGroupDetailPage()
        labeldeatilpage.click_multi_tel()

        # 通过11位号码选择联系人 看是否能精准匹配到联系人
        from pages import SelectLocalContactsPage

        selectpage = SelectLocalContactsPage()
        selectpage.search('18311111111')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0180():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0180(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                labelpage.click_one_contact('联系人3')
            if not b:
                labelpage.click_one_contact('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入1位数 查看是否能模糊匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('1')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0181():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0181(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                labelpage.click_one_contact('联系人3')
            if not b:
                labelpage.click_one_contact('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入全名 查看是否能精准匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('联系人3')
        time.sleep(3)
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0182():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')
        # 进入标签分组页签
        contactspage.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0182(self):
        # 创建标签分组
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '联系人3', '联系人4')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('联系人3')
        b = labelpage.is_contacter_in_lable('联系人4')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                labelpage.click_one_contact('联系人3')
            if not b:
                labelpage.click_one_contact('联系人4')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入非全名 查看是否能模糊匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('联系人')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "联系人3")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0193():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0193(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人3', '18311111111')
        contactspage.create_contacts_if_not_exits('联系人4', '18322222222')

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_element((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall"))
        # 选择指定联系人 点击呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人3')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="联系人3"]'))
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
            callcontact.get_source()
        if not callcontact._is_element_present((MobileBy.XPATH, "//*[contains(@text, '我')]")):
            callcontact.click_element((MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button'), 1,
                                      False)

        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(6)
        callpage = CallPage()
        callpage.hang_up_hefeixin_call()
        time.sleep(3)
        #
        # 挂断电话回到多方通话界面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))






