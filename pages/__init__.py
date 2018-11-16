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
from pages.guide.Guide import GuidePage
from pages.guide.PermissionList import PermissionListPage
from pages.login.Agreement import AgreementPage
from pages.login.AgreementDetail import AgreementDetailPage
from pages.login.OneKeyLogin import OneKeyLoginPage
from pages.login.SmsLogin import SmsLoginPage
from pages.message.Message import MessagePage
from .Me import MePage
from .MeSetMultiLanguage import MeSetMultiLanguagePage
from .Search import SearchPage
from .Setting import SettingPage
