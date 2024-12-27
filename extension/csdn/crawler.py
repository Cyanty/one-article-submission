import asyncio
import logging
from typing import Dict
from DrissionPage._functions.keys import Keys
from base import AbstractCrawler
from environment import get_chromium_browser_signal
from extension.csdn import CsdnClient
from utils import logger, github_proxy_url


class CsdnCrawler(AbstractCrawler):

    def __init__(self):
        self.type_crawler = "CSDN Crawler"
        self._csdnClient = CsdnClient()

    async def article_path_proc(self, file_name: str, md_content: str):
        for old_str in github_proxy_url():
            md_content = md_content.replace(old_str, '')
        self._csdnClient.title_name = file_name
        self._csdnClient.md_content = md_content

    async def init_config(self, source_type: str, file_name: str, md_content: str, image_results=None):
        logger.info(f"[{self.type_crawler}] Start initializing the article operation.")
        await self.article_path_proc(file_name, md_content)

    async def run(self):
        logger.info(f'[{self.type_crawler}] Start publishing articles.')
        browser, executor = get_chromium_browser_signal()
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, self.tab_publish_actions, browser)

    def tab_publish_actions(self, browser) -> Dict:
        tab = browser.new_tab()
        try:
            tab.get("https://editor.csdn.net/md/")  # tab_csdn.get("https://mp.csdn.net/mp_blog/creation/editor")
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
            return {'result': AbstractCrawler.SUCCESS_RESULT}
        except Exception as e:
            logging.error(f'[{self.type_crawler}] Failure to publish the article! Cause of error:{e}')
            return {'result': AbstractCrawler.FAILURE_RESULT}
        finally:
            tab.close()





