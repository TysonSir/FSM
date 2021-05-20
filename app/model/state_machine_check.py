from model import dataservice

# 错误信息存储
g_list_error_info = []

class Checker:
    def check(self, data):
        return True

class StateMachineChecker(Checker):
    def check(self, data):
        print("StateMachineChecker::check")
        return True

class BaseCheckDecorator(Checker):
    def __init__(self, checker):
        self.checker_ = checker

    def check(self, data):
        print("BaseCheckDecorator::check")
        return True

class TransNoEventChecker(BaseCheckDecorator):
    """检查状态机中是否存在没有事件发生的迁移"""
    def get_err_dict(self, form, to):
        errItem = {}
        errItem["description"] = "状态机中存在没有事件发生的迁移"
        errItem["transition"] = f'{form} --> {to}'
        return errItem

    def check(self, data):
        print("TransNoEventChecker::check")
        global g_list_error_info
        self.dataServ = dataservice.DataService()
        self.dataServ.dict_data = data
        # 检查逻辑
        for link in self.dataServ.getAllLink():
            if "text" not in link or not link["text"]:
                from_node = self.dataServ.findNodeById(link["from"])
                to_node = self.dataServ.findNodeById(link["to"])
                g_list_error_info.append(self.get_err_dict(from_node["text"], to_node["text"]))

        return self.checker_.check(data)

class NoEntryChecker(BaseCheckDecorator):
    """检查状态机中是否存在状态奇迹"""
    def get_err_dict(self, nodeName):
        errItem = {}
        errItem["description"] = "状态机中存在状态奇迹(只出不进)"
        errItem["state"] = f'状态名称：{nodeName}'
        return errItem

    def check(self, data):
        print("NoEntryChecker::check")
        global g_list_error_info
        self.dataServ = dataservice.DataService()
        self.dataServ.dict_data = data
        # 检查逻辑
        for node in self.dataServ.getAllNode():
            if not self.dataServ.findLinkByToId(node["id"]) and self.dataServ.findLinkByFromId(node["id"]):
                g_list_error_info.append(self.get_err_dict(node["text"]))

        return self.checker_.check(data)

class NoExitChecker(BaseCheckDecorator):
    """检查状态机中是否存在状态黑洞"""
    def get_err_dict(self, nodeName):
        errItem = {}
        errItem["description"] = "状态机中存在状态黑洞(只进不出)"
        errItem["state"] = f'状态名称：{nodeName}'
        return errItem

    def check(self, data):
        print("NoExitChecker::check")
        global g_list_error_info
        self.dataServ = dataservice.DataService()
        self.dataServ.dict_data = data
        # 检查逻辑
        for node in self.dataServ.getAllNode():
            if self.dataServ.findLinkByToId(node["id"]) and not self.dataServ.findLinkByFromId(node["id"]):
                g_list_error_info.append(self.get_err_dict(node["text"]))

        return self.checker_.check(data)
        
class IsolatedStateChecker(BaseCheckDecorator):
    """检查状态机中是否存在孤立的状态"""
    def get_err_dict(self, nodeName):
        errItem = {}
        errItem["description"] = "状态机中存在孤立的状态"
        errItem["state"] = f'状态名称：{nodeName}'
        return errItem

    def check(self, data):
        print("IsolatedStateChecker::check")
        global g_list_error_info
        self.dataServ = dataservice.DataService()
        self.dataServ.dict_data = data
        # 检查逻辑
        for node in self.dataServ.getAllNode():
            if not self.dataServ.findLinkByNodeIdExist(node["id"]):
                g_list_error_info.append(self.get_err_dict(node["text"]))

        return self.checker_.check(data)

class StateMachineCheck:
    def __init__(self):
        global g_list_error_info
        g_list_error_info = []

    def check(self, data):
        checker = StateMachineChecker()
        decorator1 = TransNoEventChecker(checker)
        decorator2 = NoEntryChecker(decorator1)
        decorator3 = NoExitChecker(decorator2)
        decorator4 = IsolatedStateChecker(decorator3)
        decorator4.check(data) # data为状态机数据
        return g_list_error_info

if __name__ == '__main__':
    dict_data = {}
    smc = StateMachineCheck()
    list_error_info = smc.check(dict_data)

    