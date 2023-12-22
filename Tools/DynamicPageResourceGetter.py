from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_dynamic_page_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    page_content = ""
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        driver.implicitly_wait(10)
        page_content = driver.page_source
    finally:
        driver.quit()
    
    return page_content