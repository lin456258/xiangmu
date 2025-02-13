import pymysql
import pandas as pd

class MySQLPipeline:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='news_db',
            charset='utf8mb4'
        )
        self.cursor = self.connection.cursor()
    
    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO news (title, publish_date, content, url)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (
            item['title'],
            item['publish_date'],
            item['content'],
            item['url']
        ))
        self.connection.commit()
        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

class CsvPipeline:
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.data)
        df.to_csv('news_data.csv', index=False, encoding='utf-8')
