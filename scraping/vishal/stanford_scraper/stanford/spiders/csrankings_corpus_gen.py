# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json
import os

class CsrankingsSpider(scrapy.Spider):
    name = 'csrankings_corpus_gen'
    allowed_domains = ['csrankings.org']
    global_dict = {}

    def formatResearcherNames(self, s):
        s = s.replace("é", "e")
        replace_name_dict = {
            "Alexander Aiken" : "Alex Aiken",
            "Christoforos E. Kozyrakis": "Christos Kozyrakis",
            "William J. Dally": "Bill dally"
        }
        if s in replace_name_dict.keys():
            s = replace_name_dict.get(s)
        
        return s

    def start_requests(self):
        yield SplashRequest(
            url = "http://csrankings.org/#/index?ai&vision&mlmining&nlp&ir",
            callback=self.parse
        )

    def parse(self, response):
        researchers = response.selector.xpath("//div[@id='Stanford%20University-faculty']/div[@class='table']/table[@class='table table-sm table-striped']/tbody/tr/td[2]/small/a/text()") 
        for index, researcher in enumerate(researchers):
            corpus_type = response.selector.xpath("//div[@id='Stanford%20University-faculty']/div[@class='table']/table[@class='table table-sm table-striped']/tbody/tr[{}]/td//a[position() > 1]/@title".format(index*2 + 1))
            corpus =  response.selector.xpath("//div[@id='Stanford%20University-faculty']/div[@class='table']/table[@class='table table-sm table-striped']/tbody/tr[{}]/td//a[position() > 1]/@href".format(index*2 + 1))
            corpus_dict = dict([(" ".join(key.get().split()[3:-1]), value.get()) for key, value in zip(corpus_type, corpus)])
            corpus_dict.update({"domain": response.selector.xpath("//div[@id='University%20of%20Maryland%20-%20College%20Park-faculty']/div[@class='table']/table[@class='table table-sm table-striped']/tbody/tr[{}]/td[2]/small/font/text()".format(index*2 + 1)).get() or ""})
            self.global_dict.update({
                self.formatResearcherNames(researcher.get()): {
                    "corpus": corpus_dict
                }
            })

        with open("{}/stanford/data/stanford_corpus_without_courses.json".format(os.getcwd()), "w") as file:
            json.dump(self.global_dict, file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

    def parse_details(self, response):
        pass