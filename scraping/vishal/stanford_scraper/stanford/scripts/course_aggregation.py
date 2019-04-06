import os
import json

class Aggregator():
    def __init__(self):
        self.data_directory = os.path.join(os.getcwd(), "scraping", "vishal", "\
stanford_scraper", "stanford", "data")
        self.load_object()
        self.load_course_explorer()
        self.aggregate()
        print(self.object)

    def load_object(self):
        with open(os.path.join(self.data_directory, "stanford_corpus_without_co\
urses.json"), "r") as fp:
            self.object = json.load(fp)

    def load_course_explorer(self):
        self.course_explorer = {}
        with open(os.path.join(self.data_directory, "stanford_course_explorer_d\
ata.json"), "r") as fp: 
            for line in fp.readlines():
                self.course_explorer.update(json.loads(line))

        # print(self.course_explorer.keys())

    def aggregate(self):
        self.output_path = os.path.join(self.data_directory, "stanford_data.jso\
n")
        for researcher, course_dict in self.course_explorer.items():
            course_array = course_dict["courses"]
            researcher = researcher.decode("utf-8")
            if not self.object[researcher].get("courses"):
                self.object[researcher].update({"courses":[]})

            if course_array:
                for course in course_array:
                    courseId = course.get("courseNumber")
                    courseTitle = course.get("courseTitle")
                    courseLevel = course.get("courseLevel")
                    courseMeta = course.get("courseDescription")
                    courseAttribsDict = {}
                    for attrib in course.get("courseAttributes").split("|\
"):
                        attrib = attrib.strip()
                        attrib = [i.strip() for i in attrib.split(":")]
                        if len(attrib) == 2:
                            courseAttribsDict.update({attrib[0]: attrib[1]})
                    gradingMethod = courseAttribsDict.get("Grading")
                    semester = courseAttribsDict.get("Terms")
                    numberOfUnits = courseAttribsDict.get("Units")
                    course_obj = {\
                        "courseId": courseId,\
                        "courseTitle": courseTitle,\
                        "courseLevel": courseLevel,\
                        "courseMeta": courseMeta,\
                        "gradingMethod": gradingMethod,\
                        "semester": semester,\
                        "numberOfUnits": numberOfUnits,\
                        }
                    self.object[researcher]["courses"].append(course_obj)

if __name__ == "__main__":
    obj = Aggregator()
