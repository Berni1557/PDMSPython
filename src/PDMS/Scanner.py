from FileAccess import Doc
import os
from settings import path_PDMS, path_tmp, path_docImage, path_docHTML
import time
from shutil import copyfile
import datetime

class Scanner:
    def __init__(self, docFileAccess):
        self.doc = Doc()
        self.docFileAccess=docFileAccess

    def scan(self):
        print("Scanning document!")
        
        filepath_pdf_tmp = path_tmp + '\\image.pdf'
        if os.path.exists(filepath_pdf_tmp): 
            os.remove(filepath_pdf_tmp) 
        
        #s='"C:\\Program Files (x86)\\NAPS2\\NAPS2.Console" -o "' + path_PDMS + '\\tmp\\image.pdf"'
        s='"C:\\Program Files (x86)\\NAPS2\\NAPS2.Console" -o "' + filepath_pdf_tmp
        os.system('"'+s+'"')
        
        while not os.path.exists(filepath_pdf_tmp):        # wait until document was created
            time.sleep(1) # delays for 1 seconds during scan
        
        print("Document scan finished!")
           
    def saveImage(self):
        
        print("Saving image document!")
        filepath_pdf_tmp = path_tmp + '\\image.pdf'
        filepath_html_tmp = path_tmp + '\\image.html'
        
        # Create pdf file name based on current time
        now = datetime.datetime.now()       
        s = '\\doc_' + str(now.year) + str(now.month) + str(now.day) + '_' + str(now.hour) + str(now.minute) + '_' + str(now.second) + '.pdf'
        filepath_pdf = path_docImage + s
        
        # Fill doc
        self.doc.DocImagePath=filepath_pdf
        self.doc.name=s[1:len(s)-4]
        self.doc.date=str(now.year) + str(now.month) + str(now.day) + '_' + str(now.hour) + str(now.minute) + '_' + str(now.second)
        
         # Create html file name based on current time
        filepath_html = path_docHTML + '\\' +self.doc.name + '.html'  
        self.doc.DocHTMLPath = filepath_html 
   
        #print(self.doc.DocHTMLPath)      
        # copy file from tmp folder to docImage folder
        copyfile(filepath_pdf_tmp, filepath_pdf)
        copyfile(filepath_html_tmp, filepath_html)
        
        # delete file from tmp
        os.remove(filepath_pdf_tmp) 
        os.remove(filepath_html_tmp) 
        
        print("saveImage: " +  self.doc.name)

    def createHTML(self):
        print("Create HTML document!")
        filepath_pdf_tmp = path_tmp + '\\image.pdf'
        filepath_html_tmp = path_tmp + '\\image.html'
            
        if os.path.exists(filepath_pdf_tmp):
            print("Creating document!")          
            # create command for pdf2txt
            #st = 'pdf2txt.py -o "' + self.doc.DocHTMLPath + '" "' + self.doc.DocImagePath + '"'
            st = 'pdf2txt.py -o "' + filepath_html_tmp + '" "' + filepath_pdf_tmp + '"' 
            os.system('"'+st+'"')

    def loadDocuments(self):
        print("Load Documents.xml!")
        self.docFileAccess.loadDocuments()
               
    def addDocument(self):
        print("Add document to Documents.xml file!")
        self.docFileAccess.addDocument(self.doc);
        
    def saveDocument(self):
        print("Save Documents.xml!")
        self.docFileAccess.saveDocuments();

