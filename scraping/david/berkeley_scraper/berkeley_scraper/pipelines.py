# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json

class BerkeleyScraperPipeline(object):
    def open_spider(self, spider):
        self.file = open("{}/berkeley_scraper/data/berkeley_course_explorer_data.json".\
            format(os.getcwd()), "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


    # def process_item(self, item, spider):
        # return item
