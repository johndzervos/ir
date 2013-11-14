from __future__ import division
import glob, re, nltk, string, pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict



#process each document in the directory 'collection'
doclist = glob.glob("collection/*.txt")
startstring = 'collection\\'
strlenStartString = len(startstring)
endstring = '.txt'
strlenEndString = len(endstring)

stemmer=PorterStemmer()
InvertedIndex = {}
tot_tokens = []
docidx = []

for docname in doclist:
    if docname.startswith(startstring):
        docname = docname[strlenStartString:]
    if docname.endswith(endstring):
        docname = docname[:-strlenEndString]
    print docname
    file_content = open(docname+".txt").read()
    file_content = file_content.lower()
    #remove odd chars
    file_content = re.sub(r'[^a-z0-9 ]',' ',file_content)
    #remove duplicates
    #file_content = re.sub(r'\b(\w+)( \1\b)+', r'\1', file_content)
    #remove punctuation
    file_content = re.sub('[%s]' % re.escape(string.punctuation), '', file_content)
    #tokenization
    file_content = nltk.word_tokenize(file_content)
    #print "tokens before preprocessing: "+str(len(file_content))
    tot_tokens.append(len(file_content))
    #stemming + count term frequency

    #self.file = [w for w in self.file if w not in stopwords.words('english')]
    d = defaultdict(int)
    stemmed_Words = []
    for word in file_content:
        if word not in stopwords.words('english'): 
            stemmedWord = stemmer.stem(word)
            stemmedWord = word        
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
        d[word] = float(d[word])/stemlen
        locations[docname] = d[word]
        #print word, d[word]


print "total tokens: "+str(sum(tot_tokens))
print "unique terms: "+str(len(InvertedIndex)) 


pickle.dump(InvertedIndex, open("SavedInvertedIndex.p", "wb"))


loaded_data = pickle.load(open( "SavedInvertedIndex.p", "rb" ))
#for i in loaded_data.items():
#    print i

#idxof = loaded_data['of'].items()
#cnt = 0
#for i in idxof:
    #print i[1]
    #cnt = cnt + i[1]

#print "Of appears: " + str(cnt)



