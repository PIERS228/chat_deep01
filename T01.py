from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 获取当前用户桌面路径
desktop = os.path.join(os.path.expanduser("~"), 'Desktop')

# 目标网址
base_url = 'https://rs.p5w.net/investor/002230/interact/qa'

# 使用Selenium加载页面
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式运行，不打开浏览器窗口
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 初始化问答对列表
all_qa_pairs = []

# 分页参数
total_pages = 17  # 假设有17页

for page in range(1, total_pages + 1):
    print(f"Processing page {page}...")

    if page == 1:
        driver.get(base_url)
    else:
        try:
            # 等待并找到“下一页”按钮
            next_page_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-next[aria-label='下一页']"))
            )
            if next_page_button.is_enabled():  # 检查按钮是否可用
                next_page_button.click()
                time.sleep(3)  # 给页面加载时间，可以适当调整
            else:
                print("下一页按钮不可用，可能是最后一页。")
                break
        except Exception as e:
            print(f"无法找到或点击下一页按钮: {e}")
            break

    # 等待几秒钟让JavaScript完全加载
    time.sleep(5)  # 可以根据实际情况调整等待时间

    # 获取页面源码并解析HTML文档
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有问答对
    qa_pairs = []
    for item in soup.select('ul.list li'):
        question_div = item.select_one('div.q > div.t')
        question_date_div = item.select_one('div.q > div.date')
        answer_div = item.select_one('div.a > div.t')
        answer_date_div = item.select_one('div.a > div.date')

        if all([question_div, question_date_div, answer_div, answer_date_div]):
            qa_pairs.append({
                'question': question_div.get_text(strip=True),
                'question_date': question_date_div.get_text(strip=True),
                'answer': answer_div.get_text(strip=True),
                'answer_date': answer_date_div.get_text(strip=True)
            })

    all_qa_pairs.extend(qa_pairs)

    # 如果没有找到任何问答对，打印出所有的<li>标签进行调试
    if not qa_pairs:
        print(f"No QA pairs found on page {page}. Here are all <li> tags:")
        for item in soup.select('ul.list li'):
            print(item.prettify())

# 关闭浏览器
driver.quit()

# 将问答对保存到桌面的TXT文件
output_file_path = os.path.join(desktop, 'Q&A001.txt')
with open(output_file_path, 'w', encoding='utf-8') as file:
    for qa in all_qa_pairs:
        file.write(f"\n=== 问题 ===\n{qa['question']}\n{qa['question_date']}\n=== 回答 ===\n{qa['answer']}\n{qa['answer_date']}\n{'-'*40}\n")

print(f"Extracted {len(all_qa_pairs)} QA pairs and saved to {output_file_path}.")