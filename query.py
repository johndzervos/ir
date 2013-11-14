from __future__ import division
import glob, re, nltk, string, pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from utilFunctions import *
import math,operator

loaded_data = pickle.load(open( "SavedInvertedIndex.p", "rb" ))
stemmer=PorterStemmer()
##for i in loaded_data:
##    print loaded_data[i].items()

def preprocessQuery(query):
    tot_tokens = []
    file_content = query.lower()
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


#-----------------It works only for one term in the query, need to be exetended----------

#example query 
query='june8'
#process query
processedQuery=preprocessQuery(query)
#empty dictionary of the ranked docs
rankedListOfDocs={}
#check if the query word exists
try:
    idx = loaded_data[processedQuery[0]].items()
except:
    idx=-1
if(idx!=-1):
    #take the freq of the doc which is the second place of the list in a list of lists
    for sublist in idx:
        noDocs=262 #toatal number of docs in collection, maybe we need to obtain it dynamically
        #compute tfidf, 
        rankedListOfDocs[sublist[0]]=(1+math.log(sublist[1]))*math.log(noDocs/len(loaded_data[processedQuery[0]].items()))
#sort the dictionary based on the value returned by score tfidf
    sortedRankOfDocs = sorted(rankedListOfDocs.iteritems(), key=operator.itemgetter(1))
    print sortedRankOfDocs
else:
    print "Query term not in collection!"
    
