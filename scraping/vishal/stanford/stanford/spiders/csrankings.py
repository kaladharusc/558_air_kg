# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class CsrankingsSpider(scrapy.Spider):
    name = 'csrankings'
    allowed_domains = ['csrankings.org']
    # start_urls = ['http://csrankings.org/#/index?all']

    def start_requests(self):
        yield SplashRequest(
            url = "http://csrankings.org/#/index?all",
            callback=self.parse
        )

    def parse(self, response):
        print(response.selector.xpath("//div[@id='Stanford%20University-faculty']/div[@class='table']/table[@class='table table-sm table-striped']/tbody/tr/td/small/a[position() > 1]/@href"))