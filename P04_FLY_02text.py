from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time
import re  # 确保导入了re模块用于sanitize_filename函数

# 定义清理文件名的函数
def sanitize_filename(filename):
    """清理字符串以适合作为文件名"""
    filename = re.sub(r'[\\/*?:"<>|\n\r\t]', "", filename)
    filename = filename.strip().replace(' ', '_')[:100]
    return filename or "default_filename"

# 定义提取并保存链接及文本内容的函数
def extract_text_from_urls(urls, output_file_name='Q003.txt'):  # 修改默认文件名为 'Q003.txt'
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    file_path = os.path.join(desktop_path, output_file_name)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--disable-dev-shm-usage')  # 解决资源限制问题

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        all_text_content = ""
        for url in urls:
            print(f"正在处理: {url}")
            driver.get(url)

            wait = WebDriverWait(driver, 10)  # 等待最多10秒

            # 等待body标签内的文本加载完成，并滚动页面加载所有动态内容
            body_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # 直接从driver获取body元素的文本，避免解析整个HTML
            body_text = driver.find_element(By.TAG_NAME, "body").text

            # 添加分隔符以区分不同网页的内容
            all_text_content += f"\n=== URL: {url} ===\n{body_text}\n"

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(all_text_content)

        print(f"所有文本已成功提取并保存到 {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()

# 从文件中读取网址
def read_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

if __name__ == "__main__":
    input_file_path = r"C:\Users\Piers\Desktop\TEST004.txt"  # 使用原始字符串来避免转义字符问题
    website_urls = read_urls_from_file(input_file_path)
    extract_text_from_urls(website_urls, output_file_name='Q003_AICC.txt')  # 使用指定参数，文件名为 'Q003.txt'