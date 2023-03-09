# 주소록 GUI 프로그램 - MySQL 연동

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class qtApp(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('./Part1/studyPyQt/address_book.ui', self)
        self.setWindowIcon(QIcon('./Part1/studyPyQt/address_book.png'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    ex.show()
    sys.exit(app.exec_())