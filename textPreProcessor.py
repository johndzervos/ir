import nltk 
import re, string
import unicodedata
import glob
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

class TextPreProcessor(object ):
    def __init__( self,file ):
        self.file=file
        
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
        #should be working now
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

invIndex = []
#postList = []
#postListEntry = {'docname': 'asdf', 'tf': 1}
#indexEntry = {'term': 'some val', 'docFreq': 1, 'postList': []}
#indexEntry['postList'].append(postListEntry)
#invIndex.append(indexEntry)

#process each document in the directory 'collection'
doclist = glob.glob("collection/*.txt")

def main():

    for docname in doclist:
        #remove the starting substring 'collection/'
        if docname.startswith('collection/'):
            docname = docname[11:]   
        #remove the ending substring '.txt' 
        if docname.endswith('.txt'):
            docname = docname[:-4]
            #print docname
        print docname

        file_content = open("collection/"+docname+".txt").read()

        #file_content = open("CSIRO063-12268790.txt").read()
        t=TextPreProcessor(file_content)
        #print t.file
        t.lowerCase()
        #print t.file
        t.removeOddCharacters()
        #print t.file
        t.wordTokenization()
        #print t.file
        t.removeStopwords()
        #print t.file
        t.removeDuplicates()
        #print t.file
        t.stemming()
        #print t.file
        t.removeDuplicates()
        t.sortTerms()
        #print t.file
        print len(t.file)
        struct = {'docname': docname, 'uniqueTerms': len(t.file)}
        invIndex.append(struct)
    
main()

#print invIndex
for i in invIndex:
    print i

print len(invIndex)
