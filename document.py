class Document():
    def __init__(self, doc,length, docId):
        self.doc= doc
        self.docId=docId
        self.length=length

    def termFrequency(self, term):
        noOccurences = 0
        for word in self.doc:
            if term == word:
                noOccurences = noOccurences + 1
        return noOccurences
