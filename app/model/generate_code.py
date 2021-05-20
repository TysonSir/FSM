from model import dataservice
from jinja2 import Template
import os
import conf

class GenerateCode:
    def __init__(self, dict_data):
        self.dict_data = dict_data
        self.dataServ = dataservice.DataService()
        self.dataServ.dict_data = dict_data

    def generate(self):
        dict_state_info = {'StateName': self.dataServ.getGlobal()['StateName'] if 'StateName' in self.dataServ.getGlobal() else 'StateEnum'}
        dict_state_info['StateList'] = self.getAllState()

        dict_class_info = {'ClassName': self.dataServ.getGlobal()['ClassName'] if 'ClassName' in self.dataServ.getGlobal() else 'StateMachineClass'}
        dict_func = {}
        for action, dict_point in self.getAllTrans().items():
            list_from_state = dict_point['from']
            list_from_state = ['state_ == %s' % state for state in list_from_state]
            dict_func[action] = {}
            dict_func[action]['from'] = ' || '.join(list_from_state)
            dict_func[action]['to'] = ' | '.join(dict_point['to'])
        dict_class_info['FuncInfo'] = dict_func

        code = self.renderTemplate('cpp_template.cpp', dict_state_info=dict_state_info, dict_class_info=dict_class_info)
        return code

    def getAllTrans(self):
        list_action = []
        for link in self.dataServ.getAllLink():
            action = link['text']
            list_action.append(action)
        set_action = set(list_action)
        if '' in set_action:
            set_action.remove('')

        dict_action = {}
        for action in set_action:
            dict_action[action] = {'from': [node['title'] for node in self.dataServ.findNodesByLinkText(action, 'from')]}
            dict_action[action]['to'] = [node['title'] for node in self.dataServ.findNodesByLinkText(action, 'to')]
            dict_action[action]['to'] = list(set(dict_action[action]['to'])) # 去重复
        return dict_action

    def getAllState(self):
        list_state = []
        for node in self.dataServ.getAllNode():
            if 'title' in node:
                stateName = node['title']
                list_state.append(stateName)
        return list_state

    def renderTemplate(self, temp_file, **data):
        filepath = os.path.join(conf.arg.code_template_dir, temp_file)
        file_content = ''
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()

        template = Template(file_content)
        return template.render(**data)
