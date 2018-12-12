from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage


class WorkbenchPage(FooterPage):
    """工作台主页"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
                  'com.chinasofti.rcs:id/home_tag_view_pager': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
                  'com.chinasofti.rcs:id/constraintLayout_home_tab': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
                  'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
                  'com.chinasofti.rcs:id/actionbar_main_enterprise': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/actionbar_main_enterprise'),
                  '当前团队名称:myteam02': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
                  'com.chinasofti.rcs:id/swipeToLoad': (MobileBy.ID, 'com.chinasofti.rcs:id/swipeToLoad'),
                  'com.chinasofti.rcs:id/swipe_target': (MobileBy.ID, 'com.chinasofti.rcs:id/swipe_target'),
                  'com.chinasofti.rcs:id/ll_viewpager': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_viewpager'),
                  '容器列表': (MobileBy.ID, 'com.chinasofti.rcs:id/viewpager'),
                  'com.chinasofti.rcs:id/card_view': (MobileBy.ID, 'com.chinasofti.rcs:id/card_view'),
                  '广告banner': (MobileBy.ID, 'com.chinasofti.rcs:id/card_banner_view'),
                  'com.chinasofti.rcs:id/image': (MobileBy.ID, 'com.chinasofti.rcs:id/image'),
                  'com.chinasofti.rcs:id/group': (MobileBy.ID, 'com.chinasofti.rcs:id/group'),
                  'com.chinasofti.rcs:id/fl_work_config': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_work_config'),
                  'com.chinasofti.rcs:id/rl_category': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_category'),
                  'com.chinasofti.rcs:id/iv_head': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
                  '管理控制台（仅管理员可见）': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '权益': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_expanded'),
                  'com.chinasofti.rcs:id/member_list': (MobileBy.ID, 'com.chinasofti.rcs:id/member_list'),
                  'com.chinasofti.rcs:id/rl_item': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_item'),
                  'com.chinasofti.rcs:id/view_header_space': (MobileBy.ID, 'com.chinasofti.rcs:id/view_header_space'),
                  'com.chinasofti.rcs:id/rl_icon_content': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_icon_content'),
                  'com.chinasofti.rcs:id/iv_iron': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_iron'),
                  '组织架构': (MobileBy.XPATH, '//*[@text="组织架构"]'),
                  '工作台管理': (MobileBy.XPATH, '//*[@text="工作台管理"]'),
                  '邀请成员': (MobileBy.XPATH, '//*[@text="邀请成员"]'),
                  '管理员指引': (MobileBy.XPATH, '//*[@text="管理员指引"]'),
                  'com.chinasofti.rcs:id/ll_content': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_content'),
                  '常用应用': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '公告信息': (MobileBy.XPATH, '//*[@text="公告信息"]'),
                  '企业新闻': (MobileBy.XPATH, '//*[@text="企业新闻"]'),
                  '企业通讯录': (MobileBy.XPATH, '//*[@text="企业通讯录"]'),
                  '团队通讯': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '超级会议': (MobileBy.XPATH, '//*[@text="超级会议"]'),
                  '群发信使': (MobileBy.XPATH, '//*[@text="群发信使"]'),
                  '语音通知': (MobileBy.XPATH, '//*[@text="语音通知"]'),
                  '139邮箱': (MobileBy.XPATH, '//*[@text="139邮箱"]'),
                  '协同办公': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '考勤打卡': (MobileBy.XPATH, '//*[@text="考勤打卡"]'),
                  '审批': (MobileBy.XPATH, '//*[@text="审批"]'),
                  '日志': (MobileBy.XPATH, '//*[@text="日志"]'),
                  '重要事项': (MobileBy.XPATH, '//*[@text="重要事项"]'),
                  '个人应用': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_category'),
                  '咪咕影院': (MobileBy.XPATH, '//*[@text="咪咕影院"]'),
                  '帮助中心': (MobileBy.XPATH, '//*[@text="帮助中心"]'),
                  '岭南优品': (MobileBy.XPATH, '//*[@text="岭南优品"]'),
                  'com.chinasofti.rcs:id/rl_bottom': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_bottom'),
                  'com.chinasofti.rcs:id/recyclerView': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
                  '应用商城': (MobileBy.XPATH, '//*[@text="应用商城"]'),
                  'com.chinasofti.rcs:id/iv_logo': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_logo'),
                  '应用管理': (MobileBy.XPATH, '//*[@text="应用管理"]'),
                  '咨询客服': (MobileBy.XPATH, '//*[@text="咨询客服"]'),
                  '创建团队': (MobileBy.XPATH, '//*[@text="创建团队"]'),
                  '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
                  '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
                  '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
                  '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
                  '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe')
                  }

