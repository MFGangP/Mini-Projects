# 스레드 미사용 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * # Qt.white ....
from PyQt5.QtGui import *   # QIcon은 여기 있음

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Part1/studyThread/threadApp.ui', self)
        self.setWindowTitle('노 쓰레드 앱 v0.1')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)

    def btnStartClicked(self):
        self.pgbTask.setRange(0, 999999)
        for i in range(0, 1000000): # 0 ~ 100
            print(f'노스레드 출력 > {i}')
            self.pgbTask.setValue(i)
            self.txbLog.append(f'노스레드 출력 > {i}')
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    ex.show()
    sys.exit(app.exec_())