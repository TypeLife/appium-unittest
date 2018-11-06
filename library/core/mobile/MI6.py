from library.core.common.simcardtype import CardType
from library.core.mobile.mobiledriver import MobileDriver


class MI6(MobileDriver):
    """小米6"""

    def supported_card_types(self):
        return [
            CardType.CHINA_MOBILE,
            CardType.CHINA_UNION,
            CardType.CHINA_TELECOM,
        ]

    def total_card_slot(self):
        return 2
