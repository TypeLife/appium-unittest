from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage


class NewContactPage(BasePage):
    """新建\编辑个人详情"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.NewContactActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/contact_edit_common': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_edit_common'),
        'com.chinasofti.rcs:id/left_back_btn_edit': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back_btn_edit'),
        'com.chinasofti.rcs:id/save': (MobileBy.ID, 'com.chinasofti.rcs:id/save'),
        '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/preservation_tv'),
        '姓名   *': (MobileBy.ID, 'com.chinasofti.rcs:id/name_tv'),
        '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_name'),
        'com.chinasofti.rcs:id/view1': (MobileBy.ID, 'com.chinasofti.rcs:id/view1'),
        '电话   *': (MobileBy.ID, 'com.chinasofti.rcs:id/phone_tv'),
        '12560': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_phone'),
        'com.chinasofti.rcs:id/view2': (MobileBy.ID, 'com.chinasofti.rcs:id/view2'),
        'com.chinasofti.rcs:id/ll_company': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_company'),
        '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/company_tv'),
        '输入公司': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_company'),
        'com.chinasofti.rcs:id/view3': (MobileBy.ID, 'com.chinasofti.rcs:id/view3'),
        'com.chinasofti.rcs:id/ll_job': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_job'),
        '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/job_tv'),
        '输入职位': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_job'),
        'com.chinasofti.rcs:id/view4': (MobileBy.ID, 'com.chinasofti.rcs:id/view4'),
        'com.chinasofti.rcs:id/ll_email': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_email'),
        '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/email_tv'),
        '输入邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_contact_email'),
        'com.chinasofti.rcs:id/view5': (MobileBy.ID, 'com.chinasofti.rcs:id/view5'),
        '删除联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/delete'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
    }
