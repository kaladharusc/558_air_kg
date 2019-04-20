import json
from requests_html import HTMLSession
import time

def main():
    start_time = time.time()
    print("Start time:",start_time)
    with open("mit_corpus_csr.json","r") as f:
        mit_dict = json.load(f)

    search_list = []
    for item in mit_dict:
        search_list.append((item,mit_dict[item]['corpus']['Last name']))
        mit_dict[item]['courses'] = []

    #print(search_list)
    #print(len(search_list))

    for key,last_name in search_list:
        #print(key)
        query_url = 'http://student.mit.edu/catalog/search.cgi?search='+last_name+'&style=professor'

        try:
            session1 = HTMLSession()
            r1 = session1.get(query_url)
            r1.html.render(wait=2) #,sleep=1)
        except:
            session1.close()
            print("\nException occurred.\n")
            continue

        list_course_id = r1.html.xpath('//*[@id="contentcontainer"]/blockquote/h3/text()')
        course_tuple = []

        if(list_course_id):
            for item in list_course_id:
                course_tuple.append([item.split(' ')[0],' '.join(item.split(' ')[1:]).strip(),""])
        else:
            list_courses = r1.html.xpath('//*[@id="contentcontainer"]/blockquote/dl/dt/a/text()')
            list_desc = r1.html.xpath('//*[@id="contentcontainer"]/blockquote/dl/dd/text()')
            for item1,item2 in zip(list_courses,list_desc):
                course_tuple.append([item1.split(' ')[0],' '.join(item1.split(' ')[1:]).strip(),item2])

        if(course_tuple):
            for item in course_tuple:
                mit_dict[key]['courses'].append({"courseId":item[0],"courseLevel":"Graduate","courseMeta":item[-1],"courseTitle":item[1],"gradingMethod":"Regular","numberOfUnits":"","semester":""})

        session1.close()

    with open("mit_corpus.json","w") as f:
        json.dump(mit_dict,f, indent=2)

    print("Time taken:",time.time() - start_time)

if __name__ == '__main__':
    main()
