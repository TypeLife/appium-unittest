import time
from pages import *
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
import random
from library.core.common.simcardtype import CardType
from pages.workbench.manager_console.WorkbenchManagerPage import WorkBenchManagerPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.voice_notice.VoiceNotice import VoiceNoticePage

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


class LoginPreconditions(object):
    """登录前置条件"""

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
        one_key.wait_for_page_load()
        # one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        if one_key.have_read_agreement_detail():
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
        LoginPreconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        else:
            try:
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                LoginPreconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                LoginPreconditions.login_by_one_key_login()

    @staticmethod
    def enter_private_chat_page(reset=False):
        """进入单聊会话页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        chat = SingleChatPage()
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()
        # 点击消息进入单聊会话页面
        cdp.click_message_icon()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        chat.wait_for_page_load()


class WorkbenchPreconditions(LoginPreconditions):
    """工作台前置条件"""

    @staticmethod
    def enter_create_team_page(reset=False):
        """从消息进入创建团队页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_create_team()
        team = CreateTeamPage()
        team.wait_for_page_load()

    @staticmethod
    def get_team_name():
        """获取团队"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # str=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        team_name = "ateam" + phone_number[-4:]
        return team_name

    @staticmethod
    def create_team(team_name=None, user_name="admin"):
        """创建团队"""
        if not team_name:
            team_name = WorkbenchPreconditions.get_team_name()
        team = CreateTeamPage()
        team.input_team_name(team_name)
        team.choose_location()
        team.choose_industry()
        team.input_real_name(user_name)
        # 立即创建团队
        team.click_immediately_create_team()
        # 点击完成设置工作台
        team.wait_for_setting_workbench_page_load()
        team.click_finish_setting_workbench()
        team.wait_for_create_team_success_page_load()
        # 进入工作台
        team.click_enter_workbench()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @staticmethod
    def enter_organization_page(reset=False):
        """从消息进入组织架构页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_organization()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()

    @staticmethod
    def enter_workbench_manager_page(reset=False):
        """从消息进入工作台管理页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            workbench.wait_for_page_load()
            workbench.click_workbench_manage()
        wmp = WorkBenchManagerPage()
        wmp.wait_for_page_load()

    @staticmethod
    def enter_voice_announcement_page(reset=False):
        """从消息进入语音通知页面"""
        # 登录进入消息页面
        LoginPreconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 从消息进入组织架构页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        if workbench.is_on_welcome_page():
            workbench.click_now_create_team()
        else:
            a=0
            while a<10:
                workbench.wait_for_page_load()
                workbench.click_voice_notice()
                time.sleep(5)
                if workbench.is_text_present("认证失败"):
                    current_mobile().back()
                    a+=1
                else:
                    break
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
