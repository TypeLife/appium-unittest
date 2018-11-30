from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatGroupSMSSelectContactsPage(BasePage):
    """选择短信发送人界面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupSMSSendeeActivity'

    __locators = {'': (MobileBy.ID, ''),
 'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
 'android:id/content': (MobileBy.ID, 'android:id/content'),
 'com.chinasofti.rcs:id/title_view': (MobileBy.ID, 'com.chinasofti.rcs:id/title_view'),
 'com.chinasofti.rcs:id/back_rl': (MobileBy.ID, 'com.chinasofti.rcs:id/back_rl'),
 'com.chinasofti.rcs:id/left_back': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
 '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/title_text'),
 '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/sure_text'),
 'com.chinasofti.rcs:id/layout_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_search'),
 '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
 'com.chinasofti.rcs:id/layout_allcheck_contactlist': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_allcheck_contactlist'),
 '全选': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_check_all'),
 'com.chinasofti.rcs:id/recyclerView_recently_person': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_recently_person'),
 'com.chinasofti.rcs:id/root_view': (MobileBy.ID, 'com.chinasofti.rcs:id/root_view'),
 'M': (MobileBy.ID, ''),
 'com.chinasofti.rcs:id/contact_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_icon'),
 'mobile0489': (MobileBy.ID, 'com.chinasofti.rcs:id/me_gorup_name'),
 'N': (MobileBy.ID, ''),
 '你大爷': (MobileBy.ID, 'com.chinasofti.rcs:id/me_gorup_name'),
 'com.chinasofti.rcs:id/contact_index_bar_view': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
 'com.chinasofti.rcs:id/contact_index_bar_container': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container')
}
