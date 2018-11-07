from library.core.common.simcardtype import CardType
from library.core.mobile.mobiledriver import MobileDriver


class MXPro6Plus(MobileDriver):
    """魅族Pro 6 Plus"""

    def supported_card_types(self):
        return [
            CardType.CHINA_MOBILE,
            CardType.CHINA_UNION,
        ]

    def total_card_slot(self):
        return 2
