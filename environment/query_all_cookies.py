# -*- coding: utf-8 -*-
import json
from typing import Dict
from DrissionPage._base.chromium import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
import re
from utils import logger

__author__ = 'lcy'


"""
from DrissionPage import ChromiumOptions
co = ChromiumOptions()
co.use_system_user_path()
co.headless(True)
co.save('environment/config1.ini')  # 把这个配置记录到 ini 文件

from DrissionPage.common import configs_to_here
configs_to_here()  # 项目文件夹会多出一个'dp_configs.ini'文件,页面对象初始化时会优先读取这个文件
"""


def process_domain(domain: str) -> str:
    parts = domain.split('.')
    if domain.endswith('.com.cn') and len(parts) >= 3:
        return '.' + '.'.join(parts[-3:])
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain):
        return domain
    if len(parts) >= 2:
        return '.' + '.'.join(parts[-2:])


def tab_cookies_to_dict(brower_cookies_list):
    for tab_cookies in brower_cookies_list:
        domain = process_domain(tab_cookies['domain'])
        if domain not in _all_cookies_dicts:
            _all_cookies_dicts[domain] = {}
        _all_cookies_dicts[domain].update({tab_cookies['name']: tab_cookies['value']})


def start_chromium_browser():
    logger.info('start chromium page')
    global page
    page = get_chromium_page()
    brower_cookies_as_json = page.cookies(all_domains=True, all_info=False).as_json()
    brower_cookies_list = json.loads(brower_cookies_as_json)
    tab_cookies_to_dict(brower_cookies_list)
    # page.disconnect()


def get_chromium_page():
    co = ChromiumOptions()
    co.set_local_port(9222)
    co.use_system_user_path()
    return ChromiumPage(addr_or_opts=co)


def get_chromium_page_single():
    return page


def get_cookies_from_chromium(cookies_key: str) -> Dict[str, str]:
    return _all_cookies_dicts.get(cookies_key)


def refresh_cookies():
    start_chromium_browser()


_all_cookies_dicts = {}
# page = ChromiumPage()
start_chromium_browser()


# print(_all_cookies_dicts)


"""
调式模式要求一个端口绑定一个用户文件目录，
反之，默认系统用户目录不能绑定多个浏览器（默认双击打开浏览器时，再启动dp指定系统用户目录会报错）
"""

