from enum import Enum, unique

# 指定自定义服务的IP地址列表
CUSTOM_URL_LIST = {
    'HALO': '192.168.1.189',
}


@unique
class Source(Enum):
    """
    已知域名的枚举定义
    """
    CSDN = '.csdn.net'
    JUEJIN = '.juejin.cn'
    CNBLOGS = '.cnblogs.com'
    WECHAT = '.weixin.qq.com'
    BAIDU = '.baidu.com'
    # 自定义服务的IP地址枚举定义
    HALO = CUSTOM_URL_LIST.get('HALO')


WEB_SETUP_SOURCE = {
    Source.CSDN.name: True,
    Source.JUEJIN.name: True,
    Source.CNBLOGS.name: True,
    Source.WECHAT.name: False,
    Source.BAIDU.name: False,
    Source.HALO.name: True,
}




