from PDMSStates import * 
from statemachine import StateMachine

# Initialize state machine for document scanning
def initSearchStateMachine():
    print("Creating STATA MACHINE for searching!")
    m = StateMachine();
    m.add_state("START_Search", StartSearch_state)
    m.add_state("DocSearcher_LoadDocumentsCluster", DocSearcher_LoadDocumentsCluster_state)
    m.add_state("DocSearcher_waitInput", DocSearcher_waitInput_state)
    m.add_state("DocSearcher_search", DocSearcher_search_state)
    m.add_state("DocSearcher_showResults", DocSearcher_showResults_state)
    m.add_state("End", EndSearch_state, end_state=1)
    m.set_start("START_Search")
    return m