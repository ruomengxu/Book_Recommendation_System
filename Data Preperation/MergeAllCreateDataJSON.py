# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:31:42 2016

@author: Silver
"""

#%% Load Data
import json

with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\isbn_title_author.json') as data_file:    
    data1 = json.load(data_file)
    
with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\isbn_avgrating_reviews.json') as data_file:    
    data2 = json.load(data_file)

with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\isbn_description.json') as data_file:    
    data3 = json.load(data_file)      
    
with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\BooksWithExtracts.json') as data_file:    
    data4 = json.load(data_file)    

with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\BookwithTropes.json',encoding="utf8") as data_file:    
    data5 = json.load(data_file)        

with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\TropeswithComment.json',encoding="utf8") as data_file:    
    data6 = json.load(data_file)   
   
with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\genre\\BooksWithExtracts_genre.json',encoding="utf8") as data_file:    
    data7 = json.load(data_file)    

with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\genre\\isbn_avgrating_reviews_genre.json',encoding="utf8") as data_file:    
    data8 = json.load(data_file) 

with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\genre\\isbn_description_genre.json',encoding="utf8") as data_file:    
    data9 = json.load(data_file) 
    
with open('C:\\Users\\Silver\\Desktop\\SUPER6\\Final Dataset\\imagelist.json',encoding="utf8") as data_file:    
    data10 = json.load(data_file) 
    
#%% Fix Extracts

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

ind = 0
success = 0
for extract in data4['Extracts']:
    ind += 1
    print(ind)
    extract['isbn'] = None
    for isbn in data1['books']:        
        if extract['Title'] == isbn['title']:
            success += 1
            extract['isbn'] = isbn['isbn']
        
#%% Fix Trops

ind = 0
success = 0
for tropelist in data5['books']:
    ind += 1
    print(ind)
    tropelist['isbn'] = None
    for isbn in data1['books']:        
        if tropelist['name'] == isbn['title']:
            success += 1
            tropelist['isbn'] = isbn['isbn']        
        

#%% List of ISBNs
ISBNs = []
for book in data1['books']:
    ISBNs.append(book['isbn'])
    
#%% Merge Reviews
for review in data2['books']:
    if review['isbn'] in ISBNs:
        if ISBNs.index(review['isbn']) != None:
            data1['books'][ISBNs.index(review['isbn'])]['avg_rating'] = review['avg_rating']
            data1['books'][ISBNs.index(review['isbn'])]['reviews'] = review['reviews']

#%% Merge Descriptions
for desc in data3['books']:
    if desc['isbn'] in ISBNs:
        if desc['isbn'] != None:
            data1['books'][ISBNs.index(desc['isbn'])]['description'] = desc['description']
            
#%% Merge Extracts
for extract in data4['Extracts']:
    if extract['isbn'] != None:
        data1['books'][ISBNs.index(extract['isbn'])]['extract'] = extract['Extract']

#%% Merge TropeLists
for tropes in data5['books']:
    if tropes['isbn'] != None:
        data1['books'][ISBNs.index(tropes['isbn'])]['tropes'] = tropes['tropes']

#%% Merge Tropes
Tropes = []
for trope in data6['tropes']:
        current = re.findall('[A-Z][^A-Z]*', trope['name'])
        current = ' '.join([word.lower() for word in current])
        Tropes.append(current)

#%% Keywords
from collections import Counter

CommonWords = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "i"
, "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but"
, "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my"
, "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about"
, "who", "get", "which", "go", "me", "book", "novel", "are", "has", "have", "is"
, "was", "will"]

ind = 0
for book in data1['books']:
    fields = book.keys()
    Corpus = ''
    if 'reviews' in fields:
        Corpus += ' '.join(book['reviews'])
    if 'description' in fields:
        Corpus += book['description']
    if 'extract' in fields:
        Corpus += book['extract']
        
    
       
    Corpus = Corpus.translate({ord(c): None for c in '1234567890.\/()`~!@#$%^&*-+=|\{}[]:;"<>,.?/'})
    words_filtered = [word.lower() for word in Corpus.split() if len(word) >= 3]  
    
    wordcount = Counter(words_filtered)
    wordcount = sorted(wordcount.items(), key=lambda item: item[1], reverse=True)  
    
    keywords = []
    for word in wordcount:
        if word[0] not in CommonWords:
            keywords.append(word[0])
        if len(keywords) == 10:
            break
        
        
    book['keywords'] = keywords
    ind += 1
    print(ind)


#%% Trope Tags
import re

ind = 0
success = 0
for book in data1['books']:
    fields = book.keys()
    Corpus = ''
    if 'reviews' in fields:
        Corpus += ' '.join(book['reviews'])
    if 'description' in fields:
        Corpus += book['description']  
    if 'extract' in fields:
        Corpus += book['extract']
    Corpus = Corpus.lower()    
    
    tropetags = []
    for trope in Tropes:
        if trope != '' and len(trope)>4 and trope in Corpus:
            tropetags.append(trope)
            success += 1
    
    book['tropetags'] = tropetags
    
    ind += 1
    print(100*ind/len(data1['books']))
    
#%% Trope Tags - Fine Tune
for bookind in range(61240,88070):
    book = data1['books'][bookind]
    fields = book.keys()
    Corpus = ''
    if 'reviews' in fields:
        Corpus += ' '.join(book['reviews'])
    if 'description' in fields:
        Corpus += book['description']  
    if 'extract' in fields:
        Corpus += book['extract']
    Corpus = Corpus.lower()    
    
    tropetags = []
    for trope in Tropes:
        if trope != '' and len(trope)>4 and trope in Corpus:
            tropetags.append(trope)
            success += 1
    
    book['tropetags'] = tropetags
    
    ind += 1
    print(100*ind/len(data1['books']))    
    
#%% Merge Genre
ind = 0
success = 0
for book in data1['books']:
    ind += 1
    print(100*ind/len(data1['books']))  
    
    book['genre'] = None
    
    for extractgenre in data7['books']:
        if extractgenre['title'] == book['title']:
            success += 1
            book['genre'] = extractgenre['genre'] 
            
    for reviewgenre in data8['books']:
        if reviewgenre['isbn'] == book['isbn']:
            if book['genre'] != None:
                newgenre = [0,0,0,0,0]
                for genreindex in range(0,5):
                    newgenre[genreindex] = book['genre'][genreindex] + reviewgenre['genre'][genreindex]
                    book['genre'] = newgenre        
            else:
                book['genre'] = reviewgenre['genre'] 
                

    for dscgenre in data9['books']:
        if dscgenre['isbn'] == book['isbn']:
            if book['genre'] != None:
                newgenre = [0,0,0,0,0]
                for genreindex in range(0,5):
                    newgenre[genreindex] = book['genre'][genreindex] + dscgenre['genre'][genreindex]
                    book['genre'] = newgenre        
            else:
                book['genre'] = dscgenre['genre']                 
                
                
#%% Sentiment - Load Pickles of Classifier and Word Features
import nltk

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

ind = 0
success = 0
for book in data1['books']:
    fields = book.keys()
    Corpus = ''
    if 'reviews' in fields:
        Corpus += ' '.join(book['reviews'])
    Corpus = Corpus.lower()    
    
    sentiment = None
    if Corpus != '':
        sentiment = classifier.classify(extract_features(Corpus))
    
    book['sentiment'] = sentiment
    
    ind += 1
    print(100*ind/len(data1['books']))                
                
               
#%% Get Images    
import http.client as httplib 

host = "www.isfdb.org"
 
def GetImage(isbn):
      webservice = httplib.HTTPConnection(host)
      command = '/cgi-bin/rest/getpub.cgi?%s' % isbn
      webservice.request('GET',command)
      response = webservice.getresponse()      
      text = response.read().decode("iso-8859-1")
      ImageURL = None
      if '<Image>' in text: 
          ImageURL = text.split('<Image>')[1].split('</Image>')[0]
      return ImageURL    
      
ind = 0
for book in data1['books']:
    ind += 1
    print(100*ind/len(data1['books']))  
    book['imageURL'] = GetImage(book['isbn'])
 
#%% Merge Images
for image in range(0,79384):
    data1['books'][image]['imageURL'] = data10['books'][image]['imageURL']

for image in range(79384,88070):
    data1['books'][image]['imageURL'] = None
   
#%% Clean
NewBooks =[]
Titles = []
for book in data1['books']:
    NewBook = {'title':book['title'], 'isbn':book['isbn'], 'author':book['author'], 'keywords':None, 'avg_rating':None, 'tropetags':None, 'genre':None, 'sentiment':None, 'imageURL':None}
    if 'keywords' in book.keys():
        NewBook['keywords'] = book['keywords']
    if 'avg_rating' in book.keys():
        NewBook['avg_rating'] = book['avg_rating']
    if 'tropetags' in book.keys():
        NewBook['tropetags'] = book['tropetags']
    if 'genre' in book.keys() and book['genre'] != None and sum(book['genre']) != 0:
        NewBook['genre'] = [round(100*genres / sum(book['genre'])) for genres in book['genre']]
    if 'sentiment' in book.keys():
        NewBook['sentiment'] = book['sentiment']   
    if 'imageURL' in book.keys():
        NewBook['imageURL'] = book['imageURL']      
    NewBooks.append(NewBook) 
    Titles.append(book['title'])

FinalData = {'books': NewBooks}    
#%% Save   
import json
with open('data.json', 'w') as outfile:
    json.dump(FinalData, outfile)
    
#%% Save Titles List    
Titles = list(set(Titles))
import json
with open('titles.json', 'w') as outfile:
    json.dump(Titles, outfile)    
    
    
#%% Push to Database
from pymongo import MongoClient    

client = MongoClient()
#client = MongoClient("mongodb://mongodb0.example.net:27017")

db = client['books']   

db.drop_collection("metadata")

for i in range(0,8):
    db['metadata'].insert_many(NewBooks[i*10000:(i+1)*10000])
     
db['metadata'].insert_many(NewBooks[80000:len(data1['books'])])   
   
#%%
   
   
   
    