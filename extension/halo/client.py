from base import AbstractClient
from config import halo_publish_token
from environment import get_cookies_from_chromium


class HaloClient(AbstractClient):
    """
        _host: str = None,  主机IP或域名
        _attachment_publish_url: str = None,  附件API
        _pre_publish_url: str = None,  创建并发布API
        _publish_url: str = None,  发布API
        _cookies: Dict = None,  cookies
        _attachment_headers: Dict = None,  附件请求头
        _headers: Dict = None,  发布请求头
        _json_data: Dict = None,  发布请求data
    """

    def __init__(self):
        self._host = None
        self._cookies = None
        self._publish_url = None
        self._json_data = None

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def attachment_publish_url(self) -> str:
        return 'http://' + self._host + '/apis/api.console.halo.run/v1alpha1/attachments/upload'

    @property
    def pre_publish_url(self) -> str:
        return 'http://' + self._host + '/apis/api.console.halo.run/v1alpha1/posts'

    @property
    def publish_url(self):
        return self._publish_url

    @publish_url.setter
    def publish_url(self, uuid: str):
        self._publish_url = 'http://' + self._host + '/apis/api.console.halo.run/v1alpha1/posts/' + uuid

    @property
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self, value: str):
        self._cookies = get_cookies_from_chromium(value)

    @property
    def attachment_headers(self):
        return {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Authorization': 'Bearer ' + halo_publish_token,
            # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary26w5KbBsjd2c3EwK',
            'Origin': 'http://' + self.host,
            'Referer': 'http://' + self.host + '/console/attachments',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }

    @property
    def headers(self):
        return {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Authorization': 'Bearer ' + halo_publish_token,
            'Content-Type': 'application/json',
            'Origin': 'http://' + self.host,
            'Referer': 'http://' + self.host + '/console/posts/editor',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

    @property
    def json_data(self):
        return self._json_data

    @json_data.setter
    def json_data(self, value: dict):
        self._json_data = {
            'post': {
                'spec': {
                    'title': value.get('title'),
                    'slug': value.get('slug'),  # 生成文章的固定链接，默认为文章标题的拼音用-分隔
                    'template': '',
                    'cover': '',
                    'deleted': False,
                    'publish': True,  # 是否发布，可以设置为True直接发布，也可以设置为False，在调用publish_url发布
                    'pinned': False,  # 是否置顶
                    'allowComment': True,  # 是否允许评论
                    'visible': 'PUBLIC',  # 可见性：公开
                    'priority': 0,
                    "publishTime": value.get('publish_time'),  # 发布时间，格式 -> "2024-10-30T09:39:10.763909062Z",
                    'excerpt': {
                        'autoGenerate': True,
                        'raw': '',
                    },
                    # 'categories': [  # 分类
                    #     '76514a40-6ef1-4ed9-b58a-e26945bde3ca',
                    # ],
                    # 'tags': [  # 标签
                    #     'c33ceabb-d8f1-4711-8991-bb8f5c92ad7c',
                    # ],
                    'htmlMetas': [],
                    # 'owner': 'lcyrus',
                },
                'apiVersion': 'content.halo.run/v1alpha1',
                'kind': 'Post',
                'metadata': {
                    'name': value.get('uuid'),
                    'annotations': {
                        'content.halo.run/preferred-editor': 'default',
                    },
                },
            },
            'content': {
                'raw': value.get('content'),
                'content': value.get('content'),
                'rawType': 'HTML',
            },
        }


# client = HaloClient()  # 打印类信息
# print(dir(client))

