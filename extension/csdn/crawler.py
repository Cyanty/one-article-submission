from typing import Optional, List, Dict, Any

from DrissionPage._functions.keys import Keys
from base import AbstractCrawler
from environment import get_chromium_page
from extension.csdn import CsdnClient


class CsdnCrawler(AbstractCrawler):

    def __init__(self):
        self._csdnClient = CsdnClient()

    async def article_path_proc(self, file_name: str, md_content: str):
        md_content = md_content.replace('https://github.moeyy.xyz/', '')
        self._csdnClient.title_name = file_name
        self._csdnClient.md_content = md_content

    async def init_config(self, source_type: str, file_name: str, md_content: str, image_results=None):
        await self.article_path_proc(file_name, md_content)

    async def run(self):
        tab = get_chromium_page().new_tab()
        tab.get("https://editor.csdn.net/md/")  # tab_csdn.get("https://mp.csdn.net/mp_blog/creation/editor")
        try:
            tab.actions \
                .click(on_ele=tab.ele(self._csdnClient.loc_title)).input(self._csdnClient.title_name) \
                .click(on_ele=tab.ele(self._csdnClient.loc_content)).input(self._csdnClient.md_content)
            tab.wait.load_start()
            tab.actions \
                .click(on_ele=tab.ele(self._csdnClient.loc_send_button)).wait(0.25) \
                .move_to(ele_or_loc=tab.ele(self._csdnClient.loc_add_tag)).wait(0.25) \
                .click(on_ele=tab.ele(self._csdnClient.loc_tag_input)).input("大数据").wait(1) \
                .key_down(Keys.ENTER).wait(0.25) \
                .click(on_ele=tab.ele(self._csdnClient.loc_close_button)) \
                .click(on_ele=tab.ele(self._csdnClient.loc_publish_button))
            tab.wait.load_start()
            return {'CSDN 发布文章成功'}
        except Exception as e:
            return {f'CSDN 发布文章失败，报错原因：{e}'}
        finally:
            tab.close()





