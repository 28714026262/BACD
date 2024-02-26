from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import threading
from os import path as OSPath
from Tools.logger import get_logger

logger = get_logger(name = OSPath.basename(__file__))

class HTMLSourceCodeAttacher:
    def __init__(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
        chrome_options.add_argument("--disable-gpu")  # 去除GPU加速，提高系统兼容性      

    def DynamicHTMLCodeExtractionThreadWorker(self, target_url, target_headers, callback, waiting_time = 5):
        # chrome浏览器启动
        driver_path = "/path/to/chromedriver"  # ChromeDriver 的路径
        service = Service(driver_path)
        service.start()
        driver = webdriver.Chrome(service=service, options=self.chrome_options)
        try:
            # 设置请求头
            for key, value in target_headers.items():
                self.driver.add_header(key, value)

            # 使用 Selenium 发送请求并获取页面内容
            driver.get(target_url)
            time.sleep(waiting_time)  # 等待页面加载完成，这里可以根据实际情况调整等待时间
            page_source = driver.page_source

            # 输出页面内容
            logger.debug(page_source)
            callback(target_url, target_headers, page_source)

        finally:
            # 关闭浏览器
            driver.quit()

    def callback_HTMLSourceCode(self):
        # 这里应该向具体node进行sourcecode输出，或者由调用者提供callback
        # 分为两步
        # 存储到外部文件或数据库中
        # 返回source code file path
        pass

    def DynamicHTMLCodeExtract(self, callback_function):
        # 创建一个新线程，并传递回调函数作为参数
        thread = threading.Thread(target=self.DynamicHTMLCodeExtractionThreadWorker, args=(callback_function,))
        # 启动线程
        thread.start()

        # 主线程可以继续执行其他操作
        logger.debug("Side thread started for html source code!")

        # 等待新线程执行完成
        thread.join()