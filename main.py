import asyncio
from scraper import Scraper
from db import Database

async def main():
    print("欢迎使用 Complex Web Scraper")
    base_url = input("请输入要抓取的基础网址（例如：https://example.com/list）: ")
    start_page = int(input("请输入起始页码: "))
    end_page = int(input("请输入结束页码: "))

    db = Database("data.db")
    scraper = Scraper(base_url, start_page, end_page, db)

    await scraper.run()
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
  import aiohttp
import asyncio
import random
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, base_url, start_page, end_page, db):
        self.base_url = base_url
        self.start_page = start_page
        self.end_page = end_page
        self.db = db

    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            print(f"请求失败: {url}, 错误: {e}")
            return None

    async def scrape_page(self, session, page_num):
        url = f"{self.base_url}?page={page_num}"
        print(f"开始抓取: {url}")
        html = await self.fetch(session, url)
        if html:
            self.parse_and_store(html)

    def parse_and_store(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('a'):
            title = item.get_text(strip=True)
            link = item.get('href')
            if title and link:
                self.db.insert_data(title, link)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page_num in range(self.start_page, self.end_page + 1):
                tasks.append(self.scrape_page(session, page_num))
                await asyncio.sleep(random.uniform(1, 3))  # 随机延迟，防止被封
            await asyncio.gather(*tasks)
        print("抓取完成，结果已存储到数据库。")
      import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.init_db()

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                link TEXT
            )
        ''')
        self.conn.commit()

    def insert_data(self, title, link):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO scraped_data (title, link) VALUES (?, ?)", (title, link))
        self.conn.commit()

    def close(self):
        self.conn.close()
