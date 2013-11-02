import nltk 
import re, string
import unicodedata
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

stemmer=PorterStemmer()
lemmatizer = WordNetLemmatizer()

#
#
#1st step - collect documents to be indexed
file_content = open("CSIRO063-12268790.txt").read()
file_content = file_content.lower()
file_content=re.sub(r'[^a-z0-9 ]',' ',file_content)

#2nd step - tokenization (remove punctuation + split text into tokens + remove stop words)
file_content = re.sub('[%s]' % re.escape(string.punctuation), '', file_content)
tokens = nltk.word_tokenize(file_content)
important_tokens=[]
for word in tokens:
    if word not in stopwords.words('english'):
        important_tokens.append(word)

#print len(tokens)
#print len(important_tokens)

#3rd step - normalization (remove accents and diacritics + case folding + stemming + lemmatization)
#def remove_accents(s):
#   return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
#noaccents_tokens = [remove_accents(item) for item in important_tokens]

#lowercase_tokens = [item.lower() for item in important_tokens]
#print lowercase_tokens

#remove duplicates
noduplicatesBeforeStemming = []
for word in important_tokens:
    if word not in noduplicatesBeforeStemming:
        noduplicatesBeforeStemming.append(word)

stemmedWords = []
for word in noduplicatesBeforeStemming:
    stemmedWords.append(stemmer.stem(word))

print "stemming_result"
#print stemmedWords

noduplicatesAfterStemming = []
for word in stemmedWords:
    if word not in noduplicatesAfterStemming:
        noduplicatesAfterStemming.append(word)

stemmedAndSortedTokens = sorted(noduplicatesAfterStemming)
for i in stemmedAndSortedTokens:
    print i
#print stemmedAndSortedTokens
print len(stemmedAndSortedTokens)
    
#stemming_result = ",".join([ stemmer.stem(kw) for kw in important_tokens])

#print stemming_result
#lemmatization_result = ",".join([ lemmatizer.lemmatize(kw) for kw in important_tokens])
#print lemmatization_result

#4th step - create the inverted index
#print stemming_result
#sorted(stemming_result)
#print stemming_result[0]
#print "Sorted list"
#print stemming_result

#remove the duplicates
s = []
for i in important_tokens:
       if i not in s:
          s.append(i)


