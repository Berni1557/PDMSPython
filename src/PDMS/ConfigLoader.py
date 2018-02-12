import html2text
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import parse
import os.path

# class to load and save config
class ConfigLoader:
    def __init__(self, Docspath):
        self.Docspath = Docspath
        self.Docs = []

    def load(self):
        print("Loading Config.")
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
      
    def save(self):
        print("Saving Config.")
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
            
        doc.writexml( open(self.Docspath, 'w'),
                       indent="  ",
                       addindent="  ",
                       newl='\n')
         
        doc.unlink()
