# 可用手机以及启动配置
from library.core.common.simcardtype import CardType
from library.core.common.supportedmodel import SupportedModel

# 测试APP信息
TARGET_APP = dict(
    # DOWNLOAD_URL="https://www.pgyer.com/apiv2/app/install?_api_key=298b363e3288c07f2683b96ca9bc5ab6&appKey=andfetiondev&buildPassword=qwer!234",
    DOWNLOAD_URL="http://dlrcs.fetion-portal.com/mobile/RCS_V6.2.8.0129_20190130.apk",
    APP_PACKAGE="com.chinasofti.rcs",
    APP_ACTIVITY="com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
    INSTALL_BEFORE_RUN=False
)

# ======================= 移动CI环境手机配置 =======================
AVAILABLE_DEVICES = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://221.176.34.113:5000/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "8DF6R17526001515",
            "udid": "8DF6R17526001515",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775970982'
            },
        ]
    },
}

# ======================= 本地CI环境手机配置 =======================
AVAILABLE_DEVICES_DEV = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.MEIZU_PRO_6_PLUS,
        "SERVER_URL": 'http://192.168.200.127:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0.1",
            "deviceName": "M960BDQN229DK",
            "udid": "M960BDQN229DK",
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
    'M960BDQN229CH-BACK': {
        "MODEL": SupportedModel.MEIZU_PRO_6_PLUS,
        "SERVER_URL": 'http://127.0.0.1:5000/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "95AQACPMGJP5L",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '14775970982'
            },
            None
        ]
    },
    'M960BDQN229CH-bak': {
        "MODEL": SupportedModel.MEIZU_PRO_6_PLUS,
        "SERVER_URL": 'http://192.168.200.112:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "M960BDQN229CH",
            "udid": "M960BDQN229CH",
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
    'M960BDQN229CH_me': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://192.168.1.103:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
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
        ]
    },
    'single_mobile': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://192.168.1.104:4724/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
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
        ]
    },
    'single_telecom': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
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
        ]
    },
    'single_union': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
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
        ]
    },
    'double_mobile': {
        "MODEL": SupportedModel.RED_MI_NOTE_4X,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "VCO7IFTKKZZ5FI9T",
            "udid": "VCO7IFTKKZZ5FI9T",
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
                'CARD_NUMBER': '19876283465'
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
            "udid": "VCO7IFTKKZZ5FI9T",
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
            "udid": "VCO7IFTKKZZ5FI9T",
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

# ======================= 个人本机执行环境手机配置 =======================
DEVICES_CONFIG_XIN = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://local.appium:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.0.0",
            "deviceName": "LKX0218814000312",
            "udid": "LKX0218814000312",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
            # "appPackage": "com.meizu.flyme.launcher",
            # "appActivity": ".Launcher",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '19876283465'
            },
        ]
    },
    # 'M960BDQN229CH': {
    #     "MODEL": SupportedModel.HUAWEI_P20,
    #     "SERVER_URL": 'http://221.176.34.113:5000/wd/hub',
    #     "DEFAULT_CAPABILITY": {
    #         "platformName": "Android",
    #         "platformVersion": "6.0",
    #         "deviceName": "8DF6R17526001515",
    #         "udid": "8DF6R17526001515",
    #         "automationName": "UiAutomator2",
    #         "newCommandTimeout": 600,
    #         "appPackage": "com.chinasofti.rcs",
    #         # "appPackage": "com.huawei.android.launcher",
    #         "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
    #         # "appActivity": ".unihome.UniHomeLauncher",
    #     },
    #     'CARDS': [
    #         {
    #             'TYPE': CardType.CHINA_MOBILE,
    #             'CARD_NUMBER': '14775970982'
    #         },
    #     ]
    # },
    # '红米Note4X': {
    #     "MODEL": SupportedModel.RED_MI_NOTE_4X,
    #     "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
    #     "DEFAULT_CAPABILITY": {
    #         "platformName": "Android",
    #         "platformVersion": "6.0",
    #         "deviceName": "VCO7IFTKKZZ5FI9T",
    #         "udid": "VCO7IFTKKZZ5FI9T",
    #         "automationName": "UiAutomator2",
    #         "newCommandTimeout": 600,
    #
    #         "appPackage": "com.chinasofti.rcs",
    #         "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
    #     },
    #     'CARDS': [
    #         {
    #             'TYPE': CardType.CHINA_MOBILE,
    #             'CARD_NUMBER': '14775290489'
    #         },
    #     ]
    # }
}

DEVICES_CONFIG_YYX = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "JUBNU18816112025",
            "udid": "JUBNU18816112025",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '13537795364'
            },
        ]
    },
}

DEVICES_P20 = {
    'M960BDQN229CH': {
        "MODEL": SupportedModel.HUAWEI_P20,
        "SERVER_URL": 'http://127.0.0.1:4723/wd/hub',
        "DEFAULT_CAPABILITY": {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "CLB7N18904002073",
            "udid": "CLB7N18904002073",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 600,
            "appPackage": "com.chinasofti.rcs",
            "appActivity": "com.cmcc.cmrcs.android.ui.activities.WelcomeActivity",
        },
        'CARDS': [
            {
                'TYPE': CardType.CHINA_MOBILE,
                'CARD_NUMBER': '15918730974'
            },
        ]
    },
}
