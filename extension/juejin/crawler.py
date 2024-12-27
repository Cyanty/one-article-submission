import asyncio
import time
from threading import Thread
from typing import Dict
from base import AbstractCrawler
from environment import get_chromium_browser_signal
from extension.juejin import JueJinClient
from utils import *


class JueJinCrawler(AbstractCrawler):

    def __init__(self):
        self.type_crawler = "JueJin Crawler"
        self._jueJinClient = JueJinClient()

    async def article_path_proc(self, file_name: str, md_content: str) -> Dict:
        return {
            'title': file_name,
            'id': None,
            'content': md_content,
            'encrypted_word_count': None,
            'origin_word_count': len(md_content),
        }

    async def init_config(self, source_type: str, file_name: str, md_content: str, image_results=None):
        logger.info(f"[{self.type_crawler}] Start initializing the article operation.")
        value: dict = await self.article_path_proc(file_name, md_content)
        self._jueJinClient.cookies = source_type
        self._jueJinClient.create_json_data = value
        code, result = await self.request_post(
            url_type=self._jueJinClient.create_publish_url,
            json_data_type=self._jueJinClient.create_json_data
        )
        if 200 <= code < 300 and result['err_msg'] == 'success':
            value.update({'id': result['data']['id']})
            self._jueJinClient.host = value.get('id')
            self._jueJinClient.pre_json_data = value
            self._jueJinClient.json_data = value

    async def run(self):
        logger.info(f'[{self.type_crawler}] Start publishing articles.')
        code, result = await self.request_post(
            url_type=self._jueJinClient.pre_publish_url,
            json_data_type=self._jueJinClient.pre_json_data
        )
        if 200 <= code < 300 and result['err_msg'] == 'success':
            browser, executor = get_chromium_browser_signal()
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(executor, self.tab_publish_actions, browser)
        else:
            logging.error(f'[{self.type_crawler}] Failure to publish the article! Cause of error: Http Response Text -> {str(result)}')
            return {'result': AbstractCrawler.FAILURE_RESULT}

    async def request_post(self, url_type, json_data_type):
        return await request(method="POST",
                             url=url_type,
                             cookies=self._jueJinClient.cookies,
                             headers=self._jueJinClient.headers,
                             json_data=json_data_type,
                             params=self._jueJinClient.params,
                             timeout=10
                             )

    def tab_publish_actions(self, browser) -> Dict:
        tab = browser.new_tab()
        try:
            tab.get('https://juejin.cn/editor/drafts/' + self._jueJinClient.host)
            tab.actions \
                .click(on_ele=tab.ele(self._jueJinClient.loc_publish_button)).wait(0.5) \
                .click(on_ele=tab.ele(self._jueJinClient.loc_confirm_publish_button)).wait(1)
            tab.wait.load_start()
            return {'result': AbstractCrawler.SUCCESS_RESULT}
        except Exception as e:
            logger.error(f'[{self.type_crawler}] Failure to publish the article! Cause of error:{e}')
            return {'result': AbstractCrawler.FAILURE_RESULT}
        finally:
            tab.close()


