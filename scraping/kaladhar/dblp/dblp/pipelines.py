# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os


class DblpPipeline(object):
    def open_spider(self, spider):
        self.file = open(
            "{}/dblp/data/dblp_final.json".format(os.getcwd()), "w")

    def process_item(self, item, spider):
        print("Writing to file")
        print("\n")
        print("\n")
        print("\n")

        line=json.dumps(item, ensure_ascii=False) + "\n"
        self.file.write(line)
        # return item

    def close_spider(self, spider):
        self.file.close()
