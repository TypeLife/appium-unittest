from library.core.common.supportedmodel import SupportedModel
from mobileimplements import *

MOBILE_DRIVER_CREATORS = {
    SupportedModel.MI6['Model']: lambda kw: MI6(**kw),
    SupportedModel.MEIZU_PRO_6_PLUS['Model']: lambda kw: MXPro6Plus(**kw)
}
