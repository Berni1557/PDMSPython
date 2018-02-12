#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QMainWindow
from PyQt5.uic import loadUi
import time
import string
PDFJS = 'file:///H:/repos/PDMS/src/PDMS/tmp/pdfjs-1.9.426-dist/web/viewer.html'
PDF = 'file:///H:/repos/PDMS/src/PDMS/doc.pdf'

from Scanner import Scanner
from DocSearcher import DocSearcher
from FileAccess import DocumentsFileAccess
from settings import path_Documents, path_tmp


class PDMSGUI(QMainWindow):
    
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self):
        
        # Init GUI      
        super(PDMSGUI,self).__init__()
        loadUi('QT/PDMS/PDMS_05.ui',self)
        self.setWindowTitle('PDMS')
        
         # Init Scan tab
        # Init PDF Viewer
        self.webViewPDF = QtWebEngineWidgets.QWebEngineView()
        self.webViewPDF.setObjectName("webView")
        self.gridBrowser.addWidget(self.webViewPDF, 0, 0, 1, 1)
        self.webViewPDF.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, PDF)))
        
        # Init HTML Viewer
        self.webViewHTML = QtWebEngineWidgets.QWebEngineView()
        self.webViewHTML.setObjectName("webView")
        self.gridBrowser.addWidget(self.webViewHTML, 0, 1, 1, 1)
        #self.webViewHTML.setUrl(QtCore.QUrl("http://www.google.com/"))
        self.webViewHTML.setUrl(QtCore.QUrl("file:///H:/repos/PDMS/data/docs/docHTML/doc_2018212_129_24.HTML"))
        
        # Set callbacks
        self.ScanButton.clicked.connect(self.on_button_scan);
        self.AddTag.clicked.connect(self.add_tag);
        self.AddDoc.clicked.connect(self.saveDoc);
        
        # Init Objects
        self.access = DocumentsFileAccess(path_Documents)
        self.scanner = Scanner(self.access)
        self.scanner.loadDocuments()
        
        # Init Search tab
        self.searchViewPDF = QtWebEngineWidgets.QWebEngineView()
        self.searchViewPDF.setObjectName("Search Document")
        self.searchGrid.addWidget(self.searchViewPDF, 0, 0, 1, 1)
        self.searchViewPDF.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, PDF)))
        
        self.DocS_Access=DocumentsFileAccess(path_Documents)
        self.DocS=DocSearcher( self.DocS_Access)
        self.DocS.loadDocuments()
        
         # Set callbacks
        self.SearchButton.clicked.connect(self.on_button_search);
        self.DocsCombo.currentIndexChanged.connect(self.onActivated) 
        self.SearchTag.returnPressed.connect(self.on_key)
        #self.DocsCombo.activated.connect(self.onActivated)
        #self.DocsCombo.currentIndexChanged.connect(self.selectionchange)

    @pyqtSlot()
    def on_button_scan(self):
        self.StatusLine.setText('Start scanning.')
        time.sleep(0.1)
        
        # Scan document
        self.scanner.scan() 
        self.scanner.createHTML()
        #self.scanner.saveImage()
        
        filepath_pdf_tmp = path_tmp + '\\image.pdf'
        filepath_html_tmp = path_tmp + '\\image.html'
        
        # Show PDF document
        file = 'file:///' + filepath_pdf_tmp
        self.webViewPDF.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, file)))
        
        # Extract HTML from pdf
        #self.scanner.createHTML()
       
        # Show HTML document
        file = 'file:///' +  filepath_html_tmp
        #file.replace('\\', '/')
        file = '/'.join(file.split('\\'))
        self.StatusLine.setText(file)
        time.sleep(0.1)
        self.webViewHTML.setUrl(QtCore.QUrl(file))

    @pyqtSlot()
    def add_tag(self):
        self.scanner.doc.tag = self.Tag.text();
        self.StatusLine.setText('Adding Tags: ' + self.scanner.doc.tag)
        #print('Adding Tags: ' + self.scanner.doc.tag)

    @pyqtSlot()
    def saveDoc(self):
        self.StatusLine.setText('Saveing document.')
        self.scanner.saveImage()        
        # Load documents
        self.scanner.loadDocuments()
        # Add document
        self.scanner.addDocument()
        # Save documents
        self.scanner.saveDocument()
        
    @pyqtSlot()
    def on_button_search(self):
        self.StatusLine.setText('Start searching.')
        tag_txt = self.SearchTag.text()
        self.DocS.processInputs(tag_txt)
        self.DocS.search()
        NumDocs = 5
        self.OrderedDocList = self.DocS.orderResults(NumDocs)
        self.DocsCombo.clear()
        for d in self.OrderedDocList:
            self.DocsCombo.addItem(d.DocImagePath)
               
    def onActivated(self, index):
        file = 'file:///' + self.OrderedDocList[index].DocImagePath
        print(len(self.OrderedDocList))
        print(index)
        self.searchViewPDF.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, file)))
        
    def on_key(self):
        self.on_button_search()

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    widget = PDMSGUI()
    widget.show();
    sys.exit(app.exec_())
    
    #b = QWebView()
    #b.show()
    #app.exec_()
    #widget = PDMSGUI()
    #widget.show();
    #sys.exit(app.exec_())
