import scrapy
from scrapy.crawler import CrawlerProcess
import os
from datetime import datetime
import re


class WendySpider(scrapy.Spider):
    name = 'wendy_spider'
    allowed_domains = ['locations.wendys.com']
    start_urls = ['https://locations.wendys.com/']

    def parse(self, response):
        # 提取网页中的所有文本
        all_text = ' '.join(response.xpath('/html/body/main//text()').getall())

        # 移除多余的空白字符
        clean_text = " ".join(all_text.split())

        # 计算文本中所有数字的总和
        numbers = re.findall(r'-?\d+\.?\d*', clean_text)
        total_sum = sum(map(float, numbers))

        # 将总和添加到文本最后
        result_text = f"{clean_text}\n\nTotal Sum of Numbers: {total_sum}"

        # 获取用户桌面路径
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

        # 创建 TEST 文件夹（如果不存在）
        test_folder = os.path.join(desktop_path, 'TEST')
        if not os.path.exists(test_folder):
            os.makedirs(test_folder)

        # 创建带有日期的新文件名
        filename = f'WENDY_{datetime.now().strftime("%Y%m%d")}.txt'
        full_path = os.path.join(test_folder, filename)

        # 将文本写入文件
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(result_text)

        self.log(f'Saved text to {full_path}')


# 运行爬虫
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WendySpider)
    process.start()