# 定义一个 Pydantic 模型来接收请求体中的数据
from pydantic import BaseModel
from config import Source


class ToggleState(BaseModel):
    type: str
    new_state: bool


def get_result_dict():
    result_dict = {}
    for source in Source:
        result_dict[source.name] = {'result': '还没有要发布文章~'}
    return result_dict


