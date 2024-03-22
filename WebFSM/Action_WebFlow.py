'''
预期返回结构：
{
    "Flow_Group":
    {
        "user":
        {
            "webpage_1":
            {
            "click" : ["self.HRA"]
            "click" : ["self.HRA"]
            ....
            "input" : ["self.HRA"]
            "input" : ["self.HRA"]
            ....
            },
            "webpage_2":
            ....
        } ,
        "superuser":
        ....
    }
}
'''
#ActionFilter用来过滤input和无意义的click
class ActionFilter:
    def __init__(self) -> None:
        self.same_click_FilterContainer = []
        self.click_list = []
        self.same_input_FilterContainer = []
        self.input_list = []

    #过滤id=''与之前统计过的无意义元素
    def click_filter(self):
        pass

    def click_condition_check(self):
        #若匹配过滤元素则返还相应flag
        pass

    #提取最终输入结果
    def input_filter(self):
        pass

    def input_condition_check(self):
        #若匹配过滤元素则返还相应flag
        pass

#GAF = ActionFilter()

#WebFilter会作更改
class WebFilter:
    def __init__(self, GLOBAL_CONFIG={}) -> None:
        pass

    def URLFilter(self):
        pass

    def staticResourceFilter(self):
        pass

    def sameURLFilter(self, url):
        pass

    def is_Same_URL_Route(self, first_url: str, second_url: str):
        pass

    def is_Same_URL_Route_by_list(self, first_list: list, second_list: list):
        pass

    def get_URL_Route(self, url: str) -> list:
        pass

    def domain(self):
        pass


#GWF = WebFilter()

class FlowNode:
    def __init__(self) -> None:
        pass

    def clear(self):
        pass

    #def analyze_action_and

class Flow():
    def __init__(self) -> None:
        pass

    def __deepcopy__(self, memodict={}):
        pass

    #这里找出在哪一个action发生后造成urlchanged
    def getActionGap(self):
        pass

    #根据getActionGap的信息进行模块区分
    def Flow_Gap_Aligner(self):
        pass

    def get_domain_url(self):
        pass

    def append_new_flow_node(self):
        pass

    #过滤剩下useful_req
    def flow_filter(self):
        pass

    def is_useful_url(self):
        pass

    def is_useful_req(self):
        pass

    def show_flow_list(self):
        pass

    def get_time_list(self):
        pass

class FlowSet:
    def __init__(self) -> None:
        self.FlowsetContainer = set()
        pass

    def flowSetAppend(self):
        pass

    #目前不是很清楚这边要怎么用
    def getSameFlowNode(self):
        pass

class ReturnToFlowAnalysis:
    def __init__(self) -> None:
        pass

    #把预期返回结果传输给图生成模块
    def ReturnFlowGroup(self):
        pass

class FlowRoleGroup:
    def __init__(self) -> None:
        self.flowset = FlowSet()
        self.role_name = ""
        self.role_code = -1
        self.FlowRoleGroup = set()

    def flowRoleAppend(self):
        pass

#应该会跟原代码一样
class Global_Flow_Node_Analyzer:
    def __init__(self) -> None:
        pass

    def getDataFromTraffic(self):
        pass

    def getHRAInPath(self):
        pass

    def getHRAInStr(self):
        pass

    def getHRAInLines(self):
        pass

    def flowAppend(self):
        pass

    def BurpResultSuiterToFlow(self):
        pass

    def UnrelatedTrafficFromURL(self):
        pass

    def get_url_list(self):
        pass

    #调用上面的filter
    def url_filter(self):
        pass

    def action_filter(self):
        pass

    #调用上面的GapAllign函数
    def GapAllign(self):
        pass

    def getFlow(self):
        pass

#GFNA = Global_Flow_Node_Analyser()

# if __name__ == "__main__":
    #config_init()
    # burp_path = r"C:/Users/User/Downloads/BACD/BACD-main/source/result.txt"
    # log_path = r"C:/Users/User/Downloads/BACD/BACD-main/source/filtered_data.txt"
    # GFNA.getFlow(0, "user", burp_path, log_path)
    # a = 1