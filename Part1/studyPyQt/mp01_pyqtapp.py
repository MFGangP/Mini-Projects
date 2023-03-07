# PyQt 복습 - 직접 디자인 코딩
import sys
from PyQt5.QtWidgets import *

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 얘는 밖에서 쓸거임
        self.lblMessage = QLabel('메시지 : ', self)
        self.lblMessage.setGeometry(10, 10, 300, 50)
        # sizeIncrement
        # 얘는 안에서만 쓸거임
        btnOk = QPushButton('OK', self)
        btnOk.setGeometry(280, 250, 100, 30)
        # PyQt 이벤트(시그널) -> 이벤트 핸들러(슬롯)
        btnOk.clicked.connect(self.btnOk_clicked)

        self.setGeometry(300, 200, 400, 300)
        self.setWindowTitle('복습 PyQt')
        self.show()

    def btnOk_clicked(self):
        self.lblMessage.clear()
        self.lblMessage.setText('메시지 : OK!!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    sys.exit(app.exec_())
