import requests
from bs4 import BeautifulSoup
import csv
import random
import time
import os
from fake_useragent import UserAgent
from requests.exceptions import RequestException

# 设置 User-Agent 来模拟不同浏览器的请求
ua = UserAgent()

# 获取代理池
def get_proxies():
    return {
        "http": "http://123.123.123.123:8888", 
        "https": "https://123.123.123.123:8888"
    }

# 发送请求并获取页面内容
def fetch_page(url, retries=3):
    headers = {
        "User-Agent": ua.random
    }
    proxies = get_proxies()
    
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"请求失败: {e}")
            time.sleep(random.randint(2, 5))
    return None

# 解析页面内容
def parse_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    data = []
    
    # 假设页面中有多个条目，每个条目有一个标题和链接
    for item in soup.find_all('div', class_='item'):
        title = item.find('h2').get_text() if item.find('h2') else '无标题'
        link = item.find('a')['href'] if item.find('a') else '无链接'
        data.append([title, link])
    
    return data

# 保存数据到CSV
def save_to_csv(data, filename='output.csv'):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['标题', '链接'])  # CSV标题
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

# 主程序
def main(url, num_pages=5):
    for page_num in range(1, num_pages + 1):
        print(f"开始爬取第{page_num}页...")
        page_url = f"{url}?page={page_num}"
        page_content = fetch_page(page_url)
        
        if page_content:
            data = parse_page(page_content)
            save_to_csv(data)
            print(f"第{page_num}页数据爬取完毕，已保存到CSV文件")
        else:
            print(f"第{page_num}页请求失败，跳过该页")
        time.sleep(random.randint(2, 5))  # 随机休眠，防止过于频繁的请求

if __name__ == '__main__':
    url = "https://example.com/items"  # 目标URL
    main(url)
