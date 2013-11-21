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
            #stemmedWord = word        
            stemmed_Words.append(stemmedWord)
    return stemmed_Words

def getListOfDocsOfTerm(processedQuery):
    #check if the query word exists
    try:
        idx = loaded_data[processedQuery].items()
    except:
        idx=-1
    return idx

#example query 
query = open("sampleQuery.txt")
#process query
processedQuery=preprocessQuery(query)
print processedQuery
#dictionary of the final ranked docs

newIndex = []
for i in processedQuery:
    print i
    newentry = []
    newentry={'term':i, 'postlist':loaded_data[i].items()}
    newIndex.append(newentry)

for i in newIndex:
    print i

print "Statistics"
print newIndex[0]['term'] #the term
print newIndex[0]['postlist'] #the posting list
print newIndex[0]['postlist'][0][0] #name of the document
print newIndex[0]['postlist'][0][1] #term freq in that document
print len(newIndex[0]['postlist']) #doc freq

doclist=[]
for i in range(len(newIndex)):
    for j in range(len(newIndex[i].values()[1])):
        ent = []
        dname = newIndex[i]['postlist'][j][0]
        ent = {'docname':dname, 'termfrequency': newIndex[i]['postlist'][j][1]}
        #print ent
        for k in doclist:
        #    print k['docname'] + " in doclist"
            if k['docname'] == dname:
                print "aaa"
            else:
                print "bbb"
        doclist.append(ent)

print "document names are"
for i in doclist:
    print i
