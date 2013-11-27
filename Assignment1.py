from __future__ import division
import glob, re, nltk, string, pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from utilFunctions import *


#process each document in the directory 'collection'
doclist = glob.glob("collection/*.txt")

stemmer=PorterStemmer()
InvertedIndex = {}
tot_tokens = []
docLength = []

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
    docInfo = {'document': cleanDocname, 'doclength': len(file_content)}
    docLength.append(docInfo)
    #stemming + count term frequency
    d = defaultdict(int)
    stemmed_Words = []
    for word in file_content:
        if word not in stopwords.words('english'): 
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

print "total tokens: " + str(sum(tot_tokens))
print "unique terms: " + str(len(InvertedIndex))

#save the index
pickle.dump(InvertedIndex, open("SavedInvertedIndex.p", "wb"))
pickle.dump(docLength, open("DocLength.p", "wb"))

#print the contents of index
printIndex(InvertedIndex)

loaded_data = pickle.load(open( "SavedInvertedIndex.p", "rb" ))
#-----Code to compute term collection frequency---------------

s=0
cf={}
for i in loaded_data:
    for j in loaded_data[i].values():
        s=s+j
    cf[i]=s
    s=0

pickle.dump(cf, open("termColFreq.p","wb"))
#for key, value in cf.iteritems() :
#    print key, value
cf = pickle.load(open( "termColFreq.p", "rb" ))
for i in cf:
    cf[i]=float(cf[i])/698565
  
