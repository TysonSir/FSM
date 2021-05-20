from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import *
import os, json, zipfile, time

from model import dataservice
from model import trans_conflict_check as TCC
from model import state_machine_check as SMC
from model import generate_code as GC
from controller import textbox
import conf

class MainLayout(QMainWindow):
    dataserv = dataservice.DataService()

    def __init__(self):
        super(MainLayout, self).__init__()
        self.base_title = "形式化状态图 [v0.3] "
        self.setWindowTitle(self.base_title)
        self.resize(1300, 810)

        self.initUI()
        self.connSlot()

    def initData(self, proj_path):
        # 设置路径+解压文件
        conf.arg.set_default_project(proj_path)
        self.unzipProject(proj_path)
        # 更新界面
        self.code.setText(self.dataserv.getDefaultText())
        self.actSetJsonOnClick()
        self.setWindowTitle(self.base_title + proj_path)

    def initMenu(self):
        # 创建Action
        self.actNew = QAction("新建")
        self.actOpen = QAction("打开")
        self.actSave = QAction("保存")
        self.actSaveAs = QAction("另存为")
        self.actDraw = QAction("渲染")
        self.actGetJson = QAction("导出json")
        self.actSetJson = QAction("导入json")
        self.actHistory = QAction("历史版本")
        self.actTransConflict = QAction("迁移冲突检查")
        self.actCheck = QAction("检查")
        self.actUpdate = QAction("更新")
        self.actGenerateCode = QAction("生成代码")

        # 菜单栏
        # bar = self.menuBar()  # 获取菜单栏
        # edit = bar.addMenu("编辑")
        # edit.addAction(self.actOpen)

        #工具栏
        tool = self.addToolBar("Tool")
        tool.addAction(self.actNew)
        tool.addAction(self.actOpen)
        tool.addAction(self.actSave)
        tool.addAction(self.actSaveAs)
        tool.addAction(self.actDraw)
        tool.addAction(self.actGetJson)
        tool.addAction(self.actSetJson)
        tool.addAction(self.actHistory)
        tool.addAction(self.actTransConflict)
        tool.addAction(self.actCheck)
        tool.addAction(self.actUpdate)
        tool.addAction(self.actGenerateCode)
        tool.setToolButtonStyle(Qt.ToolButtonTextOnly)

    def initUI(self):
        self.initMenu()

        self.code = QTextEdit()

        self.url = os.getcwd() + '/view/stateChart.html'
        self.urlc = os.getcwd() + '/view/stateChart_CLayout.html'
        self.browser = QWebEngineView()
        self.browser.load(QUrl.fromLocalFile(self.url))

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.code)
        splitter.addWidget(self.browser)
        splitter.setSizes([400, 900])

        hbox = QHBoxLayout()
        hbox.addWidget(splitter)

        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)

    def connSlot(self):
        # 新建工程
        self.actNew.triggered.connect(self.actNewOnClick)
        # 打开工程
        self.actOpen.triggered.connect(self.actOpenOnClick)
        # 保存工程
        self.actSave.triggered.connect(self.actSaveOnClick)
        # 另存为工程
        self.actSaveAs.triggered.connect(self.actSaveAsOnClick)
        # 绘制图形
        self.actDraw.triggered.connect(self.actDrawOnClick)
        # 获取Json数据
        self.actGetJson.triggered.connect(self.actGetJsonOnClick)
        # 导入Json数据
        self.actSetJson.triggered.connect(self.actSetJsonOnClick)
        # 更新数据
        self.actUpdate.triggered.connect(self.actUpdateOnClick)
        # 迁移冲突检查
        self.actTransConflict.triggered.connect(self.actTransConflictOnClick)
        # 状态图检查
        self.actCheck.triggered.connect(self.actCheckOnClick)
        # 创建代码
        self.actGenerateCode.triggered.connect(self.actGenerateCodeOnClick)

    def resizeEvent(self, e):
        # 改变窗口大小响应事件
        print("w = {0}; h = {1}".format(e.size().width(), e.size().height()))

        winMenuHeight = 37
        divHeight = e.size().height() - 110
        divHeight += winMenuHeight # 有菜单时去掉此行
        self.browser.page().runJavaScript('setMyDiagramDivHeight(%d);' % divHeight)

        QtWidgets.QWidget.resizeEvent(self, e)

    def encodeJsonString(self, gojs, escape='\\'):
        return gojs.replace('\\', escape).replace('"', '\\"').replace('\n', '\\n')

    def unzipProject(self, proj_path):
        zip_file = zipfile.ZipFile(proj_path)
        zip_list = zip_file.namelist() # 得到压缩包里所有文件

        for f in zip_list:
            zip_file.extract(f, conf.arg.text_model_dir) # 循环解压文件到指定目录
        
        zip_file.close() # 关闭文件，必须有，释放内存

    def actNewOnClick(self):
        print('actNewOnClick')
        default_text = """@startuml

# 0.global（全局属性）
global :: "StateName:BuilderState"
global :: "ClassName:HttpConnectionBuilder"

# 1.link（迁移）
[Start] --> StateA : "transitionOne"
StateA --> StateB : "transitionTwo"
StateB --> [End] : "transitionThree"

# 2.title（状态名）
StateA = "AAA"
StateB = "BBB"

# 3.detail（状态注释）
StateA : "状态A"
StateB : "状态B"

# 4.nattr（设置节点属性）
StateA << "bcolor:yellow"
StateB << "text_color:green,title_color:red,detail_color:blue"

@enduml
"""
        self.code.setText(default_text)
        self.actDrawOnClick()

    def actOpenOnClick(self):
        print('actOpenOnClick')
        select_filepath, ok = QFileDialog.getOpenFileName(self, "打开文件",
                                                        ".", # 默认当前路径
                                                        "FSM Files (*.fsm);;All Files (*)")
        if ok:
            self.initData(select_filepath)

    def getModelJson_callback_for_save(self, result):
        print(result)
        # 预处理
        dict_data = json.loads(result)

        # 状态图数据
        json_data = json.dumps(dict_data, indent=4)
        self.dataserv.setDefaultJson(json_data)

        # 标记语言数据
        code = self.code.toPlainText()
        self.dataserv.setDefaultText(code)

        # 压缩文件
        newZip = zipfile.ZipFile(conf.arg.default_project, 'w')
        newZip.write(conf.arg.default_text, os.path.basename(conf.arg.default_text), compress_type=zipfile.ZIP_DEFLATED)
        newZip.write(conf.arg.default_json, os.path.basename(conf.arg.default_json), compress_type=zipfile.ZIP_DEFLATED)
        newZip.close()

    def actSaveOnClick(self):
        print('actSaveOnClick')
        self.browser.page().runJavaScript('getModelJson();', self.getModelJson_callback_for_save)

    def actSaveAsOnClick(self):
        print('actSaveAsOnClick')
        select_filepath, ok = QFileDialog.getSaveFileName(self, "保存文件",
                                                        ".", # 默认当前路径
                                                        "FSM Files (*.fsm);;All Files (*)")
        if ok:
            conf.arg.set_default_project(select_filepath)
            self.setWindowTitle(self.base_title + select_filepath)
            self.browser.page().runJavaScript('getModelJson();', self.getModelJson_callback_for_save)

    def actDrawOnClick(self):
        print('actDrawOnClick')
        code = self.code.toPlainText()
        gojs = self.dataserv.plantUmltoGojs(code)
        gojs = self.encodeJsonString(gojs)
        print(gojs)
        self.browser.page().runJavaScript('setModel("' + gojs + '");')

    def getModelJson_callback(self, result):
        print(result)
        # 预处理
        dict_data = json.loads(result)
        # for link in dict_data["linkDataArray"]:
        #     link['points'] = []

        # 对话框中显示
        json_data = json.dumps(dict_data, indent=4)
        self.dataserv.setDefaultJson(json_data)
        self.textBox = textbox.TextBox('已导出 图形Json数据', json_data)
        self.textBox.readOnly()
        self.textBox.exec_()

    def actGetJsonOnClick(self):
        print('actGetJsonOnClick')
        self.browser.page().runJavaScript('getModelJson();', self.getModelJson_callback)

    def actSetJsonOnClick(self):
        print('actSetJsonOnClick')
        gojs = self.dataserv.getDefaultJson()
        gojs = self.encodeJsonString(gojs, escape='\\\\')
        print(gojs)
        self.browser.page().runJavaScript('setModel("' + gojs + '");')

    def getModelJson_callback_for_update(self, result):
        print(result)
        # 界面数据
        dict_data = json.loads(result)

        # 脚本数据
        code = self.code.toPlainText()
        self.dataserv.plantUmltoGojs(code)

        # 脚本数据 合并到 界面数据
        self.dataserv.mergeTo(dict_data)

        # 刷新界面数据
        gojs = json.dumps(dict_data)
        gojs = self.encodeJsonString(gojs)
        self.browser.page().runJavaScript('setModel("' + gojs + '");')

    def actUpdateOnClick(self):
        print('actUpdateOnClick')
        self.browser.page().runJavaScript('getModelJson();', self.getModelJson_callback_for_update)

    def getModelJson_callback_for_TransConflict_check(self, result):
        print(result)
        # 界面数据
        dict_data = json.loads(result)
        # 检查
        tcc = TCC.TransConflictCheck()
        list_error_info = tcc.check(dict_data)
        json_data = json.dumps(list_error_info, indent=4, ensure_ascii=False)
        # 输出结果
        self.textBox = textbox.TextBox('状态冲突错误检查结果', json_data)
        self.textBox.readOnly()
        self.textBox.exec_()

    def actTransConflictOnClick(self):
        print('actTransConflictOnClick')
        self.browser.page().runJavaScript('getModelJson();', self.getModelJson_callback_for_TransConflict_check)

    def getModelJson_callback_for_check(self, result):
        print(result)
        # 界面数据
        dict_data = json.loads(result)
        # 检查
        smc = SMC.StateMachineCheck()
        list_error_info = smc.check(dict_data)
        json_data = json.dumps(list_error_info, indent=4, ensure_ascii=False)
        # 输出结果
        self.textBox = textbox.TextBox('错误检查结果', json_data)
        self.textBox.readOnly()
        self.textBox.exec_()

    def actCheckOnClick(self):
        print('actCheckOnClick')
        self.browser.page().runJavaScript('getModelJson();', self.getModelJson_callback_for_check)

    def getModelJson_callback_for_gen_code(self, result):
        # 界面数据
        dict_data = json.loads(result)

        # 生成代码
        gc = GC.GenerateCode(dict_data)
        code = gc.generate()

        # 输出结果
        self.textBox = textbox.TextBox('生成的代码', code)
        self.textBox.readOnly()
        self.textBox.exec_()

    def actGenerateCodeOnClick(self):
        print('actGenerateCodeOnClick')
        self.browser.page().runJavaScript('getModelJson();', self.getModelJson_callback_for_gen_code)

