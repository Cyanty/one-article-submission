from DrissionPage._functions.by import By
from base import AbstractBrowserClient


class CsdnClient(AbstractBrowserClient):

    def __init__(self):
        self._title_name = None
        self._md_content = None

    @property
    def loc_title(self):  # 标题
        return By.XPATH, '//div[contains(@class,"article-bar")]//input[contains(@placeholder,"请输入文章标题")]'

    @property
    def loc_content(self):  # 内容
        return By.XPATH, '//div[@class="editor"]//div[@class="cledit-section"]'

    @property
    def loc_send_button(self):  # 发布设置按钮
        return By.XPATH, '//button[contains(@class, "btn-publish") and contains(text(),"发布文章")]'

    @property
    def loc_add_tag(self):  # 标签
        return By.XPATH, '//div[@class="mark_selection"]//button[@class="tag__btn-tag" and contains(text(),"添加文章标签")]'

    @property
    def loc_tag_input(self):  # 标签输入框
        return By.XPATH, '//div[@class="mark_selection_box"]//input[contains(@placeholder,"请输入文字搜索")]'

    @property
    def loc_close_button(self):  # 标签关闭按钮
        return By.XPATH, '//div[@class="mark_selection_box"]//button[@title="关闭"]'

    @property
    def loc_summary_input(self):  # 摘要
        return By.XPATH, '//div[@class="desc-box"]//textarea[contains(@placeholder,"摘要：会在推荐、列表等场景外露")]'

    @property
    def loc_publish_button(self):  # 发布按钮
        return By.XPATH, '//button[contains(@class, "button btn-b-red ml16") and contains(text(),"发布文章")]'

    @property
    def title_name(self):
        return self._title_name

    @title_name.setter
    def title_name(self, value: str):
        self._title_name = value

    @property
    def md_content(self):
        return self._md_content

    @md_content.setter
    def md_content(self, value: str):
        self._md_content = value










