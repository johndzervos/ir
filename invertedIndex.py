class InvertedIndex(): 
    def __init__(self,listOfDocs):
        self.listOfDocs=listOfDocs
        self.index={}
    def createIndex(self):
        for d in self.listOfDocs:
            for w in d.doc:
                if w not in self.index.keys():
                    self.index[w]={}
                self.index[w][d.docId]=d.length