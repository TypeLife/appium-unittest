__all__ = [
    'SearchPage',
    'SettingPage',
    'ContactDetailsPage',
    'NewContactPage',
    'GuidePage',
    'PermissionListPage',
    'AgreementDetailPage',
    'AgreementPage',
    'OneKeyLoginPage',
    'SmsLoginPage',
    'MePage',
    'MeSetCallPage',
    'MeSetContactsManagerPage',
    'MeSetDialPage',
    'MeSetDialWayPage',
    'MeSetFontSizePage',
    'MeSetFuHaoPage',
    'MeSetImprovePlanPage',
    'MeSetMultiLanguagePage',
    'SetMessageNoticePage',
    'MeSetUpPage',
    'MeSmsSetPage',
    'MessagePage',
]

from pages.me.Setting import SettingPage
from .Search import SearchPage
from .contacts import ContactDetailsPage
from .contacts import NewContactPage
from .guide import GuidePage
from .guide import PermissionListPage
from .login import AgreementDetailPage
from .login import AgreementPage
from .login import OneKeyLoginPage
from .login import SmsLoginPage
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
from .me import MeSmsSetPage
from .me import SetMessageNoticePage
from .message import MessagePage
