from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


def extract_text_from_urls(urls, output_file_name='I001a.txt'):  # 修改默认文件名为 'I001a.txt'
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    file_path = os.path.join(desktop_path, output_file_name)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)

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


if __name__ == "__main__":
    website_urls = [
        "https://rs.p5w.net/investor/002230/base",
        "https://rs.p5w.net/investor/002230/manage/director",
        "https://rs.p5w.net/investor/002230/manage/supervisor",
        "https://rs.p5w.net/investor/002230/manage/leader",
        "https://rs.p5w.net/investor/002230/manage/top10",
        "https://rs.p5w.net/investor/002230/manage/count"
    ]
    extract_text_from_urls(website_urls, 'I001a.txt')  # 指定输出文件名为 'I001a.txt'