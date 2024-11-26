import asyncio
from typing import Dict
import markdown2
from base import AbstractCrawler
from extension.halo import HaloClient
from utils import *


class HaloCrawler(AbstractCrawler):

    def __init__(self):
        self._haloClient = HaloClient()

    async def article_path_proc(self, file_name: str, md_content: str) -> Dict:
        uuid_str = generate_uuid()
        # 根据不同来源对markdown格式的文档作分别处理，这里每个实例单独解析content
        html_content = markdown2.markdown(md_content, extras=AbstractCrawler.extensions2)
        self._haloClient.publish_url = uuid_str
        return {
            'title': file_name,
            'slug': convert_to_slug(file_name),
            'publish_time': get_current_time(),
            'uuid': uuid_str,
            'title_html': '<p style="">' + file_name + '</p>',
            'content': html_content,
            'tags': ['测试字段标签'],
        }

    async def init_config(self, source_type: str, file_name: str, md_content: str, image_results):
        self._haloClient.host = source_type
        self._haloClient.cookies = source_type
        results = await self.image_process(image_results)
        if results:
            for image_path in results:
                if image_path and "old_image_url" in image_path and "new_image_url" in image_path:
                    md_content = md_content.replace(image_path["old_image_url"], image_path["new_image_url"])
        self._haloClient.json_data = await self.article_path_proc(file_name, md_content)

    async def run(self):
        code, result = await request(method="POST",
                                     url=self._haloClient.pre_publish_url,
                                     cookies=self._haloClient.cookies,
                                     headers=self._haloClient.headers,
                                     json_data=self._haloClient.json_data,
                                     timeout=10
                                     )
        if not (200 <= code < 300):
            return {'Halo 发布文章失败，请求响应结果：': result}
        # code, result = await request(method="PUT",
        #                              url=self._haloClient.publish_url + '/publish',
        #                              cookies=self._haloClient.cookies,
        #                              headers=self._haloClient.headers,
        #                              timeout=10
        #                              )
        # if not (200 <= code < 300):
        #     return {'Halo 发布文章失败，请求响应结果：': result}
        return {'Halo 发布文章成功，请求响应结果：': code}

    async def image_process(self, image_results):
        if image_results:
            tasks = [self.image_upload(image_result) for image_result in image_results if image_result]
            results = await asyncio.gather(*tasks)
            return results

    async def image_upload(self, image_result):
        pattern = r'[^/]+\.(png|jpg|jpeg|gif|bmp|svg|webp)(?=\?|$)'  # 正则表达式匹配文件名
        match = re.search(pattern, image_result["image_url"])  # 使用 re.search 查找匹配
        if match:
            image_filename = match.group(0)
            image_filenames = image_filename.split(".")
            files = {
                'policyName': (None, 'default-policy'),
                'groupName': (None, ''),
                'file': (image_filename, image_result["image_content"], 'image/' + image_filenames[-1]),
            }
            status_code, response_json = await request(method="POST",
                                                       url=self._haloClient.attachment_publish_url,
                                                       cookies=self._haloClient.cookies,
                                                       headers=self._haloClient.attachment_headers,
                                                       files=files,
                                                       timeout=10
                                                       )
            if 200 <= status_code < 300:
                return {"old_image_url": image_result["image_url"], "new_image_url": "/upload/" + image_filename}


# async def main():
#     await HaloCrawler().init_configs()
# asyncio.run(main())
