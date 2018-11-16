__all__ = [
    "GuidePage",
    "PermissionListPage",
    "OneKeyLoginPage",
    "MessagePage",
    "SmsLoginPage",
    "MePage",
    "SettingPage",
    "AgreementDetailPage",
    "AgreementPage",
    "MeSetMultiLanguagePage",
    "SearchPage",
]
from .Agreement import AgreementPage
from .AgreementDetail import AgreementDetailPage
from .Guide import GuidePage
from .Me import MePage
from .MeSetMultiLanguage import MeSetMultiLanguagePage
from .Message import MessagePage
from .OneKeyLogin import OneKeyLoginPage
from .PermissionList import PermissionListPage
from .Search import SearchPage
from .Setting import SettingPage
from .SmsLogin import SmsLoginPage
