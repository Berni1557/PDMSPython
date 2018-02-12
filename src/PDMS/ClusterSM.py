from PDMSStates import * 

# Initialize state machine for document scanning
def initClusterStateMachine():
    print("Creating STATA MACHINE for clustering!")
    m = StateMachine();
    m.add_state("START_Clustering", StartClustering_state)
    m.add_state("DocCluster_LoadDocumentsCluster", DocCluster_LoadDocumentsCluster_state)
    m.add_state("DocCluster_LoadTXT", DocCluster_LoadTXT_state)
    m.add_state("ProcessCluster", ProcessCluster_state)
    m.add_state("SaveCluster", SaveCluster_state)
    m.add_state("End", EndClustering_state, end_state=1)
    m.set_start("START_Clustering")
    return m