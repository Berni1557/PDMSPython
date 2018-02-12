from Scanner import Scanner
from DocSearcher import DocSearcher
from FileAccess import DocumentsFileAccess
from settings import path_Documents

# States for state machines
ScanAccess=DocumentsFileAccess(path_Documents)
Scan=Scanner(ScanAccess)

def StartNewDocument_state(txt):
    print("Starting document creation SM.")
    return ("ScannerIO_Scan", "")

def ScannerIO_Scan_state(txt):
    print("Start scanning new document.")
    Scan.scan()
    return ("ScannerIO_SaveImage", "")

def ScannerIO_SaveImage_state(txt):
    print("Saving image document.")
    Scan.saveImage()
    return ("ScannerIO_CreateTXT", "")

def ScannerIO_CreateTXT_state(txt):
    print("Do OCR and create txt file.")
    return ("ScannerIO_SaveHTML", "")

def ScannerIO_SaveHTML_state(txt):
    print("Save txt file.")
    Scan.createHTML()
    return ("ScannerIO_LoadDocuments", "")

def ScannerIO_LoadDocuments_state(txt):
    print("Loading documents files from ScannerIO.")
    Scan.loadDocuments()
    return ("ScannerIO_AddDocuments", "")

def ScannerIO_AddDocuments_state(txt):
    print("Add document to documents list.")
    Scan.docFileAccess.addDocument(Scan.doc)
    return ("ScannerIO_SaveDocuments", "")

def ScannerIO_SaveDocuments_state(txt):
    print("Save documents list in Documents.xml.")
    Scan.docFileAccess.saveDocuments()
    return ("DocCluster_LoadDocumentsCluster", "")

def DocCluster_LoadDocumentsCluster_state(txt):
    print("Loading documents files from DocCluster.")
    return ("DocCluster_LoadTXT", "")

def DocCluster_LoadTXT_state(txt):
    print("Loading txt files.")
    return ("ProcessCluster", "")

def ProcessCluster_state(txt):
    print("Process clustering.")
    return ("SaveCluster", "")

def SaveCluster_state(txt):
    print("Save clusters to Clusters.xml.")
    return ("End", "")

def EndNewDocument_state(txt):
    print("End document creation.")
    return ("Scan", "")


DocS_Access=DocumentsFileAccess(path_Documents)
DocS=DocSearcher(DocS_Access)

def StartSearch_state(txt):
    print("Start document search SM.")
    return ("DocSearcher_LoadDocumentsCluster", "")

def DocSearcher_LoadDocumentsCluster_state(txt):
    print("DocSearcher is loading documents files from DocCluster.")
    DocS.loadDocuments()
    return ("DocSearcher_waitInput", "")

def DocSearcher_waitInput_state(txt):
    print("DocSearcher is waiting for input.")
    DocS.waitInputs()
    return ("DocSearcher_search", "")

def DocSearcher_search_state(txt):
    print("DocSearcher is searching.")
    DocS.search()
    return ("DocSearcher_showResults", "")

def DocSearcher_showResults_state(txt):
    print("DocSearcher is showing results.")
    DocS.showResults()
    return ("End", "")

def EndSearch_state(txt):
    print("End searching.")
    return ("", "")




def StartClustering_state(txt):
    print("Start clustering SM.")
    return ("DocCluster_LoadDocumentsCluster", "")

def EndClustering_state(txt):
    print("End clustering.")
    return ("", "")


