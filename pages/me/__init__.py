__all__ = [
    'MePage',
    'MeSetCallPage',
    'MeSetContactsManagerPage',
    'MeSetDialPage',
    'MeSetDialWayPage',
    'MeSetFontSizePage',
    'MeSetFuHaoPage',
    'MeSetImprovePlanPage',
    'MeSetMultiLanguagePage',
    'MessageNoticeSettingPage',
    'MeSetUpPage',
    'SmsSettingPage',
    'SettingPage',
    'MeCollectionPage',
]

from .MeCollection import MeCollectionPage
from .Me import MePage
from .MeSetCall import MeSetCallPage
from .MeSetContactsManager import MeSetContactsManagerPage
from .MeSetDial import MeSetDialPage
from .MeSetDialWay import MeSetDialWayPage
from .MeSetFontSize import MeSetFontSizePage
from .MeSetFuHao import MeSetFuHaoPage
from .MeSetImprovePlan import MeSetImprovePlanPage
from .MeSetMultiLanguage import MeSetMultiLanguagePage
from .MeSetUp import MeSetUpPage
from .MessageNoticeSetting import MessageNoticeSettingPage
from .Setting import SettingPage
from .SmsSetting import SmsSettingPage
