from PDMSStates import * 
from statemachine import StateMachine

# Initialize state machine for document scanning
def initScanStateMachine():
    print("Creating STATA MACHINE for document scanning!")
    m = StateMachine();
    m.add_state("START_NewDocument", StartNewDocument_state)
    m.add_state("ScannerIO_Scan", ScannerIO_Scan_state)
    m.add_state("ScannerIO_SaveImage", ScannerIO_SaveImage_state)
    m.add_state("ScannerIO_CreateTXT", ScannerIO_CreateTXT_state)
    m.add_state("ScannerIO_SaveHTML", ScannerIO_SaveHTML_state)
    m.add_state("ScannerIO_LoadDocuments", ScannerIO_LoadDocuments_state)
    m.add_state("ScannerIO_AddDocuments", ScannerIO_AddDocuments_state)
    m.add_state("ScannerIO_SaveDocuments", ScannerIO_SaveDocuments_state)
    m.add_state("DocCluster_LoadDocumentsCluster", DocCluster_LoadDocumentsCluster_state)
    m.add_state("DocCluster_LoadTXT", DocCluster_LoadTXT_state)
    m.add_state("ProcessCluster", ProcessCluster_state)
    m.add_state("SaveCluster", SaveCluster_state)
    m.add_state("End", EndNewDocument_state, end_state=1)
    # set start state
    m.set_start("START_NewDocument")
    return m
