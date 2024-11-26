# -*- coding: utf-8 -*-
from extension import *
import asyncio
import re
from base import AbstractCrawler
from utils import *
from functools import wraps
from config import WEB_SETUP_SOURCE, Source


class EmptyClass:
    pass


class CrawlerFactory:
    CRAWLERS = {
        Source.CSDN.name: CsdnCrawler,
        Source.JUEJIN.name: JueJinCrawler,
        Source.CNBLOGS.name: CnBlogsCrawler,
        Source.WECHAT.name: WeChatCrawler,
        Source.BAIDU.name: EmptyClass,
        Source.HALO.name: HaloCrawler,
    }

    @staticmethod
    def create_crawler(source_name: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(source_name)
        if not crawler_class:
            logger.error("未定义此来源的发布模块...")
        return crawler_class()


def config_feature(source_name: str):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if WEB_SETUP_SOURCE.get(source_name, False):
                return await func(*args, **kwargs)
            else:
                return {f"来源 {source_name} 未启用"}
        return async_wrapper
    return decorator


async def image_request(md_content: str):
    pattern = r'!\[.*?\]\((.*?)\)'  # 正则表达式匹配图片URL, 匹配格式：![alt text](URL)
    matches = re.findall(pattern, md_content)  # 查找所有匹配的图片 URL
    tasks = [request_img("GET", image_url, timeout=10) for image_url in matches]
    results = await asyncio.gather(*tasks)
    image_results = [
        {"image_url": image_url, "image_content": image_content}
        for image_url, status_code, image_content in results
        if 200 <= status_code < 300
    ]
    return image_results


async def crawlers_start(file_name: str, md_content: str):
    file_name = file_name.split(".")[0]
    logger.info(f"开始发布文章: {file_name}")
    image_results = await image_request(md_content)
    result_dict = {}
    tasks = []
    for source in Source:
        crawler_object = CrawlerFactory.create_crawler(source.name)

        @config_feature(source.name)
        async def start(crawler_class: AbstractCrawler, source_type: str):
            await crawler_class.init_config(source_type=source_type,
                                            file_name=file_name,
                                            md_content=md_content,
                                            image_results=image_results)
            return await crawler_class.run()

        tasks.append(start(crawler_object, source.value))

    results = await asyncio.gather(*tasks)
    for source, result in zip(Source, results):
        result_dict[source.name] = result

    logger.info("文章发布完毕！")
    return result_dict


