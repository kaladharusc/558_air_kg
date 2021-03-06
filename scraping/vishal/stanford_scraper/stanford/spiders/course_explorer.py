# -*- coding: utf-8 -*-
import os
import json
import scrapy
import re
import lxml

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
        print(researcher_names)
        exit
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
        researcher_name = " ".join(re.findall("\?q=(.*)&descriptions", \
            request_url)[0].split("+"))
        course_explorer_dict = {}
        course_explorer_dict.update({
            researcher_name: {
                "courses": []
            }
        })

        for result in searchResults:
            result = lxml.html.fromstring(result.get())
            courseTitle = result.xpath("//span[@class='courseTitle']/text()")
            courseTitle = courseTitle[0] if len(courseTitle) else ""
            courseNumber = result.xpath("//span[@class='courseNumber']/text()")
            courseNumber = courseNumber[0] if len(courseNumber) else ""
            courseDescription = result.xpath("//div[@class='courseDescription']\
/text()")
            courseDescription = courseDescription[0] if len(courseDescription) \
                else ""
            courseAttributes = " ".join(result.xpath("//div[@class='courseAttri\
butes'][1]/text()")[0].split())
            # courseInstructors = searchResults[index].xpath("//div[@class='cou\
            # rseAttributes'][2]").get()
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

