from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MyQRCodePage(BasePage):
    """我的二维码"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.QRCodeActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        '我的二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/text_title'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        '加载中': (MobileBy.ID, 'com.chinasofti.rcs:id/img_wait'),
        'com.chinasofti.rcs:id/qr_code_info_view': (MobileBy.ID, 'com.chinasofti.rcs:id/qr_code_info_view'),
        'com.chinasofti.rcs:id/rl_qr_info': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_qr_info'),
        'com.chinasofti.rcs:id/profile_info': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_info'),
        '二维码中的名称': (MobileBy.ID, 'com.chinasofti.rcs:id/twodimension_name_text'),
        '二维码中的头像': (
            MobileBy.ID, 'com.chinasofti.rcs:id/twodimensioncode_myprofile_icon'),
        '二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/my_twodimensionCode'),
        '扫描二维码，添加和飞信': (MobileBy.ID, 'com.chinasofti.rcs:id/textView2'),
        '分享二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/qecode_share_btn'),
        '保存二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/qecode_save_btn'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
    }

    @TestLogger.log('等待加载完毕')
    def wait_for_loading_animation_end(self):
        self.mobile.wait_until(
            condition=lambda d: self.get_element(self.__locators['分享二维码']),
            timeout=60
        )

    def decode_qr_code(self):
        from pyzbar import pyzbar
        import io
        from PIL import Image

        screen_shot = self.mobile.get_element(self.__locators['二维码']).screenshot_as_png
        fp = io.BytesIO(screen_shot)
        qr = pyzbar.decode(Image.open(fp))
        if qr:
            return qr[0].data.decode()
        raise AssertionError('不是有效的二维码')

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击转发（分享）二维码')
    def click_forward_qr_code(self):
        self.click_element(self.__locators["分享二维码"], default_timeout=15)

    @TestLogger.log('点击下载（保存）二维码')
    def click_save_qr_code(self):
        self.click_element(self.__locators['保存二维码'], default_timeout=15)

    @TestLogger.log()
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__locators[text])
