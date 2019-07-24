# -*- coding: utf-8 -*-
import scrapy
from rdc_travel_talking.items import RdcTravelTalkingItem


class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['you.ctrip.com']
    start_urls = ['https://you.ctrip.com/fooditem/guangzhou152/s0-p1.html',
                  'https://you.ctrip.com/fooditem/guangzhou152/s0-p2.html'
                  ]
    base_url = 'https://you.ctrip.com/fooditem/guangzhou152/{}.html'
    id = 0

    def parse(self, response):
        data_id = response.xpath('.//div[contains(@class,"foodlist")]/@data-id').extract()
        for i in range(len(data_id)):
            url = self.base_url.format(data_id[i])
            yield scrapy.Request(url=url,callback=self.food_parse)


    def food_parse(self,response):
        item = RdcTravelTalkingItem()
        item['id'] = self.id
        item['preview'] = response.xpath('.//div[@class="item active"]//img/@src').extract_first()
        item['title'] = response.xpath('.//li[@class="title ellipsis"]/text()').extract_first()
        item['content'] = response.xpath('.//li[@class="infotext"]/text()').extract_first().strip()
        self.id += 1
        yield item