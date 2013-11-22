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
import numpy as np

loaded_data = pickle.load(open( "SavedInvertedIndex.p", "rb" ))
docInfo = pickle.load(open("DocLength.p", "rb"))

stemmer=PorterStemmer()
b = 0.75 # document length scaling
k1 = 1.5 # tunning parameter, choose a value between 1.2 and 5

averageLength = 0
for i in range(len(docInfo)):
    averageLength = averageLength + docInfo[i]['doclength']
averageLength = averageLength/262
print "Average length:" + str(averageLength) 

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

#example query 
query = open("sampleQuery.txt")
#process query
processedQuery=preprocessQuery(query)
print processedQuery
#dictionary of the final ranked docs

newIndex = []
for i in processedQuery:
    #print i
    #check if i exists in index
    if i in loaded_data:
        newentry = []
        newentry={'term':i, 'postlist':loaded_data[i].items()}
        newIndex.append(newentry)

print "Statistics"
print newIndex[0]['term'] #the term
print newIndex[0]['postlist'] #the posting list
print newIndex[0]['postlist'][0][0] #name of the document
print newIndex[0]['postlist'][0][1] #term freq in that document
print len(newIndex[0]['postlist']) #doc freq

doclist = []
dlist = []
dnames = []

for i in range(len(newIndex)):
    for j in range(len(newIndex[i].values()[1])):
        dname = newIndex[i]['postlist'][j][0]
        tf = newIndex[i]['postlist'][j][1]
        df = len(newIndex[i]['postlist'])
        trm = newIndex[i]['term']
        print dname +" in newIndex", tf, df, trm
         
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

okapiscores = []
for i in range(len(doclist)):
    #print i
    score = 0
    #print len(doclist[i]['list']), i
    dn = doclist[i]['docname']
    #get document length
    dlength = 0
    for k in range(len(docInfo)):
        if docInfo[k]['document'] == dn:
            dlength = docInfo[k]['doclength']
            break
    #print dn + " doc length:" + str(dlength)    
    if dlength <> 0:
        for j in range(len(doclist[i]['list'])):
            tf3 = doclist[i]['list'][j]['tf2']
            df3 = doclist[i]['list'][j]['df2']
            print doclist[i]['list'][j]['term'], tf3, df3
            #BM25 formula
            score = score + np.log10(262/df3)* ((k1+1)*tf3)/(k1*((1-b) + b*(dlength/averageLength))+ tf3)
            print "doc score: " + str(score)
        sss = {'dd':dn, 'ss': score}
        okapiscores.append(sss)

BM25result = sorted(okapiscores, key=lambda k: k['ss'], reverse=True)
for i in BM25result:
    print i

print len(BM25result)

