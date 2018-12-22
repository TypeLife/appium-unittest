# 可用手机以及启动配置
from library.core.common.simcardtype import CardType
from library.core.common.supportedmodel import SupportedModel

AVAILABLE_DEVICES = {
    'MI5X': {
        "MODEL": SupportedModel.MI6,
        "SERVER_URL": 'http://192.168.200.177:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "7.1",
            "deviceName": "aa8dd3c60904",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_UNION,
                'CARD_NUMBER': '17611681917'
            },
        ]
    },
    'M960BDQN229CH': {
        "MODEL": SupportedModel.MEIZU_PRO_6_PLUS,
        "SERVER_URL": 'http://192.168.200.177:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "M960BDQN229CH",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19876283465'
            },
        ]
    },
    'M960BDQN229CH-bak': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://192.168.200.112:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775290489'
            },
            None
        ]
    },
    'single_mobile': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://192.168.200.112:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775290489'
            },
            None
        ]
    },
    'single_telecom': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_TELECOM,
                'CARD_NUMBER': '15338821645'
            },
            None
        ]
    },
    'single_union': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_UNION,
                'CARD_NUMBER': '18681151872'
            },
            None
        ]
    },
    'double_mobile': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775290489'
            },
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '13510772034'
            }
        ]
    },
    'mobile_and_union': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775290489'
            },
            {
                'TYPE': CardType.CHINA_UNION,
                'CARD_NUMBER': '18681151872'
            }
        ]
    },
    'others_double': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_TELECOM,
                'CARD_NUMBER': '15338821645'
            },
            {
                'TYPE': CardType.CHINA_UNION,
                'CARD_NUMBER': '18681151872'
            }
        ]
    }
}
