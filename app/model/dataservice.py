import json, re
import conf

# 数据样例
dict_data_temp = {
    "nodeKeyProperty": "id",
    "nodeDataArray": [
        {"id": -1, "category": "Start"},
        {"id": 0, "text": "State1", "detail": "State1 info"},
        {"id": 1, "text": "State2", "detail": "State2 info"},
        {"id": -2, "category": "End"}
    ],
    "linkDataArray": [
        {"from": -1, "to": 0, "text": "next"},
        {"from": 0, "to": 1,  "progress": "false", "text": "next"},
        {"from": 0, "to": -2,  "progress": "true", "text": "next"},
        {"from": 1, "to": -2,  "progress": "true", "text": "next"}
    ]
}

class DataService:
    pattern_varName = r'[ 0-9a-zA-Z_\[\]*]+'
    dict_pattern = {
        "global": r'global[ ]+::[ ]+"(.*)"\n',
        "node": r'(%s)[ ]+:[ ]+"(.*)"\n' % pattern_varName,
        "link": r'(%s)[ ]+[-]{1,2}>[ ]+(%s)([ ]+:[ ]+".*"){0,1}\n' % (pattern_varName, pattern_varName),
        "title": r'(%s)[ ]+=[ ]+"(.*)"\n' % pattern_varName,
        "nattr": r'(%s)[ ]+<<[ ]+"(.*)"\n' % pattern_varName,
    }
    dict_data = {
        "nodeKeyProperty": "id",
        "nodeDataArray": [],
        "linkDataArray": []
    }

    def getDefaultText(self):
        with open(conf.arg.default_text, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def setDefaultText(self, text):
        with open(conf.arg.default_text, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def getDefaultJson(self):
        with open(conf.arg.default_json, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def setDefaultJson(self, text):
        with open(conf.arg.default_json, 'w', encoding='utf-8') as f:
            f.write(text)

    def clearData(self):
        self.dict_data = {
            "nodeKeyProperty": "id",
            "nodeDataArray": [],
            "linkDataArray": []
        }

    def plantUmltoGojs(self, code):
        self.clearData()

        # 处理link数据
        pattern = re.compile(self.dict_pattern["link"])  # 查找连线
        linkData = pattern.findall(code)
        print(linkData)

        for link in linkData:
            fromNode = link[0]
            toNode = link[1]
            trans = link[2].lstrip(' ').lstrip(':').lstrip(' ').strip('"')
            fromId = self.addNode(fromNode)
            toId = self.addNode(toNode)
            self.addLink(fromId, toId, trans)

        # 处理global数据
        pattern = re.compile(self.dict_pattern["global"])  # 查找节点信息
        globalData = pattern.findall(code)
        print(globalData)

        for info in globalData:
            self.setGlobal(info)

        # 处理node数据
        pattern = re.compile(self.dict_pattern["node"])  # 查找节点信息
        nodeData = pattern.findall(code)
        print(nodeData)

        for node in nodeData:
            nodeName = node[0]
            detail = node[1]
            self.setDetail(nodeName, detail)

        # 处理title数据
        pattern = re.compile(self.dict_pattern["title"])  # 查找名字信息
        titleData = pattern.findall(code)
        print(titleData)

        for title in titleData:
            nodeName = title[0]
            title = title[1]
            self.setTitle(nodeName, title)

        # 处理node attr数据
        pattern = re.compile(self.dict_pattern["nattr"])  # 查找节点属性信息
        nattrData = pattern.findall(code)
        print(nattrData)

        for nattr in nattrData:
            nodeName = nattr[0]
            nattr = nattr[1]
            self.setNattr(nodeName, nattr)

        return json.dumps(self.dict_data)

    def mergeTo(self, dict_data):
        target = DataService()
        target.dict_data = dict_data

        # 编辑node
        for node in self.dict_data["nodeDataArray"]:
            t_node = target.findNode(node["text"])
            if t_node:
                for k, v in node.items():
                    t_node[k] = v

        # 编辑link
        for link in self.dict_data["linkDataArray"]:
            t_link = target.findLink(link["from"], link["to"])
            if t_link:
                t_link["text"] = link["text"]

        # 编辑global
        if 'global' not in target.dict_data:
            target.dict_data['global'] = {}
        for k, v in self.getGlobal().items():
            target.dict_data["global"][k] = v

        dict_data = target.dict_data

    def addNode(self, nodeName):
        # 若结点存在则直接返回Id
        node = self.findNode(nodeName)
        if node:
            return node["id"]

        # 添加结点
        nodeNum = len(self.dict_data["nodeDataArray"])
        nodeId = nodeNum + 1
        node = {"id": nodeId, "text": nodeName}
        if nodeName == '[Start]':
            node["category"] = 'Start'
            node["title"] = 'START'
        if nodeName == '[End]':
            node["category"] = 'End'
            node["title"] = 'END'
        self.dict_data["nodeDataArray"].append(node)
        return nodeId

    def addLink(self, fromId, toId, trans):
        self.dict_data["linkDataArray"].append({"from": fromId, "to": toId,  "progress": "false", "text": trans})

    def getAllNode(self):
        return self.dict_data["nodeDataArray"]

    def getAllLink(self):
        return self.dict_data["linkDataArray"]
    
    def getAllLinkByNodeName(self, nodeName):
        links = []
        node = self.findNode(nodeName)
        if not node:
            return links
        # 找node所有出度link
        nodeId = node["id"]
        for link in self.dict_data["linkDataArray"]:
            if link["from"] == nodeId:
                links.append(link)
        return links

    def findNode(self, nodeName):
        for node in self.dict_data["nodeDataArray"]:
            if node["text"] == nodeName:
                return node
        return None

    def findNodeById(self, id):
        for node in self.getAllNode():
            if node['id'] == id:
                return node
        return None

    def findNodesByLinkText(self, linkText, point='from'):
        list_node = []
        for link in self.dict_data["linkDataArray"]:
            if link["text"] == linkText:
                link_point = link[point]
                node = self.findNodeById(link_point)
                if 'title' in node.keys():
                    list_node.append(node)
        return list_node

    def findLink(self, fromId, toId):
        for link in self.dict_data["linkDataArray"]:
            if link["from"] == fromId and link["to"] == toId:
                return link
        return None

    def findLinkByFromId(self, fromId):
        list_links = []
        for link in self.dict_data["linkDataArray"]:
            if link["from"] == fromId:
                list_links.append(link)
        return list_links

    def findLinkByToId(self, toId):
        list_links = []
        for link in self.dict_data["linkDataArray"]:
            if link["to"] == toId:
                list_links.append(link)
        return list_links

    def findLinkByNodeIdExist(self, nodeId):
        for link in self.dict_data["linkDataArray"]:
            if (link["from"] == nodeId or link["to"] == nodeId) and link["from"] != link["to"]:
                return True
        return False

    def setDetail(self, nodeName, detail):
        for node in self.dict_data["nodeDataArray"]:
            if node["text"] == nodeName:
                node["detail"] = detail

    def setTitle(self, nodeName, title):
        for node in self.dict_data["nodeDataArray"]:
            if node["text"] == nodeName:
                node["title"] = title
    
    def setNattr(self, nodeName, nattr):
        dict_nattr = self.getDict(nattr)
        for node in self.dict_data["nodeDataArray"]:
            if node["text"] == nodeName:
                for k, v in dict_nattr.items():
                    node[k] = v
    
    def getGlobal(self):
        if 'global' not in self.dict_data:
            self.dict_data['global'] = {}
        return self.dict_data['global']

    def setGlobal(self, info):
        if 'global' not in self.dict_data:
            self.dict_data['global'] = {}
        dict_info = self.getDict(info)
        for k, v in dict_info.items():
            self.dict_data["global"][k] = v

    def getDict(self, str_kv):
        list_kvs = str_kv.split(',')
        dist_detail = {}
        for kv in list_kvs:
            list_kv = kv.split(':')
            dist_detail[list_kv[0]] = list_kv[1]
        return dist_detail

if __name__ == '__main__':
    print(DataService().plantUmltoGojs('test'))
