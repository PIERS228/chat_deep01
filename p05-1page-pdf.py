from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os

# 获取当前用户桌面路径
desktop = os.path.join(os.path.expanduser("~"), 'Desktop')

# 目标网址
url = 'https://rs.p5w.net/investor/002230/notice/last'

# 使用Selenium加载页面
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式运行，不打开浏览器窗口
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get(url)

# 等待几秒钟让JavaScript完全加载
import time
time.sleep(5)  # 可以根据实际情况调整等待时间

# 获取页面源码并解析HTML文档
html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有PDF链接
pdf_links = []
for link in soup.find_all('a', href=True):
    if '.pdf' in link['href'].lower():
        pdf_links.append(link['href'])

# 将链接保存到桌面的TXT文件
output_file_path = os.path.join(desktop, 'PDF.txt')
with open(output_file_path, 'w') as file:
    for pdf_link in pdf_links:
        file.write(pdf_link + '\n')

print(f"Extracted {len(pdf_links)} PDF links and saved to {output_file_path}.")

# 如果没有找到任何链接，打印出所有的<a>标签及其href属性进行调试
if not pdf_links:
    print("No PDF links found. Here are all <a> tags with href attributes:")
    for link in soup.find_all('a', href=True):
        print(f"{link['href']}")