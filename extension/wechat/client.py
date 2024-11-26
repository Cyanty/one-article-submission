from base import AbstractClient


class WeChatClient(AbstractClient):
    """
    微信公众号开发者API文档：https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Access_Overview.html
    """
    def __init__(self):
        self._access_token = None
        self._pre_json_data = None
        self._json_data = None

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value: str):
        self._access_token = value

    @property
    def uploadimg_url(self):
        return "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=" + self._access_token

    @property
    def pre_publish_url(self):
        return "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=" + self._access_token

    @property
    def publish_url(self):
        return "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=" + self._access_token

    @property
    def cookies(self):
        return {}

    @property
    def headers(self):
        return {'Content-Type': 'application/json'}

    @property
    def pre_json_data(self):
        return self._pre_json_data

    @pre_json_data.setter
    def pre_json_data(self, value):
        self._pre_json_data = {
            "articles": [
                {
                    "title": value["TITLE"],  # 标题
                    "author": value["AUTHOR"],  # 作者
                    "digest": value["DIGEST"],  # 图文消息的摘要，仅有单图文消息才有摘要，多图文此处为空。如果本字段为没有填写，则默认抓取正文前54个字。
                    "content": value["CONTENT"],  # 图文消息的具体内容，支持HTML标签，必须少于2万字符，小于1M，且此处会去除JS,涉及图片url必须来源 "上传图文消息内的图片获取URL"接口获取。外部图片url将被过滤。
                    "content_source_url": value["CONTENT_SOURCE_URL"],  # 图文消息的原文地址，即点击“阅读原文”后的URL
                    "thumb_media_id": value["THUMB_MEDIA_ID"],  # 图文消息的封面图片素材id（必须是永久MediaID）
                    "need_open_comment":1,  # Uint32 是否打开评论，0不打开(默认)，1打开
                    "only_fans_can_comment":0,  # Uint32 是否粉丝才可评论，0所有人可评论(默认)，1粉丝才可评论
                    "pic_crop_235_1": value["X1_Y1_X2_Y2"],
                    "pic_crop_1_1": value["X1_Y1_X2_Y2"]
                }
                # 若新增的是多图文素材，则此处应还有几段articles结构
            ]
        }

    @property
    def json_data(self):
        return self._json_data

    @json_data.setter
    def json_data(self, value):
        self._json_data = {
            "media_id": value
        }




