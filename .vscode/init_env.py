import os
import common

workspaceFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    common.exec_cmd(workspaceFolder, 'pip install PyQt5')
    common.exec_cmd(workspaceFolder, 'pip install PyQtWebEngine')
    common.exec_cmd(workspaceFolder, 'pip install z3-solver')
    common.exec_cmd(workspaceFolder, 'pip install jinja2')
    common.exec_cmd(workspaceFolder, 'pip install pyinstaller')