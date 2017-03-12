import sqlite3
from bs4 import BeautifulSoup
import json
import pprint
import time
import pyisbn

## Reads the database that has book description then output to json
con = sqlite3.connect('reviews_az.sqlite')
con.text_factory = str
cur = con.cursor()
cur.execute('select * from ReviewsTable')
results1 = cur.fetchall()
cur.close()

## descriptions_dicts must be initalized to [] at the top since append propagate through
start = time.time()
description_tup = []
descriptions_dicts = []
for row in results1:
    description = ""
    description_tup.append(description)
    descriptions_dict = dict()
    descriptions_dict["description"] = description
    descriptions_dict["isbn"] = row[0]
    descriptions_dicts.append(descriptions_dict)
        
print "total rows read {}".format(len(results1))
print "len reviews_tup {}".format(len(description_tup))
print "time took to process: {}".format(time.time()-start)



con = sqlite3.connect('reviews_gr.sqlite')
con.text_factory = str
cur = con.cursor()
cur.execute('select * from ReviewsTable')
results1 = cur.fetchall()
cur.close()

start = time.time()
description_tup = []
for row in results1:
    description = row[4]
    if not description:
        description = ""
    else:
        soup = BeautifulSoup(description,'html.parser')
        description = ''.join(soup.findAll(text=True))
        description = description.strip()

    description_tup.append(description)
    descriptions_dict = dict()
    descriptions_dict["description"] = description
    descriptions_dict["isbn"] = row[0]
    descriptions_dicts.append(descriptions_dict)


        
print "total rows read {}".format(len(results1))
print "len reviews_tup {}".format(len(description_tup))
print "time took to process: {}".format(time.time()-start)
        
con = sqlite3.connect('reviews_gr_2.sqlite')
con.text_factory = str
cur = con.cursor()
cur.execute('select * from ReviewsTable')
results1 = cur.fetchall()
cur.close()

start = time.time()
description_tup = []
for row in results1:
    description = row[4]
    if not description:
        description = ""
    else:
        soup = BeautifulSoup(description,'html.parser')
        description = ''.join(soup.findAll(text=True))
        description = description.strip()

    description_tup.append(description)
    descriptions_dict = dict()
    descriptions_dict["description"] = description
    descriptions_dict["isbn"] = row[0]
    descriptions_dicts.append(descriptions_dict)
        
print "total rows read {}".format(len(results1))
print "len reviews_tup {}".format(len(description_tup))
print "time took to process: {}".format(time.time()-start)

books = dict()
books["books"] = descriptions_dicts
print type(books)

##divider = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
##chunks = divider(books,1000)

with open('isbn_description.json', 'w') as f:
    for chunk in json.JSONEncoder().iterencode(books):
        f.write(chunk)
##
##f = open('test.json','r')
##dataraw = f.read()
##data = json.loads(dataraw)
##print type(data)
##f.close
