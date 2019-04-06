# -*- coding: utf-8 -*-
import os
import json
import scrapy
import re

class CourseExplorerSpider(scrapy.Spider):
    name = 'course_explorer'
    allowed_domains = ['https://explorecourses.stanford.edu/print']
    academic_levels = {
        "GR": "Graduate",
        "UG": "Undergraduate"
    }

    def start_requests(self):
        corpus_file_path = "{}/stanford/data/stanford_corpus_without_courses.js\
on".format(os.getcwd())
        with open(corpus_file_path, "r") as file:
            self.global_dict = json.load(file)

        researcher_names = ["+".join(name.split()) for name in \
            self.global_dict.keys()]
        urls = ["{}?q={}&descriptions=on&academicYear=&filter-academiclevel-{}=\
on&page=0&filter-coursestatus-Active=on&collapse=%2c7%2c&catalog=".format(\
            self.allowed_domains[0], name, academic_level) for name in \
            researcher_names for academic_level in self.academic_levels.keys()]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        request_url = response.request.url
        academic_level = self.academic_levels.get(re.findall(r"academiclevel-([\
A-Z]+)=", request_url)[0])
        searchResults = response.selector.xpath("//div[@class='searchResult']")
#         researcher_name = " ".join(response.selector.xpath("//td[@id='title']/h\
# 1").get().strip("<h1>").strip("</h1>").split()[2:])
        researcher_name = " ".join(re.findall("\?q=(.*)&descriptions", request_url)[0].split("+"))

        course_explorer_dict = {}
        course_explorer_dict.update({
            researcher_name: {
                "courses": []
            }
        })

        for index in range(len(searchResults)):
            courseTitle = searchResults[index].xpath("//span[@class='courseTitle']/text()").get()
            courseNumber = searchResults[index].xpath("//span[@class='courseNumber']/text()").get()
            courseDescription = searchResults[index].xpath("//div[@class='courseDescription']/text()").get()
            courseAttributes = " ".join(searchResults[index].xpath("//div[@class='courseAttributes'][1]/text()").get().split())
            # courseInstructors = searchResults[index].xpath("//div[@class='courseAttributes'][2]").get()
            course_explorer_dict[researcher_name]["courses"].append(
                {
                    "courseTitle": courseTitle,
                    "courseNumber": courseNumber,
                    "courseDescription": courseDescription,
                    "courseAttributes": courseAttributes,
                    "courseLevel": academic_level
                    # "courseInstructors": courseInstructors
                }
            )

        yield course_explorer_dict

