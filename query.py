# -*- coding: utf-8 -*-
from __future__ import division
import glob, re, nltk, string, pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from utilFunctions import *
import math,operator
from itertools import groupby, chain
from operator import itemgetter

loaded_data = pickle.load(open( "SavedInvertedIndex.p", "rb" ))
stemmer=PorterStemmer()
##for i in loaded_data:
##    print loaded_data[i].items()

def preprocessQuery(query):
    tot_tokens = []
    file_content = query.read()
    file_content = file_content.lower()
    #remove odd chars
    file_content = re.sub(r'[^a-z0-9 ]',' ',file_content)
    #remove punctuation
    file_content = re.sub('[%s]' % re.escape(string.punctuation), '', file_content)
    #tokenization
    file_content = nltk.word_tokenize(file_content)
    #print "tokens before preprocessing: "+str(len(file_content))
    tot_tokens.append(len(file_content))
    #stemming + count term frequency
    stemmed_Words = []
    for word in file_content:
        if word not in stopwords.words('english'): 
            stemmedWord = stemmer.stem(word)
            stemmedWord = word        
            stemmed_Words.append(stemmedWord)
    return stemmed_Words

def getListOfDocsOfTerm(processedQuery):
    #check if the query word exists
    try:
        idx = loaded_data[processedQuery].items()
    except:
        idx=-1
    return idx

#-----------------It works only for 2 and more terms in the query, better doublecheck----------
#example query 
query = open("sampleQuery.txt")
#process query
processedQuery=preprocessQuery(query)
print processedQuery
#dictionary of the final ranked docs
rankedListOfDocs={}
#dict of the intersection of returned docs
final={}
#we need the counter so as to start from the seond element in the below loop
#cause in the first loop there is only one term, no intersection
count=1

#for every term in the query
for term in processedQuery:
    #get the docs of each term
    index=getListOfDocsOfTerm(term)
    #check if there is the term in the doc
    if(index!=-1& count!=1):
        #convert the list to dict to process quicker and easier
        dict_a = dict(index)
        dict_b=dict(combined)
        #common docs between terms
        all_keys = set(dict_b.keys()) | set(dict_a.keys())
        #make a new dict of the intersection of the docs
        final = dict((k, (dict_a.get(k), dict_b.get(k))) for k in all_keys)
    combined=index
    count=count+1

#for every doc in dict 
for key in final:
    #pointer to get the corresponding idf from the posting l
    counter=0
    sumScore=0
    for v in final[key]:
         #some terms occur only in one doc,the other returns none
         if (v!=None):
            noDocs=262 #total number of docs in collection, maybe we need to obtain it dynamically
            #compute tf
            tf=(1+float(math.log(float(v))))
            idf=math.log(noDocs/float(len(loaded_data[processedQuery[counter]].items())))
            score=tf*idf
            sumScore=sumScore+score
            counter=counter+1
    #assign to the rank dict the score of both terms
    rankedListOfDocs[key]=sumScore
#sort the dictionary based on the value returned by score tfidf
sortedRankOfDocs = sorted(rankedListOfDocs.iteritems(), key=operator.itemgetter(1))
print sortedRankOfDocs

    
