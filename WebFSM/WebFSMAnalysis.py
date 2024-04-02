from WebFSM import FSM

class UserGroup:
    def __init__(self) -> None:
        self.fsm = ""
        self.groupName = ""
        self.priority = -1


class FSMAnalysis:
    def __init__(self) -> None:
        self.UserGrouplist = []
    
    def VerticalBACDetected(self):
        pass

    def HorizontalBACDetected(self):
        pass

    def diffFSM(self, FSM1, FSM2):
        return 0 # [node:[action,],]

    def childgraphfinder(self, FSM_input):
        res_fsm = None
        return res_fsm
    
    def long_bussiness_chain(self, FSM_input):
        return None # [node:[action],]
        
    def global_share_area(self, FSM_input):
        res_fsm = None
        return res_fsm

    def cutEdgeFromEDGENODEToShareGraph(self, FSM_input):
        pass

    def EDGENODEFinder(self, FSM_input):
        return None # [node_list]