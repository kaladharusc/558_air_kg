import os
import json
import scrapy
import lxml

class CourseExplorerSpider(scrapy.Spider):
    name = 'course_explorer'
    allowed_domains = ['https://app.testudo.umd.edu/soc/search?']
    start_urls = [] 
    semesters = {
        '201908': 'Fall',
        '201812': 'Winter',
        '201901': 'Spring',
        '201905': 'Summer'
    }
    course_level_filter = ['GRAD', 'UGRAD']

    def format_url(self, researcher_name):
        url_string1 = "https://app.testudo.umd.edu/soc/search?courseId=&section\
Id=&termId="
        url_string2 = "&_openSectionsOnly=on&creditCompare=&credits=&courseLeve\
lFilter="
        url_string3 = "&instructor="
        url_string4 = "&_facetoface=on&_blended=on&_online=on&courseStartCompar\
e=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&c\
ourseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDa\
y2=on&_classDay3=on_classDay4=on&_classDay5=on"

        for semester in self.semesters.keys():
            for course_level in self.course_level_filter:
                url = "{0}{1}{2}{3}{4}{5}{6}".format(url_string1, semester, \
                    url_string2, course_level, url_string3, researcher_name, \
                        url_string4)
                self.start_urls.append(url)

    def start_requests(self):

        corpus_file_path = "{}/maryland/data/maryland_corpus.json".format(\
            os.getcwd())

        with open(corpus_file_path, "r") as file:
            self.global_dict = json.load(file)

        researcher_names = [value.get("query_param") for value in \
            self.global_dict.values()]

        for r in researcher_names:
            self.format_url(r)

        for url in self.start_urls:
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        researcher_name = response.selector.xpath('//input[@id="instructor-inpu\
t"]/@value').get()
        searchResults = response.selector.xpath('//div[@class="course-prefix-co\
ntainer"]')
        course_level = response.selector.xpath('//input[@type="radio" and @chec\
ked="checked"]/@value').get()
        print(course_level)
        semester = self.semesters.get(response.selector.xpath('//select[@id="te\
rm-id-input"]/option[@selected="selected"]/@value').get())
        course_explorer_dict = {}
        course_explorer_dict.update({
            researcher_name: {
                "semester": semester,
                "course_level": course_level,
                "courses": [],
                "number_of_courses": len(searchResults)
            }
        })
        if len(searchResults):
            for course in searchResults:
                course = lxml.html.fromstring(course.extract())
                course_id = course.xpath("//div[@class='course-id']/text()")
                course_id = course_id[0] if len(course_id) else ""
                course_title = course.xpath("//span[@class='course-title']/text()")
                course_title = course_title[0] if len(course_title) else ""
                course_prereqs = course.xpath("//div[@class='course-text']/text()")
                course_prereqs = course_prereqs[0] if len(course_prereqs) else ""
                course_credits = course.xpath('//span[@class="course-min-credits"]/text()')
                course_credits = course_credits[0] if len(course_credits) else ""
                course_grading_method = course.xpath("//div/span[@class='grading-method']/abbr/@title")
                course_grading_method = course_grading_method[0] if len(course_grading_method) else ""
                course_explorer_dict[researcher_name]["courses"].append({
                    "course_id": course_id,
                    "course_title": course_title,
                    "course_prereqs": course_prereqs,
                    "course_credits": course_credits,
                    "course_grading_method": course_grading_method
                })

        yield course_explorer_dict

