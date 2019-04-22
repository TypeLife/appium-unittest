__all__ = [
    'ContactDetailsPage',
    'ContactListSearchPage',
    'ContactsPage',
    'CreateContactPage',
    'GroupListPage',
    'GroupListSearchPage',
    'GuidePage',
    'PermissionListPage',
    'AgreementDetailPage',
    'AgreementPage',
    'OneKeyLoginPage',
    'SmsLoginPage',
    'MePage',
    'MeCollectionPage',
    'MeSetCallPage',
    'MeSetContactsManagerPage',
    'MeSetDialPage',
    'MeSetDialWayPage',
    'MeSetFontSizePage',
    'MeSetFuHaoPage',
    'MeSetImprovePlanPage',
    'MeSetMultiLanguagePage',
    'MessageNoticeSettingPage',
    'SettingPage',
    'MeSetUpPage',
    'SmsSettingPage',
    'ChatWindowPage',
    'EmailAssistantPage',
    'EmailDetailPage',
    'EmailListPage',
    'MessagePage',
    'GroupChatSetPage',
    'GroupChatSetManagerPage',
    'GroupChatSetModifyMyCardPage',
    'GroupChatSetSeeMembersPage',
    'GroupChatSetSeeQRCodePage',
    'GroupNamePage',
    'SelectContactsPage',
    'SelectOneGroupPage',
    'SelectLocalContactsPage',
    'CreateGroupNamePage',
    'GroupChatPage',
    'SingleChatPage',
    "ChatAudioPage",
    "ChatGIFPage",
    "ChatMorePage",
    "ChatPhotoPage",
    "ChatPicPage",
    "ChatPicEditPage",
    "ChatPicPreviewPage",
    "ChatSelectFilePage",
    "ChatSelectLocalFilePage",
    "ChatProfilePage",
    "ChatLocationPage",
    "BuildGroupChatPage",
    "MyQRCodePage",
    "ScanPage",
    "Scan1Page",
    "SelectContactPage",
    'GlobalSearchContactPage',
    'GlobalSearchGroupPage',
    'GlobalSearchMessagePage',
    'MessageSearchPage',
    'SearchPage',
    'GroupChatSetFindChatContentPage',
    'LabelGroupingPage',
    'LableGroupDetailPage',
    'LabelGroupingChatPage',
    'SelectHeContactsPage',
    'SelectHeContactsDetailPage',
    'ChatFilePage',
    'FindChatRecordPage',
    'SingleChatSetPage',
    'PicVideoPage',
    'WorkbenchPage',
    'CreateTeamPage',
    'CallPage',
    'CalllogBannerPage',
    'CallTypeSelectPage',
    'ContactSecltorPage',
    'GrantPemissionsPage',
    'CallContactDetailPage',
    'NewOrEditContactPage',
    'MultiPartyVideoPage',
]

from .ChatFile import ChatFilePage
from .SingleChatSet import SingleChatSetPage
from .FindChatRecord import FindChatRecordPage
from .CreateGroupName import CreateGroupNamePage
from .GroupChat import GroupChatPage
from .LabelGrouping import LabelGroupingPage
from .LabelGroupingChat import LabelGroupingChatPage
from .LableGroupDetail import LableGroupDetailPage
from .SelectContacts import SelectContactsPage
from .SelectLocalContacts import SelectLocalContactsPage
from .SelectOneGroup import SelectOneGroupPage
from .SelectHeContacts import SelectHeContactsPage
from .SelectHeContactsDetail import SelectHeContactsDetailPage
from .SingleChat import SingleChatPage
from .chat import ChatAudioPage
from .chat import ChatGIFPage
from .chat import ChatLocationPage
from .chat import ChatMorePage
from .chat import ChatPhotoPage
from .chat import ChatPicEditPage
from .chat import ChatPicPage
from .chat import ChatPicPreviewPage
from .chat import ChatProfilePage
from .chat import ChatSelectFilePage
from .chat import ChatSelectLocalFilePage
from .chat import PicVideoPage
from .contacts import ContactDetailsPage
from .contacts import ContactListSearchPage
from .contacts import ContactsPage
from .contacts import CreateContactPage
from .contacts import GroupListPage
from .contacts import GroupListSearchPage
from .groupset import GroupChatSetFindChatContentPage
from .groupset import GroupChatSetManagerPage
from .groupset import GroupChatSetModifyMyCardPage
from .groupset import GroupChatSetPage
from .groupset import GroupChatSetSeeMembersPage
from .groupset import GroupChatSetSeeQRCodePage
from .groupset import GroupNamePage
from .guide import GuidePage
from .guide import PermissionListPage
from .login import AgreementDetailPage
from .login import AgreementPage
from .login import OneKeyLoginPage
from .login import SmsLoginPage
from .me import MeCollectionPage
from .me import MePage
from .me import MeSetCallPage
from .me import MeSetContactsManagerPage
from .me import MeSetDialPage
from .me import MeSetDialWayPage
from .me import MeSetFontSizePage
from .me import MeSetFuHaoPage
from .me import MeSetImprovePlanPage
from .me import MeSetMultiLanguagePage
from .me import MeSetUpPage
from .me import MessageNoticeSettingPage
from .me import SettingPage
from .me import SmsSettingPage
from .message import ChatWindowPage
from .message import EmailAssistantPage
from .message import EmailDetailPage
from .message import EmailListPage
from .message import MessagePage
from .others import BuildGroupChatPage
from .others import MyQRCodePage
from .others import Scan1Page
from .others import ScanPage
from .others import SelectContactPage
from .search import GlobalSearchContactPage
from .search import GlobalSearchGroupPage
from .search import GlobalSearchMessagePage
from .search import MessageSearchPage
from .search import SearchPage
from .workbench import WorkbenchPage
from .workbench.create_team import CreateTeamPage
from .call import CallPage
from .call import CalllogBannerPage
from .call import CallTypeSelectPage
from .call import ContactSecltorPage
from .call import GrantPemissionsPage
from .call import CallContactDetailPage
from .call import NewOrEditContactPage
from .call import MultiPartyVideoPage
