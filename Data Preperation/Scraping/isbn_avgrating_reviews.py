import sqlite3
from bs4 import BeautifulSoup
import json
import pprint
import time
import pyisbn

## Reads three seperate sqlite databases, collect the results into json
con = sqlite3.connect('reviews_gr.sqlite')
con.text_factory = str
cur = con.cursor()
cur.execute('select * from ReviewsTable')
results1 = cur.fetchall()
cur.close()

start = time.time()
reviews_tup = []
reviews_dicts = []
for row in results1:
    reviews = row[7]
    if not reviews:
        reviews_parsed = []
    else:
        ## Splits the raw review string by "<seperator>", results in a list of unparsed reviews
        reviews = reviews.split('<seperator>')
        ## Stores only 5 reviews or less
        try: reviews = reviews[0:5]
        except IndexError:
            print "More than 5 reviews read. Truncating to 3 reviews.."
            pass
        reviews_parsed = []
        for review in reviews:
            ## Maybe having an enter key between tag makes it not readable
            soup = BeautifulSoup(review,'html.parser')
            longreview = soup.find('span',attrs={'style':'display:none'})
            if longreview:
                review = longreview
            else:
                shortreviewspan = soup.find_all('span')
                if shortreviewspan == []:
                    review = BeautifulSoup('','html.parser')
                else:
                    for spantag in shortreviewspan :
                        reviewid = spantag.get('id')
                        if not reviewid:
                            review = BeautifulSoup('','html.parser')
                        elif "freeText" in reviewid:
                            shortreview = spantag
                            break
                review = shortreview
            review = ''.join(review.findAll(text=True))
            review = review.strip()
            if review == "": continue
            else: pass
            reviews_parsed.append(review)
        reviews_tup.append(reviews_parsed)
        reviews_dict = dict()
        reviews_dict["reviews"] = reviews_parsed
        reviews_dict["isbn"] = row[0]
        reviews_dict["avg_rating"] = float(row[6].strip())
        reviews_dicts.append(reviews_dict)
        
print "total rows read {}".format(len(results1))
print "len reviews_tup {}".format(len(reviews_tup))
print "time took to process: {}".format(time.time()-start)
        
con = sqlite3.connect('reviews_gr_2.sqlite')
con.text_factory = str
cur = con.cursor()
cur.execute('select * from ReviewsTable')
results1 = cur.fetchall()
cur.close()

start = time.time()
reviews_tup = []
for row in results1:
    reviews = row[7]
    if not reviews:
        reviews_parsed = []
    else:
        ## Splits the raw review string by "<seperator>", results in a list of unparsed reviews
        reviews = reviews.split('<seperator>')
        ## Stores only 5 reviews or less
        try: reviews = reviews[0:5]
        except IndexError:
            print "More than 5 reviews read. Truncating to 3 reviews.."
            pass
        reviews_parsed = []
        for review in reviews:
            ## Maybe having an enter key between tag makes it not readable

            soup = BeautifulSoup(review,'html.parser')
            longreview = soup.find('span',attrs={'style':'display:none'})
            if longreview:
                review = longreview
            else:
                shortreviewspan = soup.find_all('span')
                if shortreviewspan == []:
                    review = BeautifulSoup('','html.parser')
                else:
                    for spantag in shortreviewspan :
                        reviewid = spantag.get('id')
                        if not reviewid:
                            review = BeautifulSoup('','html.parser')
                        elif "freeText" in reviewid:
                            shortreview = spantag
                            break
                review = shortreview
            review = ''.join(review.findAll(text=True))
            review = review.strip()
            if review == "": continue
            else: pass
            reviews_parsed.append(review)
        reviews_tup.append(reviews_parsed)
        reviews_dict = dict()
        reviews_dict["reviews"] = reviews_parsed
        reviews_dict["isbn"] = row[0]
        reviews_dict["avg_rating"] = float(row[6].strip())
        reviews_dicts.append(reviews_dict)
        
print "total rows read {}".format(len(results1))
print "len reviews_tup {}".format(len(reviews_tup))
print "time took to process: {}".format(time.time()-start)

con = sqlite3.connect('reviews_az.sqlite')
con.text_factory = str
cur = con.cursor()
cur.execute('select * from ReviewsTable')
results1 = cur.fetchall()
cur.close()


start = time.time()
reviews_tup = []
for row in results1:
    reviews = row[3]
    if not reviews:
        reviews_parsed = []
    else:
        ## Splits the raw review string by "<seperator>", results in a list of unparsed reviews
        reviews = reviews.split('<ggami_boxes>')
        ## Stores only 5 reviews or less
        try: reviews = reviews[0:5]
        except IndexError:
            print "More than 5 reviews read. Truncating to 3 reviews.."
            pass
        reviews_parsed = []
        for review in reviews:
            ## Maybe having an enter key between tag makes it not readable
            soup = BeautifulSoup(review,'html.parser')
            review = ''.join(soup.findAll(text=True))
            review = review.strip()
            if review == "": continue
            else: pass
            reviews_parsed.append(review)
        reviews_tup.append(reviews_parsed)
        reviews_dict = dict()
        reviews_dict["reviews"] = reviews_parsed
        reviews_dict["isbn"] = row[0]
        reviews_dict["avg_rating"] = float(row[2].split()[0])
        reviews_dicts.append(reviews_dict)
        
        reviews_dict = dict()
        reviews_dict["reviews"] = reviews_parsed
        reviews_dict["isbn"] = pyisbn.convert(row[0])
        reviews_dict["avg_rating"] = float(row[2].split()[0])
        reviews_dicts.append(reviews_dict)
        
        
print "total rows read {}".format(len(results1))
print "len reviews_tup {}".format(len(reviews_tup))
print "time took to process: {}".format(time.time()-start)

books = dict()
books["books"] = reviews_dicts
print type(books)


with open('isbn_avgrating_reviews.json', 'w') as f:
    for chunk in json.JSONEncoder().iterencode(books):
        f.write(chunk)

