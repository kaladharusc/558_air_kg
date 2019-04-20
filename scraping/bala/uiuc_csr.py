import json
from requests_html import HTMLSession

session = HTMLSession()
url = "http://csrankings.org/#/index?ai&vision&mlmining&nlp&ir"

r = session.get(url)
r.html.render(wait=2,sleep=1)

uiuc_corpus = {}
for i in range(1,71,2):
    name = r.html.xpath('//*[@id="Univ.%20of%20Illinois%20at%20Urbana-Champaign-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/a[1]/text()')[0]
    print(name)
    if('0001' in name or '0044' in name or '0011' in name):
        name = name.strip(' 0001').strip(' 0044').strip(' 0011')
    last_name = name.split(' ')[-1]
    home = ''.join(r.html.xpath('//*[@id="Univ.%20of%20Illinois%20at%20Urbana-Champaign-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/a[2]/@href'))
    google_scholar = ''.join(r.html.xpath('//*[@id="Univ.%20of%20Illinois%20at%20Urbana-Champaign-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/a[3]/@href'))
    dblp = ''.join(r.html.xpath('//*[@id="Univ.%20of%20Illinois%20at%20Urbana-Champaign-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/a[4]/@href'))
    pub_count = ''.join(r.html.xpath('//*[@id="Univ.%20of%20Illinois%20at%20Urbana-Champaign-faculty"]/div/table/tbody/tr['+str(i)+']/td[3]/small/a/text()'))
    domain = ''.join(r.html.xpath('//*[@id="Univ.%20of%20Illinois%20at%20Urbana-Champaign-faculty"]/div/table/tbody/tr['+str(i)+']/td[2]/small/font/text()'))

    if('dblp' in google_scholar and 'scholar' not in google_scholar):
        dblp = google_scholar
        google_scholar = ""

    uiuc_corpus[name] = {'corpus':
                            {'Last name':last_name,'home':home, 'DBLP':dblp, 'Google Scholar':google_scholar,'domain':domain, 'Pub count':pub_count}
                        }

with open("uiuc_corpus_csr.json","w") as f:
    json.dump(uiuc_corpus,f, indent=2)

session.close()
