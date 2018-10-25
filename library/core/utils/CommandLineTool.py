import getopt

from . import ConfigManager


def parse_and_store_command_line_params(args):
    server_opt_name = ['serverUrl']
    general_capabilities = [
        "automationName",
        "platformName",
        "platformVersion",
        "deviceName",
        "app",
        "browserName",
        "newCommandTimeout",
        "language",
        "locale",
        "udid",
        "orientation",
        "autoWebview",
        "noReset",
        "fullReset",
        "eventTimings",
        "enablePerformanceLogging",
        "printPageSourceOnFindFailure",
    ]
    android_only = [
        "appActivity",
        "appPackage",
        "appWaitActivity",
        "appWaitPackage",
        "appWaitDuration",
        "deviceReadyTimeout",
        "androidCoverage",
        "androidCoverageEndIntent",
        "androidDeviceReadyTimeout",
        "androidInstallTimeout",
        "androidInstallPath",
        "adbPort",
        "systemPort",
        "remoteAdbHost",
        "androidDeviceSocket",
        "avd",
        "avdLaunchTimeout",
        "avdReadyTimeout",
        "avdArgs",
        "useKeystore",
        "keystorePath",
        "keystorePassword",
        "keyAlias",
        "keyPassword",
        "chromedriverExecutable",
        "chromedriverExecutableDir",
        "chromedriverChromeMappingFile",
        "chromedriverUseSystemExecutable",
        "autoWebviewTimeout",
        "intentAction",
        "intentCategory",
        "intentFlags",
        "optionalIntentArguments",
        "dontStopAppOnReset",
        "unicodeKeyboard",
        "resetKeyboard",
        "noSign",
        "ignoreUnimportantViews",
        "disableAndroidWatchers",
        "chromeOptions",
        "recreateChromeDriverSessions",
        "nativeWebScreenshot",
        "androidScreenshotPath",
        "autoGrantPermissions",
        "networkSpeed",
        "gpsEnabled",
        "isHeadless",
        "uiautomator2ServerLaunchTimeout",
        "uiautomator2ServerInstallTimeout",
        "otherApps",
    ]
    ios_only = [
        "calendarFormat",
        "bundleId",
        "udid",
        "launchTimeout",
        "locationServicesEnabled",
        "locationServicesAuthorized",
        "autoAcceptAlerts",
        "autoDismissAlerts",
        "nativeInstrumentsLib",
        "nativeWebTap",
        "safariInitialUrl",
        "safariAllowPopups",
        "safariIgnoreFraudWarning",
        "safariOpenLinksInBackground",
        "keepKeyChains",
        "localizableStringsDir",
        "processArguments",
        "interKeyDelay",
        "showIOSLog",
        "sendKeyStrategy",
        "screenshotWaitTimeout",
        "waitForAppScript",
        "webviewConnectRetries",
        "appName",
        "customSSLCert",
        "webkitResponseTimeout",
        "remoteDebugProxy",
    ]
    # 无参数使用默认参数
    if not args:
        # config.GlobalConfig.set_desired_caps(config.default_desired_capability)
        return

    support_params = [capability + '=' for capability in general_capabilities]
    support_params.extend([capability + '=' for capability in android_only])
    support_params.extend([capability + '=' for capability in ios_only])
    support_params.extend([opt_name + '=' for opt_name in server_opt_name])

    caps = {}
    try:
        opts, args = getopt.getopt(args, '', support_params)
    except getopt.GetoptError as err:
        raise Exception(err.msg)
    for (opt, value) in opts:
        opt = opt.replace('--', '')
        if opt in general_capabilities or opt in android_only or opt in ios_only:
            if opt in ['newCommandTimeout']:
                value = int(value)
            elif opt in ['noReset']:
                value = True if value.lower() == 'true' else False
            caps[opt] = value
        elif opt in server_opt_name:
            ConfigManager.set_server_url(value)

    ConfigManager.set_desired_caps(caps)

    if __name__ == '__main__':
        print(ConfigManager.get_desired_caps())
        print(ConfigManager.get_server_url())


if __name__ == '__main__':
    parse_and_store_command_line_params(
        ['--app="/abs/path/to/my.apk"', '--serverUrl="http://127.0.0.1:4723/wd/hub"'])
