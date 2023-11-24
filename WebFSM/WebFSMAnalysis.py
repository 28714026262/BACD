from WebFSM import FSM

class UserGroup:
    def __init__(self) -> None:
        self.fsm = ""
        self.groupName = ""
        self.priority = -1

class DiffFSM:
    def __init__(self) -> None:
        self.FSM = FSM()   

class FSMAnalysis:
    def __init__(self) -> None:
        self.UserGrouplist = []
    
    def VerticalBACDetected(self):
        pass

    def HorizontalBACDetected(self):
        pass