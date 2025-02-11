# Advanced Web Scraper

这是一个高级 Python 爬虫项目，支持多线程抓取、自动分页处理和将数据存储到 SQLite 数据库。

## 依赖

- requests
- beautifulsoup4
- sqlite3

## 功能

- 多线程并发抓取，提升抓取效率
- 自动处理分页，抓取多页数据
- 数据存储到 SQLite 数据库

## 如何运行

1. 安装依赖：

```bash
pip install requests beautifulsoup4
```

2. 运行脚本：

```bash
python main.py
```

3. 输入基础网址、起始页码和结束页码，结果会存储到 `data.db` 数据库中。
