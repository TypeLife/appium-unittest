import argparse
import os
import re
import sys
import time
from collections import OrderedDict
from lxml import etree
import uuid
from appium.webdriver.common.mobileby import MobileBy

import settings
from library.core.utils.applicationcache import MOBILE_DRIVER_CACHE, current_driver
from settings.available_devices import AVAILABLE_DEVICES

_ENCODING = sys.stdin.encoding if sys.stdin.encoding else "UTF-8"

DISTINCT_PATH = os.path.join(settings.PROJECT_PATH, 'pages')
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
PAGE_OBJECT_TEMPLATE = os.path.join(TEMPLATE_PATH, 'pageobject.pyt')


def get_template(path):
    with open(path, 'r+', encoding='UTF-8') as t:
        content = t.read()
        return content


def build_page_object(page_name=None, page_description=None, activity=None, locator=None):
    temp = get_template(PAGE_OBJECT_TEMPLATE)
    file_path = ''
    source_path = ''
    try_times = 0
    while not page_name:
        sys.stdout.write('请输入页面类名：')
        sys.stdout.flush()
        page_name = sys.stdin.readline().strip()
        file_path = os.path.join(DISTINCT_PATH, page_name + '.py')
        source_path = os.path.join(DISTINCT_PATH, page_name + '.xml')
        if os.path.isfile(file_path):
            page_name = None
        try_times += 1
        if try_times > 3:
            raise Exception('尝试超过3次，请确认页面名不会重复再执行该任务!')
    if not page_description:
        sys.stdout.write('请输入页面描述：')
        sys.stdout.flush()
        page_description = sys.stdin.readline().strip()

    # output = temp % {
    #     'PageName': page_name,
    #     'PageDescription': page_description,
    #     'Activity': activity,
    #     'Locator': locator
    # }
    out = re.sub(r"(%\(PageName\)s)", page_name, temp)
    out = re.sub(r'(%\(PageDescription\)s)', page_description, out)
    out = re.sub(r'(%\(Activity\)s)', activity, out)
    out = out.replace("%(Locator)s", locator)
    # out = re.sub(r'(%\(Locator\)s)', locator, out)
    with open(file_path, 'w+', encoding='UTF-8') as f:
        f.write(out)
        sys.stdout.write('Page object created on: ' + file_path + '\n')
        sys.stdout.flush()

    with open(source_path, 'w+', encoding='UTF-8') as f:
        f.write(current_driver().page_source)
        sys.stdout.write('Page source created on: ' + source_path + '\n')
        sys.stdout.flush()


def generate_page_object():
    driver = current_driver()
    do = True
    while do:
        sys.stdout.write('按回车键开始录制：')
        sys.stdout.flush()
        sys.stdin.readline().strip().upper()
        activity = driver.current_activity
        page_source = driver.page_source
        tree = etree.fromstring(page_source.encode())
        elements = []

        def parse(node):
            for e in node.iter():
                resource_id = e.get('resource-id')
                xpath = node.getroottree().getpath(e)
                text = e.get('text')
                if isinstance(text, str):
                    text = text.replace('\n', '')
                key = text if text else resource_id
                if key in dict(elements):
                    key = key + uuid.uuid4().__str__()
                if key:
                    if resource_id:
                        elements.append((key, (MobileBy.ID, resource_id)))
                    else:
                        elements.append((key, (MobileBy.XPATH, xpath)))

        parse(tree)
        locators = re.sub(r"('[^)]+\),?)", r'\1\n', dict(OrderedDict(elements)).__repr__())
        locators = re.sub(r"(\('id')", r'(MobileBy.ID', locators)
        build_page_object(activity=activity, locator=locators)
        sys.stdout.write('\n结束录制?(Y/N)：')
        sys.stdout.flush()
        feedback = sys.stdin.readline().strip().upper()
        if feedback == 'Y':
            do = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', '-r', type=bool)
    args = parser.parse_args()

    sys.stdout.write("当前使用的手机为：" + MOBILE_DRIVER_CACHE.current.alis + '\n')
    sys.stdout.flush()
    devices = '\n\t'.join(AVAILABLE_DEVICES.keys())
    sys.stdout.write("可用手机：\n\t" + devices + '\n')
    sys.stdout.flush()
    sys.stdout.write('是否切换手机(Y/N):')
    sys.stdout.flush()
    resp = sys.stdin.readline().strip().upper()
    if resp == 'Y':
        sys.stdout.write('输入要切换的手机:')
        sys.stdout.flush()
        target = sys.stdin.readline().strip()
        MOBILE_DRIVER_CACHE.switch(target)
    time.sleep(.5)
    sys.stdout.write('开始连接手机并启动应用....\n')
    sys.stdout.flush()
    MOBILE_DRIVER_CACHE.current._desired_caps['newCommandTimeout'] = 600
    if args.reset:
        MOBILE_DRIVER_CACHE.current.turn_on_reset()
    MOBILE_DRIVER_CACHE.current.connect_mobile()
    generate_page_object()
