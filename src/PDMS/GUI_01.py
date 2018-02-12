#!/usr/bin/python3
import sys
#fPyQt5.QtCore import QT
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QMainWindow
from PyQt5.uic import loadUi

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets

#from PySide.QtGUI import QApplication
#from PySide.QtCore import QUrl
#from PySide.QtWebKit import QWebView, QWebSettingss

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

PDFJS = 'file:///H:/repos/PDMS/src/PDMS/tmp/pdfjs-1.9.426-dist/web/viewer.html'
PDF = 'file:///H:/repos/PDMS/src/PDMS/doc.pdf'


class PDMSGUI(QMainWindow):
    
    def __init__(self):
        #super().__init__()       
        super(PDMSGUI,self).__init__()
        loadUi('QT/PDMS/PDMS_02.ui',self)
        self.setWindowTitle('PDMS')
        
        #self.centralwidget = QtWidgets.QWidget(PDMSGUI)
        #self.PDFWidget = QtWebEngineWidgets.QWebEngineView()
        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.webView.setObjectName("webView")
        self.gridBrowser.addWidget(self.webView, 0, 0, 1, 1)
        
        #self.webView.setUrl(QtCore.QUrl("http://www.google.com/"))
        self.webView.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, PDF)))
        
        self.ScanButton.clicked.connect(self.on_button_clicked);
        
        #self.PDFWidget.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, PDF)))
        #self.browser = QWebEngineView()
        #self.browser.setUrl(QUrl('https://www.google.de/'))
        #self.SearchButton.clicked.connect(self.on_button_clicked);
        #self.initUI()
        
        
    #def initUI(self):    
    #    loadUi('mainwindow.ui',self)
    #    self.setWindowTitle('PDMS')
    #    self.SearchButton.clicked.connect(self.on_button_clicked);
    
    @pyqtSlot()
    def on_button_clicked(self):
        self.Text.setText('Press ScanButton')
            
        
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
s