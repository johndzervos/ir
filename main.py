from textPreProcessor import * 
from document import * 
from invertedIndex import * 
import glob
    
#process each document in the directory 'collection'
doclist = glob.glob("collection/*.txt")
print len(doclist)
listOfDocs=[]
for docname in doclist:
    #remove the starting substring 'collection/'
    #starting substring
    startstring = 'collection\\'   
    #ending substring
    endstring = '.txt'
    if docname.startswith(startstring):
        strlen = len(startstring)
        docname = docname[strlen:]   
    #remove the ending substring '.txt' 
    if docname.endswith(endstring):
        strlen2 = len(endstring)
        docname = docname[:-strlen2]
        #print docname
    print docname
    file_content = open("collection/"+docname+".txt").read()
    d=Document(file_content,docname)
    #print t.file
    d.lowerCase()
    #print t.file
    #d.removeDuplicates()
    #print "remove odd chars"
    #d.removeOddCharacters()
    #print "tokenization"
    d.wordTokenization()
    #print "stopwords"
    d.removeStopwords()
    #print "stemming"
    d.stemming()
    #d.sortTerms()
    listOfDocs.append(d)
#call the class inverted index which has an input a list of Documents
indexInverted=InvertedIndex(listOfDocs)
indexInverted.createIndex()
for i in indexInverted.index.items():
    print i

##print indexInverted.index.items()[3][1]
##miniList=indexInverted.index.items()[3][1]

    
        
