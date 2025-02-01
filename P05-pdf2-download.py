import os
import requests

# 定义文件路径和目标文件夹路径
pdf_links_file = r"C:\Users\Piers\Desktop\PDF.txt"
target_folder = r"C:\Users\Piers\Desktop\I-announce"

# 如果目标文件夹不存在，则创建它
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 读取PDF链接文件
with open(pdf_links_file, 'r') as file:
    pdf_links = file.readlines()

# 下载每个PDF文件
for link in pdf_links:
    link = link.strip()  # 去除链接末尾的换行符等空白字符
    if not link:  # 跳过空行
        continue

    try:
        response = requests.get(link)
        response.raise_for_status()  # 检查请求是否成功

        # 提取PDF文件名
        pdf_filename = os.path.basename(link)
        save_path = os.path.join(target_folder, pdf_filename)

        # 将PDF内容写入文件
        with open(save_path, 'wb') as pdf_file:
            pdf_file.write(response.content)

        print(f"Downloaded {pdf_filename} to {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {link}: {e}")

print("All PDF downloads completed.")