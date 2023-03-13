# QRCODE PyQt App
import qrcode
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * # Qt.white ....
from PyQt5.QtGui import *   # QIcon은 여기 있음

class qtApp(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('./Part1/studyPython/qrcodeApp.ui', self)
        self.setWindowTitle('QrCode 생성앱 V.0.1')
        self.setWindowIcon(QIcon('./Part1/studyPython/QRCode.png'))
        
        # 시그널 / 슬롯
        self.btnQrGen.clicked.connect(self.btnQrGenClicked)
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked)

    def btnQrGenClicked(self):
        data = self.txtQrData.text()

        if data == '':
            QMessageBox.warning(self, '경고', '데이터를 입력하세요')
            return
        else:
            qr_img = qrcode.make(data)
            qr_img.save('./Part1/studyPython/site.png')

            img = QPixmap('./Part1/studyPython/site.png')
            self.lblQrCode.setPixmap(QPixmap(img).scaledToWidth(300))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    ex.show()
    sys.exit(app.exec_())