# class DocSearcher
import webbrowser

class DocSearcher:
    def __init__(self,docFileAccess):
        self.docFileAccess=docFileAccess
        self.tags = []
        self.scoreResults = []
        self.docResults = []

    def loadDocuments(self):
        print("Load Documents.xml!")
        self.docFileAccess.loadDocuments()
        self.docFileAccess.extractTXTDocument()
        
    def waitInputs(self):
        print("Insert document tags (comma seperated)!")
        st = input("Tags: ")
        self.tags=st.split(',')
        st_tags = " ".join(self.tags)
        print("Extracted Tags: " + st_tags)

    def processInputs(self, tags_str):
        self.tags=tags_str.split(',')
        st_tags = " ".join(self.tags)
        print("Extracted Tags: " + st_tags)
        
    def search(self):
        print("Searching for documents!")
        self.docResults.clear()
        self.scoreResults.clear()
        for d in self.docFileAccess.Docs:
            n=0
            for t in self.tags:
                n = n + str(d.txt).count(t)
            self.docResults.append(d)
            self.scoreResults.append(n)
    
    def showResults(self):
        print("Searching for documents!")
        NumDocs=5;
        i=0
        scores=[];
        for d in self.docResults:
            score = self.scoreResults[i] / len(d.txt)
            scores.append(score);
            print(d.name + ": " + str(score))
            i = i + 1    
            
        i=0
        scoreResultsIdx=[b[0] for b in sorted(enumerate(scores),key=lambda i:i[1])]
        for i in range(0, NumDocs):
            idx=scoreResultsIdx[len(scoreResultsIdx)-NumDocs+i]
            d=self.docResults[idx]
            webbrowser.open_new(d.DocImagePath)

    def orderResults(self, NumDocs):
        print("Searching for documents!")
        #NumDocs=5;
        i=0
        scores=[];
        for d in self.docResults:
            score = self.scoreResults[i] / len(d.txt)
            scores.append(score);
            print(d.name + ": " + str(score))
            i = i + 1    
            
        i=0
        scoreResultsIdx=[b[0] for b in sorted(enumerate(scores),key=lambda i:i[1])]
        OrderedDocList=[]
        for i in range(0, NumDocs):
            idx=scoreResultsIdx[len(scoreResultsIdx)-NumDocs+i]
            d=self.docResults[idx]
            OrderedDocList.append(d)
            #webbrowser.open_new(d.DocImagePath)
        OrderedDocList.reverse()
        return OrderedDocList
            
    def searchRegEx(self):
        print("Searching for documents with searchRegEx!")