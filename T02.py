from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time

# 获取当前用户桌面路径
desktop = os.path.join(os.path.expanduser("~"), 'Desktop')

# 目标网址模板
base_url_template = 'https://www.iflytek.com/news/{}'

# 使用Selenium加载页面
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式运行，不打开浏览器窗口
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 初始化新闻列表
all_news_items = []

for news_id in range(799, 2733):  # 包含2732
    url = base_url_template.format(news_id)
    print(f"Processing news ID {news_id}...")

    try:
        driver.get(url)

        # 等待几秒钟让JavaScript完全加载
        time.sleep(5)  # 可以根据实际情况调整等待时间

        # 获取页面源码并解析HTML文档
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # 查找新闻标题、发布日期和详细内容
        title = soup.select_one('div.detail-header h3').get_text(strip=True) if soup.select_one('div.detail-header h3') else "Title not found"
        publish_date = soup.select_one('div.create-info span').get_text(strip=True).replace('发布日期：', '') if soup.select_one('div.create-info span') else "Date not found"
        content = '\n'.join([p.get_text(strip=True) for p in soup.select('div.detail-content p')]) if soup.select('div.detail-content p') else "Content not found"

        # 添加到新闻列表
        all_news_items.append({
            'id': news_id,
            'title': title,
            'publish_date': publish_date,
            'content': content
        })

    except Exception as e:
        print(f"Error processing news ID {news_id}: {e}")

# 关闭浏览器
driver.quit()

# 将新闻信息保存到桌面的TXT文件
output_file_path = os.path.join(desktop, 'ALL_NEWS.txt')
with open(output_file_path, 'w', encoding='utf-8') as file:
    for news_item in all_news_items:
        file.write(f"\n=== 新闻ID: {news_item['id']} ===\n")
        file.write(f"标题: {news_item['title']}\n")
        file.write(f"发布日期: {news_item['publish_date']}\n")
        file.write(f"内容:\n{news_item['content']}\n{'-'*40}\n")

print(f"Extracted {len(all_news_items)} news items and saved to {output_file_path}.")