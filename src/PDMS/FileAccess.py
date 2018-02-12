import html2text
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import parse
import os.path

# class for document
class Doc:
    def __init__(self):
        self.name = None
        self.DocImagePath = None
        self.DocHTMLPath = None
        self.date = None
        self.tag = None
        self.txt = None
    

class DocumentsFileAccess:
    def __init__(self, Docspath):
        self.Docspath = Docspath
        self.Docs = []

    def loadDocuments(self):
        print("Load Documents (images and HTMLs!)")
        if os.path.exists(self.Docspath):
            try:
                dom = parse(self.Docspath)
            except:
                print("Creating new document.xml because document.xml corrupted or empty!")
                self.saveDocuments()
                dom = parse(self.Docspath)        
            # iterate over documents
            for node in dom.getElementsByTagName('doc'):
                d=Doc();    # create document
                d.name=node.getAttribute('name')      # get document name
                d.DocImagePath=node.getAttribute('DocImagePath')    # get document DocImagePath
                d.DocHTMLPath=node.getAttribute('DocHTMLPath')    # get document DocHTMLPath
                d.date=node.getAttribute('date')    # get document date
                d.tag=node.getAttribute('tag')    # get document tags
                self.Docs.append(d)
        else:
            print("Creating new document.xml because document.xml does not exist!")
            self.saveDocuments()
            dom = parse(self.Docspath) 
            
        #print("Docs: " + self.Docs)
      
    def saveDocuments(self):
        print("Saving Documents (images and HTMLs!)!")
        doc = minidom.Document()
        root = doc.createElement("data")
        doc.appendChild(root)
        
        # iterate over documents
        for d in self.Docs:
            docChild = doc.createElement("doc")
            docChild.setAttribute( "name", d.name )
            docChild.setAttribute( "DocImagePath", d.DocImagePath )
            docChild.setAttribute( "DocHTMLPath", d.DocHTMLPath )
            docChild.setAttribute( "date", d.date )
            docChild.setAttribute( "tag", d.tag )
            root.appendChild(docChild)
            
        print("Docspath: " + self.Docspath)
        
        #print("Docs: " + self.Docs)
            
        doc.writexml( open(self.Docspath, 'w'),
                       indent="  ",
                       addindent="  ",
                       newl='\n')
         
        doc.unlink()
        
    def addDocument(self, doc):
        print("Saving image and HTML to Documents.xml file!")
        self.Docs.append(doc)
        
    
    def extractTXTDocument(self,):
        print("Extract text from pdf files")
        for d in self.Docs:
            filename=d.DocHTMLPath
            html = open(filename, encoding='utf-8')
            f = html.read()
            s=html2text.html2text(f).encode('utf-8')
            d.txt=s    

  
        
class ConfigsFileAccess:
    def __init__(self, Docspath):
        self.Docspath = Docspath

    def loadConfig(self):
        print("Load config!")
            
    def saveConfig(self):
        print("Saving config!")

    def initConfig(self):
        print("Init config!")
        
        
        
class ClustersFileAccess:
    def __init__(self, Docspath):
        self.Docspath = Docspath

    def loadClusters(self):
        print("Load Clusters.xml file!")
            
    def saveClusters(self):
        print("Saving Clusters.xml file!")
