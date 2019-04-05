import os
import json
import scrapy

class CourseExplorerSpider(scrapy.Spider):
    name = 'course_explorer'
    allowed_domains = ['https://app.testudo.umd.edu/soc/search?']
    start_urls = [] 
    semesters = {
        '201812': 'Winter',
        '201901': 'Spring',
        '201905': 'Summer',
        '201908': 'Fall'
    }

    def format_name(self, unformatted_name_array):
        reversed_name_array = [unformatted_name_array[-1], \
            unformatted_name_array[0]]
        return_string = "%2C+".join(reversed_name_array)
        return return_string

    def format_url(self, researcher_name):
        url_string1 = "https://app.testudo.umd.edu/soc/search?courseId=&section\
Id=&termId="
        url_string2 = "&_openSectionsOnly=on&creditCompare=&credits=&courseLeve\
lFilter=ALL&instructor="
        url_string3 = "&_facetoface=on&_blended=on&_online=on&courseStartCompar\
e=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&c\
ourseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDa\
y2=on&_classDay3=on_classDay4=on&_classDay5=on"

        for semester in self.semesters.keys():
            url = "{}{}{}{}{}".format(url_string1, semester, \
                url_string2, researcher_name, url_string3)
            self.start_urls.append(url)

    def start_requests(self):

        corpus_file_path = "{}/maryland/data/maryland_corpus.json".format(\
            os.getcwd())

        with open(corpus_file_path, "r") as file:
            self.global_dict = json.load(file)

        researcher_names = [self.format_name(name.split()) for name in \
            self.global_dict.keys()]

        for r in researcher_names:
            self.format_url(r)

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
            break

    def parse(self, response):
        searchResults = reponse.selector.xpath('//div[@class="course-prefix-container"]')
