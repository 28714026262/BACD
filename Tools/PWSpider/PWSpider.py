'''
Author: Suez_kip 287140262@qq.com
Date: 2024-04-08 11:41:58
LastEditTime: 2024-04-08 12:51:26
LastEditors: Suez_kip
Description: 
'''
import asyncio
import base64
import os
import traceback
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from playwright._impl._page import Page
from playwright._impl._browser import Browser
from playwright._impl._network import Response
from Tools.logger import get_logger

logger = get_logger(name = os.path.basename(__file__))
# utils.Tools delet

class BaseSpider:
    def __init__(self, browser:Browser, loop, tid: str, mode: str = "detect", ignore: str = "", **kwargs):
        self.mode = mode
        self.browser = browser
        self.storage = ""
        self.content = None
        self.host = ""
        self.ignore = ignore.split(";")
        self.request_num = 0
        self.request_time = 0.0
        self.tid = tid
        self.captcha = 'knv4'
        self.scan_domain = set()
        asyncio.set_event_loop(loop=loop)

    def get_host(self, url):
        ps = urlparse(url)
        self.host = ps.scheme + "://" + ps.netloc

    async def get_response_log(
        self, response: Response, id: str="000",random_flag: bool=False, 
        post_data:str="", res_data: str=""
    ) -> str:
        """
        根据Playwright Response得到Burplog格式日志记录
        >>> args:  
        response # playwright Response对象
        post_data: str # 可选, 指定post data
        res_data: str  # 可选, 指定返回数据
        >>> return -> str # burplog格式日志
        """
        log_data = '='*54 + '\n' + datetime.now().strftime('%H:%M:%S') + '  '
        req = response.request
        # url静态资源审查
        # if Tools.is_stastic(req.url):
        #     return None
        
        parse_url = urlparse(req.url)
        path = parse_url.path
        if parse_url.query != "":
            path = path + "?" + parse_url.query
        if parse_url.fragment == "":
            pass
        else:
            path = path + "#" + parse_url.fragment.split("?", 1)[0]  # noqa


        port = ''
        if not parse_url.port:
            port = ':80' if parse_url.scheme=='http' else ':443'
        log_data += f"{parse_url.scheme}://{parse_url.netloc}{port}\n{'='*54}\n"
        log_data += f"{req.method} {path}\n"
        headers = await req.all_headers()
        log_data += '\n'.join([f"{x.lstrip(':')}: {y}" for x, y in headers.items() if not x.startswith(':')])
        log_data += '\n\n'
        if req.method == 'POST' or req.method == "PUT":
            try:
                if post_data:
                    log_data += post_data + '\n'
                elif req.post_data:
                    log_data += req.post_data + '\n'
            except:
                if req.post_data_buffer:
                    log_data += req.post_data_buffer.decode(errors='ignore') + '\n'
        log_data += '='*54 + '\n'
        #记录response
        if response.status != 200:
            log_data += f"HTTP {response.status} BAD\n"
        else:
            log_data += f"HTTP {response.status} OK\n"

        headers = await response.all_headers()
        log_data += '\n'.join([f"{x}: {y}" for x, y in headers.items()])
        if random_flag: # 表明是随机填写的，响应不作为判定成功的依据
            log_data += f"\nRandom-Flag: 1"
        if response.status != 200:
            log_data += '\n' + '='*54 + '\n\n'
            return log_data

        if res_data:
            body_str = res_data
            body = res_data.encode(errors='ignore')
        else:
            try:
                body: bytes = await response.body()
            except Exception as e:
                logger.warning(f"[baseSpider] Get log failed, {req.url}\n{e.args[0]}")
                return None
            try:
                body_str = body.decode(encoding='utf-8', errors='ignore')
            except Exception as e:
                logger.error(f"[baseSpider] Response body decoding failed! {e.args[0]}")
                body_str = ''
                traceback.print_exc()

        # if "captcha" in req.url.lower():
        #     test_point = 1
        content_type_str_UP = response.headers.get("Content-Type", "unknown")
        content_type_str_LOW = response.headers.get("content-type", "unknown")
        # mime = Tools.mime_type(body)
        try:
            if content_type_str_UP.startswith("image") or content_type_str_LOW.startswith("image"): # mime.startswith('image') or content_type_str_UP.startswith("image") or content_type_str_LOW.startswith("image"):
                body_str = base64.b64encode(body).decode('ascii')
        except Exception as e:
            logger.debug("IMAGE FILE HAS BEEN DETECTED! BUT ANALYZER HAS CRASDED in func get_response_log!")
            logger.debug(e)
        # log_data += f"\nMIME-Type: {mime}\n"
        log_data += f"LOG-ID: {id}\n"

        log_data += '\n' + body_str + '\n'
        log_data += '='*54 + '\n\n'

        return log_data
        
    async def async_init_hook(self, page):
        page.on("dialog", self.handle_dialog)

    async def new_page(self) -> Page:
        """
        :param origin: local storage的源
        :return:
        """
        if self.content is None:
            # if GLOBAL.VIEWPORT:
            #     options = {"ignore_https_errors": True,"locale": "zh-CN", "viewport": GLOBAL.VIEWPORT}
            # else:
            #     options = {"ignore_https_errors": True,"locale": "zh-CN"}
            options = {"ignore_https_errors": True,"locale": "zh-CN"}
            self.content = await self.browser.new_context(**options)
        page = await self.content.new_page()
        page.set_default_navigation_timeout(25000)
        return page

    async def browser_open_url(self, page: Page, url: str):
        # await self.sleep(GLOBAL.SPIDER_INTERVAL)
        logger.info(f"[+] 请求地址 {url}")
        res = await page.goto(url=url, timeout=25000)
        await page.wait_for_timeout(1500)
        return res

    @staticmethod
    async def handle_dialog(dialog):
        await dialog.dismiss()

    @staticmethod
    async def sleep(timeout: float = 1.0):
        await asyncio.sleep(timeout)

    async def close_other_pages(self, first=1):
        """
            关闭多余的标签页
        :param first: 前几个
        :return:
        """
        for i in self.content.pages[first:]:
            await i.close()

    async def close(self):
        await self.content.close()