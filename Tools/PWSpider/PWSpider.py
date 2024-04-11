from playwright.sync_api import sync_playwright
from collections import defaultdict
import json
"https://www.xhsd.com/"
class BaseSpider:
    def __init__(self, url) -> None:
        self.domain = url

    def record_traffic(self, page, page_actions):
        # 监听请求
        def on_request(request):
            request_url = request.url
            request_method = request.method
            request_headers = dict(request.headers)
            request_body = request.post_data

            page_actions.append({
                'type': 'request',
                'url': request_url,
                'method': request_method,
                'headers': request_headers,
                'body': request_body
            })

        # 监听响应
        def on_response(response):
            response_url = response.url
            response_status = response.status
            response_headers = dict(response.headers)
            response_body = response.body()

            page_actions.append({
                'type': 'response',
                'url': response_url,
                'status': response_status,
                'headers': response_headers,
                'body': response_body
            })

        page.on('request', on_request)
        page.on('response', on_response)

    def traverse_website(self, page, url, visited_pages, page_actions):
        if url in visited_pages:
            return
        visited_pages.add(url)

        print("---------------------------\nVisiting:" + url + "\n---------------------------")
        page.goto(url)
        self.record_traffic(page, page_actions)

        links = page.query_selector_all('a')
        for link in links:
            href = link.get_attribute('href')
            self.traverse_website(page, self.domain + href, visited_pages, page_actions)

        # 在这里可以执行其他行为，比如点击按钮等

    def main(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()

            page_actions = []
            visited_pages = set()

            page = context.new_page()
            self.traverse_website(page, url, visited_pages, page_actions)

            browser.close()

            # 将结果保存到文件
            with open('crawl_result.json', 'w') as f:
                json.dump({
                    'visited_pages': list(visited_pages),
                    'page_actions': page_actions
                }, f, indent=4)

if __name__ == "__main__":
    bs = BaseSpider("https://www.xhsd.com")
    bs.main("https://www.xhsd.com")