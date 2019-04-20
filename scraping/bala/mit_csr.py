import json
from requests_html import HTMLSession

session = HTMLSession()
url = "http://csrankings.org/#/index?ai&vision&mlmining&nlp&ir"

r = session.get(url)
r.html.render(wait=2,sleep=1)

mit_corpus = {}
for i in range(1,109,2):
    name = r.html.xpath('//*[@id="Massachusetts%20Institute%20of%20Technology-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/a[1]/text()')[0]
    print(name)
    if('0001' in name):
        name = name.strip(' 0001')
    last_name = name.split(' ')[-1]
    home = ''.join(r.html.xpath('//*[@id="Massachusetts%20Institute%20of%20Technology-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/a[2]/@href'))
    google_scholar = ''.join(r.html.xpath('//*[@id="Massachusetts%20Institute%20of%20Technology-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/a[3]/@href'))
    dblp = ''.join(r.html.xpath('//*[@id="Massachusetts%20Institute%20of%20Technology-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/a[4]/@href'))
    pub_count = ''.join(r.html.xpath('//*[@id="Massachusetts%20Institute%20of%20Technology-faculty"]/div/table/tbody/tr['+str(i)+']/td[3]/small/a/text()'))
    domain = ''.join(r.html.xpath('//*[@id="Massachusetts%20Institute%20of%20Technology-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/font/text()'))

    if('dblp' in google_scholar and 'scholar' not in google_scholar):
        dblp = google_scholar
        google_scholar = ""

    mit_corpus[name] = {'corpus':
                            {'Last name':last_name,'home':home, 'DBLP':dblp, 'Google Scholar':google_scholar,'domain':domain, 'Pub count':pub_count}
                        }

with open("mit_corpus_csr.json","w") as f:
    json.dump(mit_corpus,f, indent=2)

session.close()
