import re
from pypinyin import pinyin, lazy_pinyin, Style
from datetime import datetime
import uuid


def convert_to_slug(title):
    pinyin_list = lazy_pinyin(title)
    slug = '-'.join(pinyin_list)
    slug = re.sub(r'-+', '-', slug)
    return slug


def get_current_time():
    now = datetime.utcnow()
    return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def generate_uuid():
    return str(uuid.uuid1())  # 生成基于时间的UUID


def generate_uuid4():
    return str(uuid.uuid4())  # 生成一个随机的UUID



