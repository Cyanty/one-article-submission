from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class AbstractCrawler(ABC):
    extensions2 = [
        "fenced-code-blocks",
        "footnotes",
        "header-ids",
        "tables",
        "smarty-pants",
        "strike",
        "task_list",
        "toc"
    ]

    SUCCESS_RESULT = "太棒了，文章发布成功~!"
    FAILURE_RESULT = "文章发布失败了，好事多磨!"

    @abstractmethod
    async def article_path_proc(self, file_name: str, md_content: str):
        pass

    @abstractmethod
    async def init_config(self,
                          source_type: str,
                          file_name: str,
                          md_content: str,
                          image_results: Optional[List[Dict[str, Any]]]):
        pass

    @abstractmethod
    async def run(self):
        pass


class AbstractClient(ABC):
    @property
    @abstractmethod
    def pre_publish_url(self):
        ...

    @property
    @abstractmethod
    def publish_url(self):
        ...

    @property
    @abstractmethod
    def cookies(self):
        ...

    @property
    @abstractmethod
    def headers(self):
        ...

    @property
    @abstractmethod
    def json_data(self):
        ...


class AbstractBrowserClient(ABC):
    @property
    @abstractmethod
    def loc_title(self):  # 标题
        ...

    @property
    @abstractmethod
    def loc_content(self):  # 内容
        ...

    @property
    @abstractmethod
    def loc_publish_button(self):  # 发布按钮
        ...

    @property
    @abstractmethod
    def title_name(self):  # 文章标题
        ...

    @property
    @abstractmethod
    def md_content(self):  # 文章内容
        ...





