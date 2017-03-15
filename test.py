# scrapy runspider test.py -o out.csv

import scrapy
import re

class TestSpider(scrapy.Spider):
    name = 'testspider'

    def start_requests(self):
        urls = [
            'https://www.chemistwarehouse.com.au/Shop-Online/957/Baby-Formula',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for quote in response.css('div.Product'):
            yield {
                'text': quote.css('div.product-image img::attr(alt)').extract_first(),
                'price': quote.css('div.prices span.Price::text').extract_first(),
            }

        # loop through all pages
        next_page_url = response.css('div.pager-results a.next-page::attr(href)').extract_first()
        next_page = re.search(r'\?page=.*', next_page_url).group(0)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
