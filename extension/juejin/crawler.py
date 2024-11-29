import time
from typing import Dict
from base import AbstractCrawler
from environment import get_chromium_page_single
from extension.juejin import JueJinClient
from utils import *


class JueJinCrawler(AbstractCrawler):

    def __init__(self):
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
        logger.info("JueJin 开始初始化文章操作")
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
        logger.info("JueJin 开始发布文章")
        code, result = await self.request_post(
            url_type=self._jueJinClient.pre_publish_url,
            json_data_type=self._jueJinClient.pre_json_data
        )
        if 200 <= code < 300 and result['err_msg'] == 'success':
            tab = get_chromium_page_single().new_tab()
            tab.get('https://juejin.cn/editor/drafts/' + self._jueJinClient.host)
            try:
                time.sleep(1)  # 等待页面装载外链图片
                tab.actions \
                    .click(on_ele=tab.ele(self._jueJinClient.loc_publish_button)).wait(0.5) \
                    .click(on_ele=tab.ele(self._jueJinClient.loc_confirm_publish_button)).wait(1)
                tab.wait.load_start()
                return {'result': AbstractCrawler.SUCCESS_RESULT}
            except Exception as e:
                logger.error(f'JueJin 发布文章失败，报错原因：{e}')
                return {'result': AbstractCrawler.FAILURE_RESULT}
            finally:
                tab.close()

            # code, result = await self.request_post(
            #     url_type=self._jueJinClient.publish_url,
            #     json_data_type=self._jueJinClient.json_data
            # )
        else:
            logger.error('JueJin 发布文章失败，请求响应结果：' + str(result))
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



