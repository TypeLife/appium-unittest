__all__ = [
    'BuildGroupChatPage',
    'MyQRCodePage',
    'ScanPage',
    'SelectContactPage',
]

# 创建群聊
from .BuildGroupChat import BuildGroupChatPage
# 我的二维码
from .MyQRCode import MyQRCodePage
# 扫一扫
from .Scan import ScanPage
# 选择联系人
from .SelectContact import SelectContactPage
