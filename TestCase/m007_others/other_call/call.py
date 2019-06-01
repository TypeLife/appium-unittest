import time
from appium.webdriver.common.mobileby import MobileBy
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, ContactSecltorPage, \
    SelectContactsPage, CalllogBannerPage
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













