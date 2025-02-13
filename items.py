import scrapy

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    publish_date = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
