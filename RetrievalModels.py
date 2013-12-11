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
import numpy as np, os

items = os.listdir("collection/")
# get the number of documnets inside collection
NoOfDocumentsInsideCollection = len(items)

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

def generateFileTrecFormat(result, fileName, queryID, modelType):
    if queryID == 1:
        #for the first query we write to the file
        f = open(fileName, 'w')
    else:
        #for the second query we append to the file
        f = open(fileName, 'a')
        
    for i in range(len(result)):
        s = str(queryID) + " Q0 " + str(result[i]['dd']) + ' ' + str(i + 1) + ' ' + str(result[i]['ss']) + " " + modelType
        f.write(s + "\n")
    f.close()

def tfidf(processedQuery, InvertedIndex):
    newIndex = []
    for i in processedQuery:
        if i in InvertedIndex:
            newentry = []
            newentry={'term':i, 'postlist':InvertedIndex[i].items()}
            newIndex.append(newentry)
    doclist = []
    dlist = []
    dnames = []
    for i in range(len(newIndex)):
        for j in range(len(newIndex[i].values()[1])):
            dname = newIndex[i]['postlist'][j][0]
            tf = newIndex[i]['postlist'][j][1]
            df = len(newIndex[i]['postlist'])
            trm = newIndex[i]['term']
            if dname in dnames:
                for k in range(len(doclist)):
                    if doclist[k]['docname']==dname:
                        struct2a = {'term': trm, 'tf2': tf, 'df2': df}
                        doclist[k]['list'].append(struct2a)
            else:
                dnames.append(dname)
                struct1 = {'docname': dname, 'list':[]}
                struct2b = {'term': trm, 'tf2': tf, 'df2': df}
                struct1['list'].append(struct2b)
                doclist.append(struct1)        
    tfidfscores = []
    for i in range(len(doclist)):
        score = 0
        dn = doclist[i]['docname']
        for j in range(len(doclist[i]['list'])):
            tf3 = doclist[i]['list'][j]['tf2']
            df3 = doclist[i]['list'][j]['df2']
            #tf-idf formula
            score = score + (1+np.log10(tf3))*np.log10(NoOfDocumentsInsideCollection/df3)
        sss = {'dd':dn, 'ss': score}
        tfidfscores.append(sss)

    tfidfresult = sorted(tfidfscores, key=lambda k: k['ss'], reverse=True)
    return tfidfresult

def BM25(processedQuery, InvertedIndex, docInfo, b, k1):
    #b = 0.75 # document length scaling
    #k1 = 1.5 # tunning parameter, choose a value between 1.2 and 5
    averageLength = 0
    for i in range(len(docInfo)):
        averageLength = averageLength + docInfo[i]['doclength']
    averageLength = averageLength/NoOfDocumentsInsideCollection
    newIndex = []
    for i in processedQuery:
        if i in InvertedIndex:
            newentry = []
            newentry={'term':i, 'postlist':InvertedIndex[i].items()}
            newIndex.append(newentry)

    doclist = []
    dlist = []
    dnames = []

    for i in range(len(newIndex)):
        for j in range(len(newIndex[i].values()[1])):
            dname = newIndex[i]['postlist'][j][0]
            tf = newIndex[i]['postlist'][j][1]
            df = len(newIndex[i]['postlist'])
            trm = newIndex[i]['term']             
            if dname in dnames:
                for k in range(len(doclist)):
                    if doclist[k]['docname']==dname:
                        struct2a = {'term': trm, 'tf2': tf, 'df2': df}
                        doclist[k]['list'].append(struct2a)
            else:
                dnames.append(dname)
                struct1 = {'docname': dname, 'list':[]}
                struct2b = {'term': trm, 'tf2': tf, 'df2': df}
                struct1['list'].append(struct2b)
                doclist.append(struct1)

    okapiscores = []
    for i in range(len(doclist)):
        score = 0
        dn = doclist[i]['docname']
        #get document length
        dlength = 0
        for k in range(len(docInfo)):
            if docInfo[k]['document'] == dn:
                dlength = docInfo[k]['doclength']
                break
        if dlength <> 0:
            for j in range(len(doclist[i]['list'])):
                tf3 = doclist[i]['list'][j]['tf2']
                df3 = doclist[i]['list'][j]['df2']
                #BM25 formula
                score = score + np.log10(NoOfDocumentsInsideCollection/df3)* ((k1+1)*tf3)/(k1*((1-b) + b*(dlength/averageLength))+ tf3)
            sss = {'dd':dn, 'ss': score}
            okapiscores.append(sss)
    BM25result = sorted(okapiscores, key=lambda k: k['ss'], reverse=True)
    return BM25result

def computeLangModel(term,tf,Ld,opt, cf, averageLength):
    if opt==1:
        #interpolation equation
        inter=0.5
        score=inter*(tf/Ld)+(1-inter)*cf[term]
    if opt==2:
        #Dirichlet smoothing
        #alpha=0.8
        alpha = averageLength
        score=(tf+alpha*cf[term])/(Ld+alpha)
    return score

def LanguageModel(processedQuery, InvertedIndex, docInfo, collectionFrequency):
    averageLength = 0
    for i in range(len(docInfo)):
        averageLength = averageLength + docInfo[i]['doclength']
    averageLength = averageLength/262
    
    newIndex = []
    for i in processedQuery:
        #check if i exists in index
        if i in InvertedIndex:
            newentry = []
            newentry={'term':i, 'postlist':InvertedIndex[i].items()}
            newIndex.append(newentry)
    doclist = []
    dlist = []
    dnames = []
    
    for i in range(len(newIndex)):
        for j in range(len(newIndex[i].values()[1])):
            dname = newIndex[i]['postlist'][j][0]
            tf = newIndex[i]['postlist'][j][1]
            df = len(newIndex[i]['postlist'])
            trm = newIndex[i]['term'] 
            if dname in dnames:
                for k in range(len(doclist)):
                    if doclist[k]['docname'] == dname:
                        struct2a = {'term': trm, 'tf2': tf, 'df2': df}
                        doclist[k]['list'].append(struct2a)
            else:
                dnames.append(dname)
                struct1 = {'docname': dname, 'list':[]}
                struct2b = {'term': trm, 'tf2': tf, 'df2': df}
                struct1['list'].append(struct2b)
                doclist.append(struct1)
                
    langModelScore = []
    for i in range(len(doclist)):
        score = 0
        dn = doclist[i]['docname']
        #get document length
        dlength = 0
        for k in range(len(docInfo)):
            if docInfo[k]['document'] == dn:
                dlength = docInfo[k]['doclength']
                break
        if dlength <> 0:
            for j in range(len(doclist[i]['list'])):
                tf3 = doclist[i]['list'][j]['tf2']
                df3 = doclist[i]['list'][j]['df2']
                #choose smoothing, opt=1 -> linear interpolation, opt=2 ->dirichlet
                opt=2
                pscore=computeLangModel(doclist[i]['list'][j]['term'],tf3,dlength,opt, collectionFrequency, averageLength)
                score=score+np.log10(pscore)
            sss = {'dd':dn, 'ss': score}
            langModelScore.append(sss)
    
    langModelresult = sorted(langModelScore, key=lambda k: k['ss'], reverse=True)
    return langModelresult

def demo(ModelType):
    stemmer=PorterStemmer()
    InvertedIndex = pickle.load(open( "SavedInvertedIndex.p", "rb" ))
    docInfo = pickle.load(open("DocLength.p", "rb"))
    collectionFrequency = pickle.load(open( "termColFreq.p", "rb" ))
    
    firstQuery = open("FirstQuery.txt")
    firstProcessedQuery=preprocessQuery(firstQuery)
    secondQuery = open("SecondQuery.txt")
    secondProcessedQuery=preprocessQuery(secondQuery)

    if (ModelType == "TF-IDF"):
        print "TF-IDF"
        tfidfResult = tfidf(firstProcessedQuery, InvertedIndex)
        generateFileTrecFormat(tfidfResult, 'TFIDFEvaluationResult.txt', 1, "tfidf")
        tfidfResult = tfidf(secondProcessedQuery, InvertedIndex)
        generateFileTrecFormat(tfidfResult, 'TFIDFEvaluationResult.txt', 2, "tfidf")
        print "Finished"
    elif (ModelType == "BM25"):
        print "BM25"
        b_list = [0.1, 0.5, 0.9]
        k1_list = [1.5, 3.0, 4.5]
        b = 0.75
        k1 = 1.5

        for b in b_list:
            for k1 in k1_list:
                bm25Result = BM25(firstProcessedQuery, InvertedIndex, docInfo,b, k1)
                #filename = ['BM25EvaluationResult_' +str(b)+ '_' +str(k1)+ '.txt']
                generateFileTrecFormat(bm25Result, 'BM25EvaluationResult_' +str(b)+ '_' +str(k1)+ '.txt', 1, "BM25")
                bm25Result = BM25(secondProcessedQuery, InvertedIndex, docInfo, b, k1)
                generateFileTrecFormat(bm25Result, 'BM25EvaluationResult_' +str(b)+ '_' +str(k1)+ '.txt', 2, "BM25")
        print "Finished"
    else:
        print "Language Model"
        langModelResult = LanguageModel(firstProcessedQuery, InvertedIndex, docInfo, collectionFrequency)
        generateFileTrecFormat(langModelResult, 'LanguageModellingResult.txt', 1, "LanguageModelling")
        langModelResult = LanguageModel(secondProcessedQuery, InvertedIndex, docInfo, collectionFrequency)
        generateFileTrecFormat(langModelResult, 'LanguageModellingResult.txt', 2, "LanguageModelling")
        print "Finished"
    
demo("TF-IDF")
#demo("BM25")
#demo("Language")

