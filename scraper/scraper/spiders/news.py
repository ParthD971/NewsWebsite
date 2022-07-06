import scrapy
from datetime import datetime, timedelta
from ..items import NewsPostItem


class NewsSpider(scrapy.Spider):
    name = "news"

    def __init__(self, category=None, **kwargs):
        self.category = category
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(f'https://indianexpress.com/section/{self.category}/page/1/', callback=self.parse)

    def parse(self, response, **kwargs):
        today_news_end = False
        for news in response.css('div.articles'):
            item = NewsPostItem()
            item['title'] = news.css('.title a::text').get()
            item['date'] = news.css('.date::text').get()
            item['href'] = news.css('.title a::attr(href)').get()
            print('\n\n\n ')
            print((datetime.now()).strftime('%B %-d'), item['date'].split(',')[0].strip())
            print('\n\n\n ')
            if item['date'].split(',')[0].strip() != datetime.now().strftime('%B %-d') \
                    and item['date'].split(',')[0].strip() != (datetime.now() - timedelta(hours=34)).strftime('%B %-d'):
            # if item['date'].split(',')[0].strip() != datetime.now().strftime('%B %d'):
                today_news_end = True
                break
            request = scrapy.http.Request(
                url=item['href'],
                callback=self.parse_details,
                meta={"item": item}
            )
            yield request

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None and not today_news_end:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        item = response.meta.get('item')
        item = NewsPostItem(item)

        lis_of_string = response.css(
            ''' #pcl-full-content>p::text, 
            #pcl-full-content>.ev-meter-content > p::text , 
            .custom-caption+ p::text , 
            .hlt-bot-text p~ p+ p::text , 
            .ev-meter-content .ev-meter-content p::text '''
        ).getall()
        content = '\n\n'.join(lis_of_string)
        image_url = response.css('.custom-caption img::attr(src)').getall()

        for url in image_url:
            if '.jpg' in url:
                image_url = url
                break
        else:
            image_url = image_url[:1]

        item['content'] = content
        item['image_url'] = image_url
        item['category'] = self.category

        yield item

