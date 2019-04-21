import scrapy
import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path


class Dblp(scrapy.Spider):
    name = "dblp_corpus_gen"
    scraping_folder_url = str(Path(os.path.abspath(
        __file__)).parent.parent.parent.parent.parent.resolve())

    file_paths = [
        scraping_folder_url+'/vishal/maryland_scraper/maryland/data/maryland_corpus.json',
        scraping_folder_url+'/vishal/stanford_scraper/stanford/data/stanford_corpus.json',
        scraping_folder_url+'/bala/data/mit_corpus.json',
        scraping_folder_url+'/bala/data/uiuc_corpus.json'
    ]

    final_json = {}

    def start_requests(self):
        for file_name in self.file_paths:
            self.final_json[file_name] = {}
            with open(file_name, "r") as f:
                total_data = json.loads(f.read())
                univ_name = file_name.split("/")[-1].strip("_corpus.json")
                for (_, obj) in total_data.items():
                    url = obj["corpus"]["DBLP"]
                    self.final_json[univ_name] = []

                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        meta={"univ_name": univ_name,
                              "corpus": obj["corpus"], "courses": obj["courses"]}
                    )

    def parse(self, response):
        # request_url = response.request.url

        download_xml_url = response.selector.xpath(
            "//header[@class='headline noline']/nav[@class='head']/ul/li[@class='export drop-down']/div[@class='body']/ul[1]/li[5]/a/@href").get()

        yield scrapy.Request(
            url=download_xml_url,
            callback=self.downloadXml,
            meta=response.meta
        )

    def downloadXml(self, response):
        root = ET.fromstring(response.body)
        papers_arr = []
        for some_ele in root.findall('r'):
            temp_paper_obj = {}
            if some_ele.tag == 'r':
                for child in some_ele:
                    temp_paper_obj["title"] = child.find("title").text
                    temp_url_val = child.find("ee")
                    temp_paper_obj["url"] = "" if temp_url_val is None else temp_url_val.text
                    co_authors = []
                    for author in child.findall("author"):
                        co_authors.append(author.text)
                    temp_paper_obj["co_authors"] = co_authors
                papers_arr.append(temp_paper_obj)

        temp = {
            "person": root.attrib['name'],
            "no_of_papers": root.attrib['n'],
            "univ_name": response.meta['univ_name'],
            "papers": papers_arr,
            "corpus": response.meta["corpus"],
            "courses": response.meta["courses"]
        }
        yield temp
