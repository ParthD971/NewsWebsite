import scrapy


class NewsPostItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    href = scrapy.Field()
    content = scrapy.Field()
    image_url = scrapy.Field()
    category = scrapy.Field()
