'''

拖动控件之间的边界（QSplitter）

'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Splitter(QWidget):
    def __init__(self):
        super(Splitter, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QSplitter 例子')
        self.resize(1300, 810)
        # self.setGeometry(300, 300, 300, 200)

        left = QTextEdit()

        right = QFrame()
        right.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([400, 900])

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter)
        self.setLayout(hbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Splitter()
    demo.show()
    sys.exit(app.exec_())

