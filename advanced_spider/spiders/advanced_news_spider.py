import scrapy
from advanced_spider.items import NewsItem
from fake_useragent import UserAgent
import logging

class AdvancedNewsSpider(scrapy.Spider):
    name = 'advanced_news'
    allowed_domains = ['example-news.com']
    start_urls = ['https://www.example-news.com/news']
    
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': UserAgent().random
    }
    
    def parse(self, response):
        articles = response.xpath('//div[@class="article"]')
        logging.info(f"Found {len(articles)} articles on the page.")
        
        for article in articles:
            item = NewsItem()
            item['title'] = article.xpath('.//h2/a/text()').get().strip()
            item['url'] = article.xpath('.//h2/a/@href').get()
            if item['url']:
                yield scrapy.Request(
                    url=item['url'],
                    callback=self.parse_detail,
                    meta={'item': item},
                    headers={'User-Agent': UserAgent().random}
                )

    def parse_detail(self, response):
        item = response.meta['item']
        item['publish_date'] = response.xpath('//div[@class="publish-date"]/text()').get().strip()
        item['content'] = ' '.join(response.xpath('//div[@class="content"]//text()').getall()).strip()
        logging.info(f"Scraped article: {item['title']}")
        yield item
