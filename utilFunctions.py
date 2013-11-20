from __future__ import division
import glob, re, nltk, string, pickle,os,time,sys
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
stemmer=PorterStemmer()

def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "="*block + " "*(barLength-block), progress*100, status)
    print"\n"
    sys.stdout.write(text)
    sys.stdout.flush()
    

def preprocess(file_content):
    tot_tokens = []
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

    
def printIndex(loaded_data):
    for i in loaded_data:
        print i, loaded_data[i].keys(), loaded_data[i].values()
