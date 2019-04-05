# -*- coding: utf-8 -*-
import os
import json
import scrapy


class CourseExplorerSpider(scrapy.Spider):
    name = 'course_explorer'
    allowed_domains = ['https://explorecourses.stanford.edu/print']

    def start_requests(self):
        corpus_file_path = "{}/stanford/data/stanford_corpus.json".format(os.getcwd())
        with open(corpus_file_path, "r") as file:
            self.global_dict = json.load(file)

        researcher_names = ["+".join(name.split()) for name in self.global_dict.keys()]
        urls = ["{}?q={}&descriptions=on&schedules=on".format(self.allowed_domains[0], name) for name in researcher_names]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        searchResults = response.selector.xpath("//div[@class='searchResult']")
        researcher_name = " ".join(response.selector.xpath("//td[@id='title']/h1").get().strip("<h1>").strip("</h1>").split()[2:])

        course_explorer_dict = {}
        course_explorer_dict.update({
            researcher_name: {
                "courses": []
            }
        })

        for index in range(len(searchResults)):
            courseTitle = searchResults[index].xpath("//span[@class='courseTitle']").get()
            courseNumber = searchResults[index].xpath("//span[@class='courseNumber']").get()
            courseDescription = searchResults[index].xpath("//div[@class='courseDescription']").get()
            courseAttributes = searchResults[index].xpath("//div[@class='courseAttributes'][1]").get()
            courseInstructors = searchResults[index].xpath("//div[@class='courseAttributes'][2]").get()
            course_explorer_dict[researcher_name]["courses"].append(
                {
                    "courseTitle": courseTitle,
                    "courseNumber": courseNumber,
                    "courseDescription": courseDescription,
                    "courseAttributes": courseAttributes,
                    "courseInstructors": courseInstructors
                }
            )

        yield course_explorer_dict

