import asyncio
import datetime
from base import AbstractCrawler
from extension.cnblogs import CnBlogsMetaBlogClient
from utils import logger
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError


class CnBlogsCrawler(AbstractCrawler):
    def __init__(self):
        self._cnBlogsMetaBlogClient = CnBlogsMetaBlogClient()
        self._cnBlogsMetaBlogClient.read_config()
        self.post_data = None

    async def article_path_proc(self, file_name: str, md_content: str):
        return {
            "dateCreated": datetime.datetime.now(),
            "title": file_name,
            "description": md_content,
            "categories": ["[Markdown]"],  # 设置默认为markdown编辑器
            "mt_keywords": "大数据"  # 标签
        }

    async def init_config(self, source_type: str, file_name: str, md_content: str, image_results):
        logger.info(f"CNBLOGS 开始初始化并处理图片链接")
        results = await self.image_process(image_results)
        if results:
            for image_path in results:
                if image_path and "old_image_url" in image_path and "new_image_url" in image_path:
                    md_content = md_content.replace(image_path["old_image_url"], image_path["new_image_url"])
        self.post_data = await self.article_path_proc(file_name, md_content)

    async def run(self):
        logger.info(f'CNBLOGS 开始发布文章!')
        try:
            post_id = await self.new_post()  # 发布文章返回的文章id
            return {'result': AbstractCrawler.SUCCESS_RESULT}
        except RetryError as e:
            logger.info(f'CNBLOGS 发布文章失败! 报错原因:{e.last_attempt.exception()}')  # 获取最后一次重试的异常
            return {'result': AbstractCrawler.FAILURE_RESULT}

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def new_post(self):
        try:
            return self._cnBlogsMetaBlogClient.new_post(self.post_data, True)  # 返回博文ID
        except Exception as e:
            raise Exception(e)

    async def image_process(self, image_results):
        if image_results:
            tasks = [self.new_media_object(image_result["image_url"], image_result["image_content"])
                     for image_result in image_results
                     if image_result]
            results = await asyncio.gather(*tasks)
            return results

    async def new_media_object(self, image_url, image_content):
        for i in range(3):
            try:
                new_image_url = self._cnBlogsMetaBlogClient.new_media_object({
                    "bits": image_content,
                    "name": "abc.png",
                    "type": "image/png"
                })
                return {"old_image_url": image_url, "new_image_url": new_image_url.get("url")}
            except Exception as e:
                logger.error(f"cnblogs 请求图片链接失败！- {e}")







