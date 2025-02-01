from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time


def extract_and_save_links(url, output_file_name='TEST002.txt'):
    # 获取当前用户的桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    file_path = os.path.join(desktop_path, output_file_name)

    # 设置Chrome选项以无头模式运行（即不打开浏览器窗口）
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--disable-dev-shm-usage')  # 解决资源限制问题

    # 创建WebDriver对象，这里假设你已经将chromedriver放在了系统PATH中
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开目标网站
        driver.get(url)

        # 等待页面加载完成（这里简单地等待几秒钟；更复杂的情况可以使用显式等待）
        time.sleep(5)

        # 获取页面源代码
        page_source = driver.page_source

        # 解析HTML内容
        soup = BeautifulSoup(page_source, 'html.parser')

        # 打开文件准备写入
        with open(file_path, 'w', encoding='utf-8') as file:
            # 查找所有的<a>标签
            for link in soup.find_all('a', href=True):
                href = link['href']

                # 构建完整的URL
                if href.startswith('http') or href.startswith('//'):
                    full_url = href
                elif href.startswith('/'):
                    full_url = f"https://edu.iflytek.com/{href}"
                else:
                    full_url = f"https://edu.iflytek.com/{href}"

                # 获取链接的文本
                link_text = link.get_text(strip=True)

                # 写入文件
                file.write(f"Link Text: {link_text}, URL: {full_url}\n")
                print(f"已添加: {link_text} -> {full_url}")

        print(f"链接已成功提取并保存到 {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭浏览器
        driver.quit()


if __name__ == "__main__":
    website_url = "https://edu.iflytek.com/"
    extract_and_save_links(website_url, 'TEST009.txt')