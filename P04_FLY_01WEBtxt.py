from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# 获取当前用户的桌面路径
desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

# 设置Chrome选项
options = webdriver.ChromeOptions()
# 如果不想看到浏览器窗口，可以取消下面这行的注释
# options.add_argument('--headless')  # 无头模式运行

# 初始化WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

try:
    # 访问目标网站 (替换为实际要抓取的网站URL)
    driver.get('http://aicc.iflytek.com/')  # 替换为你要抓取的网站URL

    # 等待页面完全加载，这里简单地等待5秒，实际情况可能需要更智能的等待方式
    time.sleep(5)  # 这里建议使用显式等待或者直到条件满足的等待方法

    # 获取所有<a>标签中的href属性值
    links = [link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME, 'a')]

    # 去除空链接或无效链接
    links = [link for link in links if link and not link.startswith('javascript:')]

    # 定义输出文件路径
    output_file = os.path.join(desktop_path, 'TEST004.txt')

    # 将链接写入桌面的TXT文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(f'{link}\n')

    print(f"Links have been saved to {output_file}")

finally:
    # 关闭浏览器
    driver.quit()