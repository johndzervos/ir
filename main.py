from textPreProcessor import * 
from document import * 
from invertedIndex import * 
import glob
import collections
invIndex = []
#postList = []
#postListEntry = {'docname': 'asdf', 'tf': 1}
#indexEntry = {'term': 'some val', 'docFreq': 1, 'postList': []}
#indexEntry['postList'].append(postListEntry)
#invIndex.append(indexEntry)
    
#process each document in the directory 'collection'
doclist = glob.glob("sampleCollection/*.txt")
listOfDocs=[]
for docname in doclist:
    #remove the starting substring 'collection/'
    if docname.startswith('sampleCollection/'):
        docname = docname[17:]   
    #remove the ending substring '.txt' 
    if docname.endswith('.txt'):
        docname = docname[:-4]
        #print docname
    print docname
    file_content = open(docname+".txt").read()
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
    #make a class Document whre we put the content of the doc,its name....
    #now we put the length of a file in the doc, later the term freq
    d=Document(t.file,docname)
    #puth the docs in a list
    listOfDocs.append(d)
#call the class inverted index which has an input a list of Documents
indexInverted=InvertedIndex(listOfDocs)
indexInverted.createIndex()
print indexInverted.index


    
        
