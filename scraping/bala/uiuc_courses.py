import json
from requests_html import HTMLSession
import time

def main():
    start_time = time.time()
    print("Start time:",start_time)
    with open("uiuc_corpus_csr.json","r") as f:
        uiuc_dict = json.load(f)

    terms = ['spring','summer','fall','winter']
    search_list = []

    for item in uiuc_dict:
        search_list.append((item,uiuc_dict[item]['corpus']['Last name']))
        uiuc_dict[item]['courses'] = []

    #print(search_list)
    #print(len(search_list))

    for key,last_name in search_list:
        for term in terms:
            #print(last_name,term)
            query_url = 'https://courses.illinois.edu/search?year=2019&term='+term+'&keyword=&keywordType=qs&instructor='+last_name+'&collegeCode=KP&subjectCode=&creditHour=&degreeAtt=&courseLevel=&genedCode1=&genedCode2=&genedCode3=&genedType=all&partOfTerm=&_online=on&_nonOnline=on&_open=on&_evenings=on'

            try:
                session1 = HTMLSession()
                r1 = session1.get(query_url)
                r1.html.render(wait=1) #,sleep=1)
            except:
                session1.close()
                print("\nException occurred.\n")
                continue
            list_course_id = r1.html.xpath('//td[4]/text()')
            list_course_term = r1.html.xpath('//td[3]/text()')
            list_course_name = r1.html.xpath('//td[5]/a/text()')
            list_course_link = r1.html.xpath('//td[5]/a/@href')

            course_tuple = []
            for id,term,name,link in zip(list_course_id,list_course_term,list_course_name,list_course_link):
                course_tuple.append([id,term,name.strip(),link])

            for itr in range(len(course_tuple)):
                course_url = 'https://courses.illinois.edu' + course_tuple[itr][3]
                try:
                    session2 = HTMLSession()
                    r2 = session2.get(course_url)
                    r2.html.render(wait=1) #,sleep=1)
                except:
                    session2.close()
                    print("\nException occurred.\n")
                    course_tuple[itr].append("")
                    course_tuple[itr].append("")
                    continue
                credits = ''.join(r2.html.xpath('//*[@id="app-course-info"]/div[2]/p[1]/text()'))
                meta1 = ''.join(r2.html.xpath('//*[@id="app-course-info"]/div[2]/p[2]/text()'))
                meta2 = ''.join(r2.html.xpath('//*[@id="app-course-info"]/div[2]/p[3]/text()'))
                meta = meta1 + meta2
                course_tuple[itr].append(credits)
                course_tuple[itr].append(meta)

            if(course_tuple):
                for item in course_tuple:
                    uiuc_dict[key]['courses'].append({"courseId":item[0],"courseLevel":"Graduate","courseMeta":item[-1],"courseTitle":item[2],"gradingMethod":"Regular","numberOfUnits":item[-2],"semester":item[1]})

            session1.close()
            session2.close()

    with open("uiuc_corpus.json","w") as f:
        json.dump(uiuc_dict,f, indent=2)

    print("Time taken:",time.time() - start_time)

if __name__ == '__main__':
    main()
