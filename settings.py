BOT_NAME = 'advanced_spider'

SPIDER_MODULES = ['advanced_spider.spiders']
NEWSPIDER_MODULE = 'advanced_spider.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 16

ITEM_PIPELINES = {
    'advanced_spider.pipelines.MySQLPipeline': 300,
    'advanced_spider.pipelines.CsvPipeline': 400,
}
