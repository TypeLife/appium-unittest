__all__ = [
    'BuildGroupChatPage',
    'MyQRCodePage',
    'ScanPage',
    'Scan1Page',
    'SelectContactPage',
]

# 创建群聊
from .BuildGroupChat import BuildGroupChatPage
# 我的二维码
from .MyQRCode import MyQRCodePage
# 扫一扫
from .Scan import ScanPage
# 扫一扫（网络异常）
from .Scan1 import Scan1Page
# 选择联系人
from .SelectContact import SelectContactPage
