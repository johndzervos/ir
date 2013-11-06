from textPreProcessor import * 
from document import * 
from invertedIndex import * 
import glob
    
#process each document in the directory 'collection'
doclist = glob.glob("sampleCollection/*.txt")
print len(doclist)
listOfDocs=[]
for docname in doclist:
    #remove the starting substring 'collection/'
    if docname.startswith('sampleCollection\\'):
        docname = docname[17:]   
    #remove the ending substring '.txt' 
    if docname.endswith('.txt'):
        docname = docname[:-4]
        #print docname
    print docname
    file_content = open("sampleCollection/"+docname+".txt").read()
    d=Document(file_content,docname)
    #print t.file
    d.lowerCase()
    #print t.file
    d.removeOddCharacters()
    d.wordTokenization()
    d.removeStopwords()
    d.stemming()
    d.sortTerms()
    listOfDocs.append(d)
#call the class inverted index which has an input a list of Documents
indexInverted=InvertedIndex(listOfDocs)

indexInverted.createIndex()
for i in indexInverted.index.items():
    print i
##print indexInverted.index.items()[3][1]
##miniList=indexInverted.index.items()[3][1]

    
        
