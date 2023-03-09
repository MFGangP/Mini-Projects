# 주소록 GUI 프로그램 - MySQL 연동

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql

class qtApp(QMainWindow):
    conn = None

    def __init__(self):
        super().__init__()
        uic.loadUi('./Part1/studyPyQt/address_book.ui', self)
        self.setWindowIcon(QIcon('./Part1/studyPyQt/address_book.png'))
   
        self.initDB() # DB 초기화

    def initDB(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db='miniproject', charset='utf8')
        cur = self.conn.cursor()
        query = 'SELECT * FROM addressbook'
        cur.execute(query)
        rows = cur.fetchall()

        print(rows)
        self.conn.close() # 프로그램 종료할 때

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    ex.show()
    sys.exit(app.exec_())