import rltk
import json
import pandas as pd
from collections import defaultdict
from pyjarowinkler import distance

class Record1(rltk.Record):
   @property
   def id(self):
      return self.raw_object['id']

   @property
   def fname(self):
      return self.raw_object['first_name']

   @property
   def lname(self):
      return self.raw_object['last_name']

class Record2(rltk.Record):
   @property
   def id(self):
      return self.raw_object['id']

   @property
   def fname(self):
      return self.raw_object['first_name']

   @property
   def lname(self):
      return self.raw_object['last_name']


def compare(s1,s2):
    return distance.get_jaro_distance(s1, s2, winkler=False, scaling=0.1)

def main():
    with open("dblp_final_JSON.json","r") as f:
        dblp_dict = json.load(f)

    professors = set()
    for key in dblp_dict:
        professors.add(key['person'])

    #print(professors)
    #print(len(professors))

    coauthor_dict = defaultdict(list)
    for key in dblp_dict:
        author = key['person']
        for items in key['papers']:
            co_authors = items['co_authors']
            if author in co_authors:
                co_authors.remove(author)
            if co_authors:
                coauthor_dict[author].extend(co_authors)

    list_of_coauthors = []
    for key in coauthor_dict:
        list_of_coauthors.extend(coauthor_dict[key])
    #print(len(list_of_coauthors))

    ### String / Data Matching for Entity linking using RLTK

    ### Remove duplicates in the coauthor_dict using String Matching
    ### Compare with professors and do entity linking / remove duplicates

    df1 = pd.DataFrame(list(professors),columns=['name'])
    #print(df1)
    df2 = pd.DataFrame(list_of_coauthors,columns=['name'])
    #print(len(df2))
    df1['first_name'] = df1.apply(lambda x: x['name'].split()[0], axis=1)
    df1['last_name'] = df1.apply(lambda x: ' '.join(x['name'].split()[1:]), axis=1)
    df1['id'] = (df1.index+1).astype(str)

    #print(df1)
    df2['first_name'] = df2.apply(lambda x: x['name'].split()[0], axis=1)
    df2['last_name'] = df2.apply(lambda x: ' '.join(x['name'].split()[1:]), axis=1)
    df2['id'] = (df2.index+1).astype(str)

    ds1 = rltk.Dataset(reader=rltk.DataFrameReader(df1),record_class=Record1, adapter=rltk.MemoryKeyValueAdapter())
    ds2 = rltk.Dataset(reader=rltk.DataFrameReader(df2),record_class=Record2, adapter=rltk.MemoryKeyValueAdapter())
    bg = rltk.HashBlockGenerator()
    block = bg.generate(bg.block(ds1, property_='fname'),bg.block(ds2, property_='fname'))
    pairs = rltk.get_record_pairs(ds1, ds2, block=block)
    num_pairs = 0
    sim_pairs = []
    sim_dict = {}
    for r1, r2 in pairs:
        num_pairs+=1
        sim = rltk.jaro_winkler_similarity(r1.lname, r2.lname)
        if 0.9<sim<1:
            sim_pairs.append((r1.fname+' '+r1.lname,r2.fname+' '+r2.lname))
            sim_dict[r1.fname+' '+r1.lname] = r2.fname+' '+r2.lname
            #print(r1.lname,r2.lname,sim)
    #print(sim_pairs)
    #print("Blocking using Cuisine - Number of pairs:",num_pairs)
    for key in coauthor_dict:
        lis = coauthor_dict[key]
        for ind in range(len(lis)):
            if lis[ind] in sim_dict:
                lis[ind] = sim_dict[lis[ind]]

    with open("co_authors.json","w") as jf:
        json.dump(coauthor_dict, jf, indent=2)

if __name__ == '__main__':
    main()
