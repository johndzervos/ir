import nltk 
import re, string
import unicodedata
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

class Document():
    def __init__(self, doc, docId):
        self.file=doc
        self.docId=docId

    def termFrequency(self,term):
        noOccurences = 0
        for word in self.file:
            if term == word:
                noOccurences = noOccurences + 1
        return noOccurences

    def lowerCase(self):
        self.file=self.file.lower()

    def removeOddCharacters(self):
        self.file=re.sub(r'[^a-z0-9 ]',' ',self.file)
    
    def wordTokenization(self):
        self.file = re.sub('[%s]' % re.escape(string.punctuation), '', self.file)
        self.file = nltk.word_tokenize(self.file)

    def removeStopwords(self):
        tokens=[]
        for word in self.file:
            if word not in stopwords.words('english'):
                tokens.append(word)
        self.file=tokens
        #self.file = [w for w in self.file if w not in stopwords.words('english')]

    def removeDuplicates(self):
        noDuplicates=[]
        for word in self.file:
            if word not in noDuplicates:
                noDuplicates.append(word)
        self.file=noDuplicates

    def stemming(self):
        stemmer=PorterStemmer()
        stemmedWords = []
        for word in self.file:
            stemmedWords.append(stemmer.stem(word))
        self.file=stemmedWords

    def sortTerms(self):
        sortedFile=[]
        sortedFile = sorted(self.file)
        self.file=sortedFile

    def wordLemmatization(self):
        lemmatizer = WordNetLemmatizer()
        lemmatization_result = []
        for word in self.file:
            lemmatization_result.append(lemmatizer.lemmatize(word))
        self.file=lemmatization_result

    def removeAccents():
        noaccents_tokens=[]
        return ''.join((c for c in unicodedata.normalize('NFD', self.file.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
        noaccents_tokens = [remove_accents(item) for item in important_tokens]
        self.file=noaccents_tokens
