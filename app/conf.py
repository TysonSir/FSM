import os, json

class Config:
    def __init__(self):
        with open('config.json', 'r', encoding='utf-8') as f:
            dict_config = json.load(f)
        self.code_template_dir = os.path.abspath(dict_config['code_template_dir'])
        self.text_model_dir = os.path.abspath(dict_config['text_model_dir'])

        self.set_default_project(dict_config['default_project'])
    
    def set_default_name(self, proj_name):
        self.default_text = os.path.join(self.text_model_dir, proj_name + '.txt')
        self.default_json = os.path.join(self.text_model_dir, proj_name + '.json')

    def set_default_project(self, project_path):
        self.default_project = os.path.abspath(project_path)
        self.set_default_name(os.path.basename(project_path).replace('.fsm', ''))

arg = Config()
