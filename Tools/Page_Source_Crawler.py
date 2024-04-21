from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def Crawler(url, num):
    # Configure ChromeOptions for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode
    chrome_options.add_argument("--disable-gpu")  # For compatibility with some systems

    # Initialize WebDriver with ChromeOptions
    driver = webdriver.Chrome(r"C:\path\to\chromedriver.exe", options=chrome_options)

    # 可以自己改要将page_source存到哪里
    path_str = f"C:/Users/User/Downloads/BACD-v2/source/page_source/webpage_{num}.txt"

    # Open the webpage
    driver.get(url)

    # Get the outer HTML of the entire page
    elem = driver.find_element("xpath", "//*")  # Find the root element
    source_code = elem.get_attribute("outerHTML")  # Get the HTML content

    # Save the source code to a file
    with open(path_str, 'w', encoding="utf-8") as f:
        f.write(source_code)  # Write the HTML content

    # Close the WebDriver
    driver.quit()

    return path_str