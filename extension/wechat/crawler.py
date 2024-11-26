# -*- coding: utf-8 -*-
import asyncio
import json
import re
from typing import Optional, List, Dict, Any

import markdown2

from base import AbstractCrawler
from config import wechat_public_account
from extension.wechat import WeChatClient
from utils import request


class WeChatCrawler(AbstractCrawler):
    def __init__(self):
        self._weChatClient = WeChatClient()

    async def article_path_proc(self, file_name: str, md_content: str):
        html_content = markdown2.markdown(md_content, extras=AbstractCrawler.extensions2)
        return {
            'TITLE': file_name,
            'AUTHOR': "天氰色等烟雨",  # 自定义作者名称
            'DIGEST': None,
            'CONTENT': html_content,
            'CONTENT_SOURCE_URL': None,
            'THUMB_MEDIA_ID': "oL0UpGlBxdUv4oNzDuNmlBA_vUPdtm__P2wPG0TkzmKKXSKy1gGuwn3FZG640iZf",  # 文章封面（必须为永久素材id）
            'X1_Y1_X2_Y2': None,
        }

    async def init_config(self, source_type: str, file_name: str, md_content: str,
                          image_results: Optional[List[Dict[str, Any]]]):
        status_code, access_token_json = await request(method="POST",
                                                       url="https://api.weixin.qq.com/cgi-bin/stable_token",
                                                       json_data=wechat_public_account,
                                                       timeout=10)
        self._weChatClient.access_token = access_token_json["access_token"]
        results = await self.image_process(image_results)
        if results:
            for image_path in results:
                if image_path and "old_image_url" in image_path and "new_image_url" in image_path:
                    md_content = md_content.replace(image_path["old_image_url"], image_path["new_image_url"])
        self._weChatClient.pre_json_data = await self.article_path_proc(file_name, md_content)
        json_data = json.dumps(self._weChatClient.pre_json_data, ensure_ascii=False).encode('utf-8')
        status_code, media_id_json = await request("POST",
                                                   url=self._weChatClient.pre_publish_url,
                                                   content=json_data,
                                                   headers=self._weChatClient.headers,
                                                   timeout=10)

        if 200 <= status_code < 300:
            self._weChatClient.json_data = media_id_json["media_id"]

    async def run(self):
        status_code, result_json = await request("POST",
                                                 url=self._weChatClient.publish_url,
                                                 json_data=self._weChatClient.json_data,
                                                 headers=self._weChatClient.headers,
                                                 timeout=10)
        if 200 <= status_code < 300 and result_json.get("errmsg") == "ok":
            return {'WeChat 发布文章成功!'}
        else:
            return {'WeChat 发布文章失败!'}

    async def image_process(self, image_results):
        if image_results:
            tasks = [self.image_upload(image_result) for image_result in image_results if image_result]
            results = await asyncio.gather(*tasks)
            return results

    async def image_upload(self, image_result):
        pattern = r'[^/]+\.(png|jpg|jpeg|gif|bmp|svg|webp)(?=\?|$)'  # 正则表达式匹配文件名
        match = re.search(pattern, image_result["image_url"])
        if match:
            image_filename = match.group(0)
            image_filenames = image_filename.split(".")
            files = {
                "media": (image_filenames[0] + ".png", image_result["image_content"], 'image/png'),
            }
            status_code, response_json = await request(method="POST",
                                                       url=self._weChatClient.uploadimg_url,
                                                       files=files,
                                                       timeout=10
                                                       )
            if 200 <= status_code < 300:
                return {"old_image_url": image_result["image_url"], "new_image_url": response_json["url"]}




