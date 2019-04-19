import os
import json
import scrapy
import lxml

class CourseExplorerSpider(scrapy.Spider):
    name = 'course_explorer'
    allowed_domains = ['https://classes.berkeley.edu/search/class/']
    start_urls = [] 
    semesters = {
        '3A851': 'Fall 2019',
        '3A831': 'Spring 2019',
        '3A789': 'Fall 2018',
        '3A770': 'Spring 2018',
        '3A618': 'Fall 2017',
        '3A582': 'Spring 2017',
        '3A589': 'Fall 2016'
        
    }
    # &f%5B2%5D=ts_course_level%3Agrad
    course_level_filter = ['Agrad', 'Aup', 'Alow'] #GRAD vs Undergrad

    def format_url(self, researcher_name):
        print(researcher_name)
        splitter = researcher_name.split()
        print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
        print(splitter)
        if len(splitter) == 2:
            researcher_formatted = splitter[0] + "%20%20" + splitter[1]
        else:
            researcher_formatted = splitter[0] + "%20" + splitter[1] + "%20" \
+ splitter[2]
        url_string1 = "https://classes.berkeley.edu/search/class/?f%5B0%5D=sm_instructors%3A"
        #Alexandre%20M.%20Bayen
        url_string2 = "&f%5B1%5D=im_field_term_name%"
        #3A851
        url_string3 = "&f%5B2%5D=ts_course_level%3"
        #Agrad

        for semester in self.semesters.keys():
            for course_level in self.course_level_filter:
                url = "{0}{1}{2}{3}{4}{5}".format(url_string1, researcher_formatted, \
                    url_string2, semester, url_string3, course_level)
                self.start_urls.append(url)

    def start_requests(self):

        corpus_file_path = "{}/berkeley_scraper/data/berkeley_corpus_without_courses.js\
on".format(os.getcwd())

        with open(corpus_file_path, "r") as file:
            self.global_dict = json.load(file)

        researcher_names = []
        for key in self.global_dict.keys():
            researcher_names.append(key)

        for r in researcher_names:
            self.format_url(r)

        for url in self.start_urls:
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        researcher_name = response.selector.xpath('/html/body/div/div[2]/main\
/div/ol/li[1]/div/div/div[1]/div[1]/div[1]/div[3]/span[2]').get()
        searchResults = response.selector.xpath('/html/body/div/div[2]/main\
/div/ol/li/div/div')
        course_level = response.selector.xpath('//*[@id="facetapi-facet-\
apachesolrsolr-block-ts-course-level"]/li[input/@checked="checked"]/text()').get()
        semester = self.semesters.get(response.selector.xpath('//*[@id="facet\
api-facet-apachesolrsolr-block-im-field-term-name"]/li[input/@checked="checked"]/text()').get())
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
                course_id = course.xpath("/html/body/div/div[2]/main/div/ol/li\
//div[span/text()='Class #:']/text()")
                course_id = course_id[0] if len(course_id) else ""
                course_title = course.xpath("/html/body/div/div[2]/main/div/ol/li//h2/text()")
                course_title = course_title[0] if len(course_title) else ""
                #course_prereqs = course.xpath("//div[@class='course-text']/text()")
                #course_prereqs = course_prereqs[0] if len(course_prereqs) else ""
                course_credits = course.xpath("/html/body/div/div[2]/main/div\
/ol/li//div[span/text()='Units:']/text()")
                course_credits = course_credits[0] if len(course_credits) else ""
                #course_grading_method = course.xpath("//div/span[@class='grading-method']/abbr/@title")
                #course_grading_method = course_grading_method[0] if len(course_grading_method) else ""
                course_explorer_dict[researcher_name]["courses"].append({
                    "course_id": course_id,
                    "course_title": course_title,
                    #"course_prereqs": course_prereqs,
                    "course_credits": course_credits
                    #"course_grading_method": course_grading_method
                })

        yield course_explorer_dict
