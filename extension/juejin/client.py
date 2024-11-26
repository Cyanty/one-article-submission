from environment import get_cookies_from_chromium
from DrissionPage._functions.by import By
from base import AbstractClient, AbstractBrowserClient


class JueJinClient(AbstractClient, AbstractBrowserClient):

    def __init__(self):
        self._create_json_data = None
        self._pre_json_data = None
        self._json_data = None
        self._cookies = None
        self._host = None

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def create_publish_url(self) -> str:
        return 'https://api.juejin.cn/content_api/v1/article_draft/create'

    @property
    def pre_publish_url(self) -> str:
        return 'https://api.juejin.cn/content_api/v1/article_draft/update'

    @property
    def publish_url(self):
        return 'https://api.juejin.cn/content_api/v1/article/publish'

    @property
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self, value: str):
        self._cookies = get_cookies_from_chromium(value)

    @property
    def headers(self):
        return {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://juejin.cn',
            'priority': 'u=1, i',
            'referer': 'https://juejin.cn/',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            # 'x-secsdk-csrf-token': '000100000001a935c7084c5451cccfdcf9be535cbed655a1363fbe29ab48e99ec2f8ce8a3d25180500f4c9397353',
        }

    @property
    def create_json_data(self):
        return self._create_json_data

    @create_json_data.setter
    def create_json_data(self, value: dict):
        self._create_json_data = {
            'category_id': '0',
            'tag_ids': [],
            'link_url': '',
            'cover_image': '',
            'title': value.get('title'),
            'brief_content': '',
            'edit_type': 10,
            'html_content': 'deprecated',
            'mark_content': '',
            'theme_ids': [],
            'pics': [],
        }

    @property
    def pre_json_data(self):
        return self._pre_json_data

    @pre_json_data.setter
    def pre_json_data(self, value: dict):
        self._pre_json_data = {
            'id': value.get('id'),
            'category_id': '6809637769959178254',  # 分类：后端
            'tag_ids': [
                '6809641131131797511',  # 标签：大数据
            ],
            'link_url': '',
            'cover_image': '',
            'is_gfw': 0,
            'title': value.get('title'),
            'brief_content': '',
            'is_english': 0,
            'is_original': 1,
            'edit_type': 10,
            'html_content': 'deprecated',
            'mark_content': value.get('content'),
            'theme_ids': [],
            'pics': [
                {
                    'pic_url': 'https://p0-xtjj-private.juejin.cn/tos-cn-i-73owjymdk6/445b8abf25634e3eb40597273f84c8f8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZKa5ZKa5ZKa:q75.awebp?policy=eyJ2bSI6MywidWlkIjoiNDE4OTYxNjU3MDkwNDIxNSJ9&rk3s=f64ab15b&x-orig-authkey=f32326d3454f2ac7e96d3d06cdbb035152127018&x-orig-expires=1731477584&x-orig-sign=qxp1sKylNw%2BrSJ%2BT%2Bx4T4%2BZAR04%3D',
                    'pic_uri': 'tos-cn-i-73owjymdk6/445b8abf25634e3eb40597273f84c8f8',
                },
            ],
        }

    @property
    def json_data(self):
        return self._json_data

    @json_data.setter
    def json_data(self, value: dict):
        self._json_data = {
            'draft_id': value.get('id'),
            'sync_to_org': False,
            'column_ids': [],
            'theme_ids': [],
            # 'encrypted_word_count': value.get('encrypted_word_count'),
            # 'origin_word_count': value.get('origin_word_count'),
        }

    @property
    def params(self):
        return {
            'aid': '2608',
            'uuid': '7298657419406935589',
        }

    @property
    def loc_title(self):
        return None

    @property
    def loc_content(self):
        return None

    @property
    def loc_publish_button(self):
        return By.XPATH, '//button[contains(text(), "发布")]'  # 发布按钮

    @property
    def loc_confirm_publish_button(self):
        return By.XPATH, '//button[contains(text(), "确定并发布")]'  # 确认并发布按钮

    @property
    def title_name(self):
        return None

    @property
    def md_content(self):
        return None




