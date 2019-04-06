import os
import json

class Aggregator():

    def __init__(self):
        self.data_directory = os.path.join(os.getcwd(), "scraping", "vishal", "\
maryland_scraper", "maryland", "data")
        self.load_object()
        self.load_course_explorer()
        self.aggregate()
        self.save_to_file()

    def load_object(self):
        with open(os.path.join(self.data_directory, "maryland_corpus_without_co\
urses.json"), "r") as fp:
            self.object = json.load(fp)
        self.reverse_dict = {}
        for key, value in self.object.items():
            self.reverse_dict.update({value["query_param"]: key})

    def load_course_explorer(self):
        self.course_explorer = {}
        with open(os.path.join(self.data_directory, "maryland_course_explorer_d\
ata.json"), "r") as fp: 
            for line in fp.readlines():
                researcher_dict = json.loads(line)

                r = list(researcher_dict.keys())[0]
                semester = researcher_dict.get(r).get("semester")
                course_level = researcher_dict.get(r).get("course_level")
                c = researcher_dict.get(r).get("courses")
                if not self.course_explorer.get(r):
                    self.course_explorer.update({r: {"courses": []}})
                if c:
                    for index in range(len(c)):
                        c[index].update({"semester": semester, "courseLevel": \
                            course_level})
                    self.course_explorer[r]["courses"].extend(c)

    def aggregate(self):
        self.output_path = os.path.join(self.data_directory, "maryland_data.jso\
n")
        for researcher, course_dict in self.course_explorer.items():
            course_array = course_dict["courses"]
            researcher = self.reverse_dict.get("%2C+".join(researcher.split(", \
")))
            if not self.object[researcher].get("courses"):
                self.object[researcher].update({"courses":[]})

            if course_array:
                for course in course_array:
                    courseId = course.get("course_id")
                    courseTitle = course.get("course_title")
                    courseLevel = course.get("course_level")
                    courseMeta = course.get("course_prereqs")
                    gradingMethod = course.get("course_grading_method")
                    semester = course.get("semester")
                    numberOfUnits = course.get("course_credits")
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

    def save_to_file(self):
        with open("{}/maryland_corpus.json".format(self.data_directory), "w") \
            as file:
            json.dump(self.object, file, ensure_ascii=False, sort_keys=True,\
                 indent=4, separators=(',', ': '))       


if __name__ == "__main__":
    obj = Aggregator()