import sys, os
from PyQt5.QtWidgets import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.getcwd(), 'controller'))
from controller import layout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = layout.MainLayout()
    main.show()
    sys.exit(app.exec_())