from z3 import *
from model import dataservice
import re

class Trans:
    def __init__(self, text):
        self.text = text
        list_info = text.split(':', 1)
        self.priority = list_info[0].strip() # 优先级
        self.condition = list_info[1].strip() # 表达式
class ErrItem:
    def __init__(self):
        self.transA = ''
        self.transB = ''
        self.explain = ''

    def getDict(self):
        return {"transA": self.transA, "transB": self.transB, "explain": self.explain}

    def __str__(self):
        return str(self.getDict())

class ErrorInfo:
    def __init__(self, description):
        self.nodeText = ''
        self.description = description
        self.list_err = [] # ErrItem
    
    def getDict(self):
        return {"nodeName": self.nodeText, "description": self.description, "list_err": self.list_err}
    
    def __str__(self):
        return str(self.getDict())

class TransConflictCheck:
    def __init__(self):
        self.description = '状态迁移冲突检查'

    def check(self, dict_data):
        list_error_info = []
        self.dataServ = dataservice.DataService()
        self.dataServ.dict_data = dict_data

        for node in self.dataServ.getAllNode():
            errorInfo = self.checkNode(node)
            if len(errorInfo.list_err) > 0:
                list_error_info.append(errorInfo.getDict())
        return list_error_info
    
    def checkNode(self, node):
        eInfo = ErrorInfo(self.description)
        eInfo.nodeText = node["text"]

        links = self.dataServ.getAllLinkByNodeName(node["text"])
        for pair in self.createLinkPair(links):
            trans1 = Trans(pair[0]["text"])
            trans2 = Trans(pair[1]["text"])
            if trans1.priority != trans2.priority:
                continue # 优先级不同，不冲突
            explain = self.checkTrans(trans1.condition, trans2.condition)
            if explain != '':
                ei = ErrItem()
                ei.explain = explain
                ei.transA = trans1.text
                ei.transB = trans2.text
                eInfo.list_err.append(ei.getDict())
        return eInfo


    def createLinkPair(self, links):
        list_link_pairs = []
        link_num = len(links)
        if link_num <= 1:
            return list_link_pairs

        for i in range(link_num-1):
            for j in range(i+1, link_num):
                list_link_pairs.append((links[i], links[j]))
        return list_link_pairs

    def checkTrans(self, condition1, condition2):
        Activate = Bool('Activate')
        S_ChannelA = Bool('S_ChannelA')
        S_ChannelB = Bool('S_ChannelB')
        Timer = Int('Timer')
        DiscrepancyTime = Int('DiscrepancyTime')

        s = Solver()
        z3_cond1 = self.change_format(condition1)
        z3_cond2 = self.change_format(condition2)
        s.add(eval(z3_cond1), eval(z3_cond2))
        ret = s.check()
        if ret == sat:
            return str(s.model())
        else:
            return ''
    
    # 词法分析
    def process_logic(self, expr):
        def change(matched):
            dict_keys = {'&': 'And', 'XOR': 'Or'}
            left = matched.group(1)
            logic = matched.group(2)
            right = matched.group(3)
            return '{}({},{})'.format(dict_keys[logic], left, right)
        
        result = re.sub('(.*)(&|XOR)(.*)', change, expr)
        return result

    def process_not(self, expr):
        def change(matched):
            exp = matched.group(1)
            return 'Not({})'.format(exp)
        
        result = re.sub('!(\w+)', change, expr)
        return result

    def change_format(self, expr):
        if not ('&' in expr or 'XOR' in expr or '!' in expr):
            return expr
        expr = expr.replace(' ', '')
        expr = self.process_logic(expr)
        expr = self.process_not(expr)
        return expr
