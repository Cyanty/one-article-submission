# encoding = utf-8
# !/bin/sh python3
import xmlrpc.client as xmlrpclib
from config import CNBLOGS_METABLOG_CONFIG
from utils import logger


class CnBlogsMetaBlogClient:
    """
    metaweblog文档：https://rpc.cnblogs.com/metaweblog/zhaoqingqing#Post

    配置字典：
    type | description(example)
    str  | metaWeblog url, 博客设置中有('https://rpc.cnblogs.com/metaweblog/1024th')
    str  | appkey, Blog地址名('1024th')
    str  | blogid, 这个无需手动输入，通过getUsersBlogs得到
    str  | usr, 登录用户名
    str  | passwd, 登录密码
    str  | rootpath, 博文存放根路径（添加git管理）
    """
    def __init__(self):
        self._config = None
        self._server = None
        self._mwb = None

    def read_config(self):
        """ 读取配置 """
        try:
            self._config = CNBLOGS_METABLOG_CONFIG
            self._server = xmlrpclib.ServerProxy(CNBLOGS_METABLOG_CONFIG["url"])
            self._mwb = self._server.metaWeblog
            self._config["blogid"] = self.get_users_blogs()[0]["blogid"]
        except Exception as e:
            logger.error(f"cnblogs metablog config 发生错误！- {e}")

    def get_users_blogs(self):
        """ 获取博客信息 @return: { string blogid, string url, string blogName } """
        return self._server.blogger.getUsersBlogs(self._config["appkey"], self._config["usr"], self._config["passwd"])

    def get_recent_posts(self, num):
        """ 读取最近的博文信息 """
        return self._mwb.getRecentPosts(self._config["blogid"], self._config["usr"], self._config["passwd"], num)

    def new_post(self, post, publish):
        """ 发布新博文  @post: 发布内容 , @publish: 是否公开 , @return: 博文ID """
        return self._mwb.newPost(self._config['blogid'], self._config['usr'], self._config['passwd'], post, publish)

    def edit_post(self, postid, post, publish):
        """ 更新已存在的博文  @postid: 已存在博文ID , @post: 发布内容 , @publish: 是否公开发布 """
        self._mwb.editPost(postid, self._config['usr'], self._config['passwd'], post, publish)

    def delete_post(self, postid, publish):
        """ 删除博文 """
        self._mwb.deletePost(self._config['appkey'], postid, self._config['usr'], self._config['passwd'], publish)

    def get_categories(self):
        """ 获取博文分类 """
        return self._mwb.getCategories(self._config['blogid'], self._config['usr'], self._config['passwd'])

    def get_post(self, postid):
        """ 读取博文信息 @postid: 博文ID , @return: POST """
        return self._mwb.getPost(postid, self._config['usr'], self._config['passwd'])

    def new_media_object(self, file):
        """ 资源文件（图片，音频，视频...)上传  @file: { base64 bits, string name, string type } , @return: URL """
        return self._mwb.newMediaObject(self._config['blogid'], self._config['usr'], self._config['passwd'], file)

    def new_category(self, categoray):
        """ 新建分类 @categoray: { string name, string slug(optional), integer parent_id, string description(optional) }
                    @return : categorayid """
        return self._server.wp.newCategory(self._config['blogid'], self._config['usr'], self._config['passwd'],
                                           categoray)

