# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 13:29:25 2016

@author: Silver
"""

import nltk

positive_reviews = [line.strip() for line in open('C:\\Users\\Silver\\Desktop\\reviews_Books_5.json\\HighReviews.txt', 'r')]
positive_tags = ['positive' for i in range(0,10000)]

pos_revs = list(zip(positive_reviews,positive_tags))

negative_reviews = [line.strip() for line in open('C:\\Users\\Silver\\Desktop\\reviews_Books_5.json\\LowReviews.txt', 'r')]
negative_tags = ['negative' for i in range(0,10000)]

neg_revs = list(zip(negative_reviews,negative_tags))

test_reviews = [line.strip() for line in open('C:\\Users\\Silver\\Desktop\\reviews_Books_5.json\\TestReviews.txt', 'r')]
test_tags =  [line.strip() for line in open('C:\\Users\\Silver\\Desktop\\reviews_Books_5.json\\TestRates.txt', 'r')]

test_revs = list(zip(test_reviews,test_tags))

#%%

train_reviews = []
for (words, sentiment) in pos_revs + neg_revs:
    words = words.translate({ord(c): None for c in '1234567890.\/()`~!@#$%^&*-+=|\{}[]:;"<>,.?/'})
    words_filtered = [word.lower() for word in words.split() if len(word) >= 3] 
    train_reviews.append((words_filtered, sentiment))


test_reviews = []
for (words, sentiment) in test_revs:
    words = words.translate({ord(c): None for c in '1234567890.\/()`~!@#$%^&*-+=|\{}[]:;"<>,.?/'})
    words_filtered = [word.lower() for word in words.split() if len(word) >= 3] 
    test_reviews.append((words_filtered, sentiment))


#%%

def get_words_in_reviews(reviews):
    all_words = []
    for (words, sentiment) in reviews:
      all_words.extend(words)
    return all_words
    
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features
 
    
word_features = get_word_features(get_words_in_reviews(train_reviews))    

#%%
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
    
training_set = nltk.classify.apply_features(extract_features, train_reviews)


#%%
classifier = nltk.NaiveBayesClassifier.train(training_set)

#%%
print(classifier.show_most_informative_features(32))


#%%
results = [classifier.classify(extract_features(line[0])) for line in test_reviews]

#%%
import time

t = time.time()
classifier.classify(extract_features(test_reviews[10][0]))
elapsed = time.time() - t

#%%
import csv
with open('eggs.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\n',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(results)      


#%%                  
import pickle
f = open('my_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()


#%%
import pickle
f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()



    