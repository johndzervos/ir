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
    #print i
    newentry = []
    newentry={'term':i, 'postlist':loaded_data[i].items()}
    newIndex.append(newentry)

#for i in newIndex:
#    print i

print "Statistics"
print newIndex[0]['term'] #the term
print newIndex[0]['postlist'] #the posting list
print newIndex[0]['postlist'][0][0] #name of the document
print newIndex[0]['postlist'][0][1] #term freq in that document
print len(newIndex[0]['postlist']) #doc freq

doclist = []
docnames = []
dlist = []
dnames = []

for i in range(len(newIndex)):
    for j in range(len(newIndex[i].values()[1])):
        dname = newIndex[i]['postlist'][j][0]
        tf = newIndex[i]['postlist'][j][1]
        df = len(newIndex[i]['postlist'])
        trm = newIndex[i]['term']
        print dname +" in newIndex", tf, df, trm
        #ent = {'docname':'', 'list':[]}
        #doclist.append(ent)
        docnames.append(dname)
        
        #if len(doclist)==0:
        #    print "doclist empty" 
        #    struct0 = {'term': trm, 'tf2': tf, 'df2': df}
        #    ent = {'docname':dname, 'list':[]}  
        #    ent['list'].append(struct0) 
            #doclist.append(ent)
            #doclist
        #   doclist.append(dname)
        #else:   
        if dname in dnames:
            print "doc in doclist-------"
            for k in range(len(doclist)):
                if doclist[k]['docname']==dname:
                    struct2a = {'term': trm, 'tf2': tf, 'df2': df}
                    doclist[k]['list'].append(struct2a)
        else:
            print "doc not in doclist"
            dnames.append(dname)
            struct1 = {'docname': dname, 'list':[]}
            struct2b = {'term': trm, 'tf2': tf, 'df2': df}
            struct1['list'].append(struct2b)
            doclist.append(struct1)
            
    print len(dnames)
    for i in doclist:
        print i
            #for k in range(len(doclist)):
                #print k['docname'] +" in doclist"
                #print k
                #if doclist[k]['docname'] == dname:
                #if doclist[k] == dname:
                    #print "1---------document exists in doclist"
                    #struct2a = {'term': trm, 'tf2': tf, 'df2': df}
                    #print doclist[k]
                    #doclist[k]['list'].append(struct2a)
                    #break;
                #else:
                    #print "2---document NOT in doclist"
                    #doclist.append(dname)
                    #struct1 = {'docname': dname, 'list':[]}
                    #struct2b = {'term': trm, 'tf2': tf, 'df2': df}
                                  
                    #doclist.append(struct1)
                    #print doclist[k]
                    #doclist[k]['list'].append(struct2b)
            #print doclist[k]
            #print len(doclist),"len of doclist"
        #docnames.append(dname)

print "document names are"
for i in doclist:
    print i
