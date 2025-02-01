from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from datetime import datetime

# 获取当前日期并格式化为 YYYYMMDD 格式
current_date = datetime.now().strftime('%Y%m%d')

# 设置输出文件夹路径为桌面上的 TEST 文件夹
output_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "TEST")

# 如果输出文件夹不存在，则创建它
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 设置输出文件路径为带有 CMG 和日期的文件名
output_file_name = f"CMG{current_date}.txt"
output_file_path = os.path.join(output_folder_path, output_file_name)

# 定义要访问的网站列表
websites = [
    'https://locations.chipotle.com/',
    'https://locations.chipotle.ca/',
    'https://locations.chipotle.co.uk/',
    'https://locations.chipotle.fr/',
    # 添加更多网站...
]

# 启动浏览器驱动（假设是Chrome）
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式，不打开浏览器窗口
driver = webdriver.Chrome(options=options)

def extract_data_from_website(url):
    try:
        print(f"Processing URL: {url}")
        driver.get(url)

        # 查找所有包含 data-count 属性的 a 标签
        elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-count]')

        # 打开输出文件准备追加写入
        with open(output_file_path, 'a', encoding='utf-8') as file:
            for element in elements:
                data_count = element.get_attribute('data-count')
                if data_count:
                    count = int(data_count.strip('()'))
                    file.write(f"{count}\n")  # 写入文件并换行

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

try:
    # 对于每一个网站，执行数据提取
    for website in websites:
        extract_data_from_website(website)

    # 计算总和
    total_sum = 0
    try:
        with open(output_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    number = int(line.strip())
                    total_sum += number
                except ValueError:
                    # 忽略非整数行
                    continue
    except FileNotFoundError:
        pass  # 如果文件未找到，直接跳过计算部分

    # 将总和追加到文件末尾
    with open(output_file_path, 'a', encoding='utf-8') as file:
        file.write(f"\nTotal Sum of All Numbers: {total_sum}\n")

finally:
    # 关闭浏览器
    driver.quit()

print(f"All data has been written to {output_file_path}, including the total sum.")