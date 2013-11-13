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
    print "tokens before preprocessing: "+str(len(file_content))
    tot_tokens.append(len(file_content))
    #stemming + count term frequency
    d = defaultdict(int)
    stemmed_Words = []
    for word in file_content:
        stemmedWord = stemmer.stem(word)
        stemmed_Words.append(stemmedWord)
        d[stemmedWord] += 1
        
    #build the inverted index
    for word in stemmed_Words:
        locations = InvertedIndex.setdefault(word, {})
        locations[docname] = d[word]

print "total tokens: "+str(sum(tot_tokens))
print "unique terms: "+str(len(InvertedIndex)) 
# total number of tokens
#print len(InvertedIndex)
# total count of the token 'of'
#print InvertedIndex['of']
#print len(InvertedIndex['of'])
# the Inverted Index
#for i in InvertedIndex.items():
#    print i

pickle.dump(InvertedIndex, open("SavedInvertedIndex.p", "wb"))
loaded_data = pickle.load(open( "SavedInvertedIndex.p", "rb" ))
#for i in loaded_data.items():
#    print i

idxof = loaded_data['of'].items()
cnt = 0
for i in idxof:
    #print i[1]
    cnt = cnt + i[1]

print "Of appears: " + str(cnt)



