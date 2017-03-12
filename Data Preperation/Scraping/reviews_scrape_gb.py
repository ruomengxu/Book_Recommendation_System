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
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import settings

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import base64




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
##                print "Proxies Left %s"  %len(sharedproxs)
                continue
            else: pass
            break
        ## Unbound local error, "proxy' referenced before assignment == No sharedproxs content
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




def fetch_review(isbn,sharedproxs):
    starturl =  'https://www.goodreads.com/search?q=' + str(isbn)
    proxy = random.choice(sharedproxs[0])['https'].replace('sk004:cpUGUJ4L@','')
    service_args = [
        '--proxy={}'.format(proxy),
        '--proxy-auth=sk004:cpUGUJ4L',
        '--proxy-type=https'
        ]
    driver = webdriver.PhantomJS(service_args = service_args)
    driver.get(starturl)    
    try:
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "bookReviews")))
    except:
        print "isbn: {}".format(isbn)
        print driver.current_url
        print "Timeout has occured, Page could not load the reviews box"
        driver.quit()
        return []

         
    html = driver.page_source
    try: url = driver.current_url
    except: url = 'Not recognized url'
    print url
    driver.quit()

    
    print len(html)
    soup = BeautifulSoup(html,'html.parser')

    image = soup.find('img',attrs={'id':'coverImage'})
    if not image:
        print "No Image Found"
    else:
        image = image.get('src')
        
    title = soup.find('h1',attrs={'class':'bookTitle'})
    if not title:
        print "No title recognized.."
    else:
        title = title.contents[0].strip()
        title = unicode(title).encode('ascii','ignore')
        print "title: {}".format(title)

    description = soup.find('div',attrs={'id':'description'})
    if not description:
        print "No description recognized.."
    else:
        description = unicode(description).encode('ascii','ignore')
        print "description: {}".format(description)

    avgrating = soup.find('span',attrs={'itemprop':'ratingValue'})
    if not avgrating:
        print "No avgrating recognized.."
    else:
        avgrating = avgrating.string
        print "avgrating: {}".format(avgrating)

    ratingcount = soup.find('span',attrs={'itemprop':'ratingCount'})
    if not ratingcount:
        print "No ratingcount recognized.."
    else:
        ratingcount = ratingcount.string
        print "ratingcount: {}".format(ratingcount)

    try:
        bookReviewsBox = soup.find('div',attrs={'id':'bookReviews'})
        if not bookReviewsBox:
            print "No bookReviewsBox recognized.."
        else:
            reviews = bookReviewsBox.find_all('div',attrs={'class':'friendReviews elementListBrown'})
            if reviews == []:
                print "There is no reviews for this title"
                reviewsread = []
            else:
                reviewsread = []
                for review in reviews:
                    rating = review.find('span',attrs={'class':' staticStars'})
                    rating = unicode(rating).encode('ascii','ignore')
                    reviewtext = review.find('div',attrs={'class':'reviewText stacked'})
                    reviewtext = unicode(reviewtext).encode('ascii','ignore')
                    reviewsread.append( "<review>" + rating + reviewtext + "<review>" ) 

        totalnumreviews = len(reviewsread)
    except:
        reviewsread = []
        totalnumreviews = 0
        
        
    
    
   
    l = sharedproxs[1]
    l.acquire()
    if os.path.isfile('database/reviews_gr.sqlite') == False:
        conn = sqlite3.connect('database/reviews_gr.sqlite')
        cur = conn.cursor()
        ##Introduces Some kind of concurrency enabled mode. 
        cur.execute('PRAGMA journal_mode=WAL')
        cur.executescript('''

            Create TABLE ReviewsTable (
            
            isbn TEXT UNIQUE ,
            title TEXT,
            image TEXT,
            url TEXT,
            description TEXT,
            totalnumreviews TEXT,
            avgrating TEXT,
            review_content TEXT
            );
            
            ''')
    else:
        conn = sqlite3.connect('database/reviews_gr.sqlite')
        cur = conn.cursor()
        ##Introduces Some kind of concurrency enabled mode
        cur.execute('PRAGMA journal_mode=WAL')
        cur.execute('''INSERT OR REPLACE INTO ReviewsTable (isbn,title, image, url, description,  totalnumreviews, avgrating , review_content)
                    VALUES (?,?,?,?,?,?,?,?)''', (isbn, title, image ,url, description, totalnumreviews , avgrating , '<seperator>'.join(reviewsread)))
    conn.commit()
    conn.close()
    l.release()
    return html

    

    
if __name__ == '__main__':
    
    isbns = []
    f = open('isbnshalf.txt','r')
    results = f.readlines()
    for line in results:
        isbn = line.strip()
        isbns.append(isbn)
    print len(isbns)


    con = sqlite3.connect('database/reviews_gr.sqlite')
    cur = con.cursor()
    cur.execute('select isbn from ReviewsTable')
    results = cur.fetchall()
    cur.close()

    
    isbnsread = []
    for isbn in results:
        isbn = str(isbn[0])
        isbnsread.append(isbn)
    print len(isbnsread)


    isbnsrest = []
    for isbn in isbns:
        if isbn  in isbnsread: continue
        else: isbnsrest.append(isbn)
    print len(isbnsrest)
        
    
    
        
    proxs = settings.proxy_paid()
    manager = Manager()
    freshproxies = manager.list(proxs)
    manager2 = Manager()
    l = manager2.Lock()
    partial_fetch_review = partial(fetch_review,sharedproxs = (freshproxies,l))
    
    p = Pool(4)
    result = p.map(partial_fetch_review,isbnsrest, chunksize = 1)
    p.close()
    p.join() 
    print 'Runtime: %ss' % (time.time()-start)
    print result

        

    



