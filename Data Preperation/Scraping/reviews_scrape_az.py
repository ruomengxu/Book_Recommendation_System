from multiprocessing import Pool, Lock, Manager
import multiprocessing
import time
import urllib
import requests
import sys
import random
import os
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ProxyError
from requests.exceptions import ConnectionError
from requests.exceptions import ContentDecodingError
from requests.exceptions import TooManyRedirects
from functools import partial
from bs4 import BeautifulSoup
import re
import pandas as pd
from functools import partial
from tqdm import *
import datetime
import pyisbn
import sqlite3



#Uses proxy.txt proxies which is saved from running get_proxy() in the beginning of the code run
def get_proxy_saved():
    proxlst = []
    f = open('proxy.txt','r')
    for proxy in f.readlines():
        proxlst.append({'http':'http://' + proxy.strip()})
    return proxlst


def user_agents():
    agents_list = [  'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)', 
                     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)' ,
                     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
                     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' ]
    return random.choice(agents_list)

#Goes to gatherproxies.com to obtain fresh list of proxies of about 90 proxies.
#Using this function too much withh make me banned from the site, use cautiously,gently.
def get_proxy():
    ports = ['8080','80','3128','8888','81']
    proxlst = []
    proxycleanlst = []
    for port in tqdm(ports):
        url = 'http://gatherproxy.com/embed/?t=Elite&p=' + port + '&c='
        proxlst_saved = get_proxy_saved()
        while True:
            try:
                randomlst = [0,1,2]
                if random.choice(randomlst) != 0:
                    prox  = random.choice(proxlst_saved)
                    response = requests.get(url, headers={'User-agent': user_agents()},proxies = prox, timeout = (1,5))
                else: response = requests.get(url, headers={'User-agent': user_agents()})
                if response.status_code != 200:
                    try: proxlst_saved.remove(prox)
                    except: proxlst_saved = get_proxy_saved()
                    continue
                else: break
            except:
                print "Something wrong grabbing proxies"
                pass
            
        html = response.content
        soup = BeautifulSoup(html,'html.parser')
        try:
            proxlstraw = soup.find_all('script',attrs={'type':'text/javascript'})
            proxlstraw = soup.find_all('script',attrs={'type':'text/javascript'})[3:len(proxlstraw)-3]
        except: print "Something wrong during scriping proxies from gatherproxy"
            
        
        for proxraw in proxlstraw:
            proxraw = unicode(proxraw.string).strip()
            beg = '"PROXY_IP":"'
            end = '","PROXY_LAST_UPDATE":'
            try:
                proxclean =  proxraw[proxraw.index(beg)+len(beg):proxraw.index(end)] + ':' + port
                proxlst.append({'http':'http://' + str(proxclean)})
                proxycleanlst.append(proxclean)
            except: print "proxclean not properly read: Error arising from get_proxy()"
    f = open('proxy.txt','w')
    for proxy in proxycleanlst: f.write(proxy +'\n')
    f.close
    return proxlst

#*#Uses preexisting proxies to simultaneously check for internet conenction/ obtain html.
def wait_for_internet_connection(ur):
    proxlst = get_proxy_saved()
    while True:
        try:
            response = requests.get(ur, headers={'User-agent': user_agents()}, proxies = random.choice(proxlst), timeout = (1,5))
            if len(response.content) < 100000:
##                print "wait_for_internet_connection: len(html) < 100000"
                continue
            else: return response
        except: print "Internect Connection Not Properly Initiated, Retrying..."
            
#*#Goes into the directory defined by path, and obtains names + extention of all files in the directory.        
def filename_extractor(path):
    lst = []
    files = os.listdir(path)
    for filename in files: lst.append(filename[:len(filename)-4])
    return lst

#*#Randomly chooses whether to obtain fresh proxies or use proxies from saved file.
#This must be done to ensure I am gently using gather_proxy, but also not reusing useless/banned proxies
def random_proxylst_choice():
    randomlst = [0,1,2,3,4,5,6,7,8,9]
    if random.choice(randomlst) == 0: return get_proxy()
    else: return get_proxy_saved()



#*#Enters url in question then successfully obtain/return soup object.
def proxy_loop(url,sharedproxs):
    while True:
        try:
            headers={ "User-agent": user_agents()}
            proxy = random.choice(sharedproxs)
            response = requests.get(url, headers = headers, proxies = proxy, timeout = (1,5))
            if response.status_code == 200: pass
            else:
                html = response.content
                f = open('errorresponse.html','w')
                f.write(html)
                f.close()
            html = response.content
            if len(html) < 100000:
                if len(sharedproxs) == 0:
                    for prox in random_proxylst_choice(): sharedproxs.append(prox)
                else:
                    try: sharedproxs.remove(proxy)
                    except ValueError: pass
                continue
            else: pass
            break
        except (IndexError,UnboundLocalError):
            for prox in random_proxylst_choice(): sharedproxs.append(prox)
            print "Proxies Left %s: IndexError, UnBoundError"  %len(sharedproxs)

        except (ConnectTimeout,ReadTimeout,ChunkedEncodingError,ProxyError,ConnectionError,ContentDecodingError,TooManyRedirects):
            if len(sharedproxs) == 0:
                for prox in random_proxylst_choice(): sharedproxs.append(prox)
            else: 
                try: sharedproxs.remove(proxy)
                except ValueError: pass
            print "Proxies Left %s: All Error"  %len(sharedproxs)
    delay = 2
    time.sleep(delay)
    return html




def fetch_review(url,sharedproxs):
    isbn = url[url.index('https://www.amazon.com/product-reviews/') +len('https://www.amazon.com/product-reviews/'):]
    html = proxy_loop(url,sharedproxs[0])
    soup = BeautifulSoup(html,'html.parser')
    reviewstot = soup.find('span',attrs={'data-hook':'total-review-count'}).contents[0]
    reviewstot = unicode(reviewstot).encode('ascii','ignore')
    avgreview = soup.find('span',attrs={'data-hook':'rating-out-of-text'}).contents[0]
    avgreview = unicode(avgreview).encode('ascii','ignore')
    
    reviewslst = []
    reviews = soup.find_all('div',attrs={'data-hook':'review'})
    if reviews == []:
        print "Reviews Total: %s, %s , %s , %s" %(isbn, reviewstot, avgreview , 'No Review')
        return avgreview
    else: pass
        
    for review in reviews:
        if review.find('div',attrs={'class':'a-row review-data'}) != None:
            review_content = review.find('span',attrs={'data-hook':'review-body'})
            review_content = unicode(review_content).encode('ascii','ignore')
        else:
            print "Invalid review_content, sys.exit()"
            sys.exit()
        reviewslst.append(review_content)
    print "Reviews Total: %s, %s , %s , %s" %(isbn, reviewstot, avgreview ,  len(reviewslst))

    ##Combine all the reviews together
    combinedreviews = '<ggami_boxes>'.join(reviewslst)
    l = sharedproxs[1]
    l.acquire()
    if os.path.isfile('database/reviews.sqlite') == False:
        conn = sqlite3.connect('database/reviews.sqlite')
        cur = conn.cursor()
        ##Introduces Some kind of concurrency enabled mode. 
        cur.execute('PRAGMA journal_mode=WAL')
        cur.executescript('''

            Create TABLE ReviewsTable (
            
            isbn TEXT UNIQUE ,
            tot_reviews TEXT,
            avg_review_rating TEXT,
            review_content TEXT
            );
            ''')
    else:
        conn = sqlite3.connect('database/reviews.sqlite')
        cur = conn.cursor()
        ##Introduces Some kind of concurrency enabled mode
        cur.execute('PRAGMA journal_mode=WAL')
        cur.execute('''INSERT OR REPLACE INTO ReviewsTable (isbn,tot_reviews,avg_review_rating,review_content)
                    VALUES (?,?,?,?)''', (isbn,reviewstot , avgreview , combinedreviews))
    conn.commit()
    conn.close()
    l.release()
    return avgreview
    

    
if __name__ == '__main__':
    start = time.time()
    baseurl = 'https://www.amazon.com/product-reviews/'
    f = open('isbn_name.tsv','r')
    lines = f.readlines()
    f.close()
    testisbns = []
    for line in lines:
        if not line.strip():
            continue
        isbn = line.strip().split()[0]
        if len(isbn) <= 0:
            print "Isbn not properly scraped"
        title = line.strip().replace(isbn,'').strip()
        testisbns.append(isbn)
    print "Success!"

    
        
    
    isbns = []
    for testisbn in testisbns:
        isbns.append(str(testisbn.strip().replace('-','')))
    print len(isbns)

    urlstup = []
    for isbn in isbns:
        isbnraw = isbn[:]
        if len(isbn) == 10: pass
        elif len(isbn) == 13:
            try:
                isbn = pyisbn.convert(isbn)
            except pyisbn.IsbnError as e:
                print "Invalid ISBN: " , isbn
                continue
        else:
            print "Length of ISBN not 13 or 10: " , isbn
            continue
        isbn_title_author = (isbnraw,isbn,title,author)
        urlstup.append(fullurl)
    print len(urls)
    
    urls = []
    for isbn in isbns:
        if len(isbn) == 10: pass
        elif len(isbn) == 13:
            try:
                isbn = pyisbn.convert(isbn)
            except pyisbn.IsbnError as e:
                print "Invalid ISBN: " , isbn
                continue
        else:
            print "Length of ISBN not 13 or 10: " , isbn
            continue
        fullurl = baseurl + isbn
        urls.append(fullurl)
    print len(urls)

    
    


