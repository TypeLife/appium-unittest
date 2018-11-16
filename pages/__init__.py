__all__ = [
    "MePage",
    "MeSetMultiLanguagePage",
    "SearchPage",
    "SettingPage",
    "ContactDetailsPage",
    "NewContactPage",
    "GuidePage",
    "PermissionListPage",
    "AgreementDetailPage",
    "AgreementPage",
    "OneKeyLoginPage",
    'SmsLoginPage',
    'MessagePage',
]

from .Me import MePage
from .MeSetMultiLanguage import MeSetMultiLanguagePage
from .Search import SearchPage
from .Setting import SettingPage
from .contacts import ContactDetailsPage
from .contacts import NewContactPage
from .guide import GuidePage
from .guide import PermissionListPage
from .login import AgreementDetailPage
from .login import AgreementPage
from .login import OneKeyLoginPage
from .login import SmsLoginPage
from .message import MessagePage
