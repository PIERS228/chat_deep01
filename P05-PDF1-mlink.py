from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time

# 获取当前用户桌面路径
desktop = os.path.join(os.path.expanduser("~"), 'Desktop')

# 目标网址
base_url = 'https://rs.p5w.net/investor/002230/interact/record'

# 使用Selenium加载页面
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式运行，不打开浏览器窗口
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 初始化PDF链接列表
all_pdf_links = []

# 分页参数
total_pages = 9  # 假设有107页
pdf_per_page = 20  # 每页20个PDF

for page in range(1, total_pages + 1):
    print(f"Processing page {page}...")

    # 构建每一页的URL（根据实际情况调整URL构建逻辑）
    if page == 1:
        url = base_url
    else:
        url = f'{base_url}?page={page}'  # 假设分页是通过URL参数?page=实现的

    driver.get(url)

    # 等待几秒钟让JavaScript完全加载
    time.sleep(5)  # 可以根据实际情况调整等待时间

    # 获取页面源码并解析HTML文档
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有PDF链接
    pdf_links = []
    for link in soup.find_all('a', href=True):
        if '.pdf' in link['href'].lower():
            pdf_links.append(link['href'])

    all_pdf_links.extend(pdf_links)

    # 如果没有找到任何链接，打印出所有的<a>标签及其href属性进行调试
    if not pdf_links:
        print(f"No PDF links found on page {page}. Here are all <a> tags with href attributes:")
        for link in soup.find_all('a', href=True):
            print(f"{link['href']}")

# 关闭浏览器
driver.quit()

# 将链接保存到桌面的TXT文件
output_file_path = os.path.join(desktop, 'PDF.txt')
with open(output_file_path, 'w') as file:
    for pdf_link in all_pdf_links:
        file.write(pdf_link + '\n')

print(f"Extracted {len(all_pdf_links)} PDF links and saved to {output_file_path}.")