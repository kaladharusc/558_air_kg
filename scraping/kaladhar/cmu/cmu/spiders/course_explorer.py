import scrapy


class CourseExplorerSpider(scrapy.Spider):
    name = 'course_explorer'
    allowed_domains = []