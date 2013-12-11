from __future__ import division
import glob, re, nltk, string, pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from utilFunctions import *

stemmer=PorterStemmer()
InvertedIndex = {}
tot_tokens = []
docidx = []

#process each document in the directory 'collection'
doclist = glob.glob("collection/*.txt")
InvertedIndex = {}
docidx = []
timeCounter=0
for doc in doclist:
    #made a progress bar for fun, remove it if you want
    timeCounter=timeCounter+1;
    steps=float(timeCounter)/len(doclist)
    update_progress(steps)
    #take the path of the doc
    base=os.path.basename(doc)
    #pick only the filename of the doc
    cleanDocname= os.path.splitext(base)[0]
    #print cleanDocname
    file_content = open(doc).read()
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
    d = defaultdict(int)
    stemmed_Words = []
    for word in file_content:
        #if word not in stopwords.words('english'): 
            stemmedWord = stemmer.stem(word)
        #stemmedWord = word        
            stemmed_Words.append(stemmedWord)
            d[stemmedWord] += 1

    stemlen = len(stemmed_Words)
    noDuplicates= []   
    for word in stemmed_Words:
        if word not in noDuplicates:
            noDuplicates.append(word)

    #build the inverted index
    for word in noDuplicates:
        locations = InvertedIndex.setdefault(word, {})       
        #d[word] = float(d[word])/stemlen
        locations[cleanDocname] = d[word]
        #print word, d[word]

print "total tokens: "+str(sum(tot_tokens))
print "unique terms: "+str(len(InvertedIndex))
idxof = InvertedIndex['of'].items()
cnt = 0
for i in idxof:
    cnt = cnt + i[1]
print "Of appears: " + str(cnt)
#save the index
pickle.dump(InvertedIndex, open("SavedInvertedIndex.p", "wb"))

#print the contents of index
#printIndex(InvertedIndex)

#loaded_data = pickle.load(open( "SavedInvertedIndex.p", "rb" ))




