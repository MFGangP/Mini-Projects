# 스레드 사용 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * # Qt.white ....
from PyQt5.QtGui import *   # QIcon은 여기 있음
import time

MAX = 1000 # 

class BackGroundWorker(QThread): # PyQt5 스레드를 위한 클래스 존재
    procChanged = pyqtSignal(int) # 커스텀 시그널 INT값 받아서 전달
    # 시그널 하나 만든거임 (마우스 클릭 같은 시그널을 따로 만드는 것)
    def __init__(self, count = 0, parent = None) -> None:
        super().__init__()
        self.main = parent
        self.working = False # 스레드 동작여부
        self.count = count # QT앱에서 받은 값 전달

    def run(self): # thread.start() --> run() 대신 실행
        while self.working: # True인 동안
            # emit = 시그널을 내보냄. 값이 바뀔 때 마다
            if self.count <= MAX:
                self.procChanged.emit(self.count) # QT앱에게 내보내겠다.
                self.count += 1 # 값 증가만 // 업무 프로세스 동작하는 위치
                time.sleep(0.001) #1ms 시간 단위로 움직이기 때문에 쪼개줘야한다.
                # 하는 일이 많으면 이런 time.sleep 필요없음
                # 0.0000001 세밀하게 주면 GUI처리를 제대로 못함
                # 1초는 너무 느리다
            else:
                self.working = False # 멈춤

class qtApp(QWidget): # GUI 그래픽 그리는 부분, 실행
    # 위젯의 실제 컨트롤 제어
    def __init__(self):
        super().__init__()
        uic.loadUi('./Part1/studyThread/threadApp.ui', self)
        self.setWindowTitle('쓰레드 앱 v0.1')
        self.pgbTask.setValue(0)
        # 내장 시그널
        self.btnStart.clicked.connect(self.btnStartClicked) # 버튼 클릭하게 되면 어떻게 할래
        # 스레드 생성, 초기화
        self.worker = BackGroundWorker(parent=self, count=0)
        # 백그라운드 워커에 있는 시그널을 접근해서 처리해주기 위한 슬롯함수
        self.worker.procChanged.connect(self.procUpdated)
        # 셀프 워커에서 버튼 클릭 시그널이 생기면 어떻게 할래?
        self.pgbTask.setRange(0, MAX)

    # PyQt
    @pyqtSlot(int) # 데코레이션
    def procUpdated(self, count):
        self.txbLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')

    @pyqtSlot() 
    def btnStartClicked(self):
        self.worker.start() # thread 클래스 안에 있는 run() 실행
        self.worker.working = True # 
        self.worker.count = 0
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    ex.show()
    sys.exit(app.exec_())