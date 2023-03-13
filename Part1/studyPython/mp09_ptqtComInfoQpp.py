# mp09_ptqtComInfoQpp.py
import sys
import psutil
import socket
import requests # pip install requests
import re

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * # Qt.white ....
from PyQt5.QtGui import *   # QIcon은 여기 있음


class qtApp(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('./Part1/studyPython/comInfo.ui', self)
        self.setWindowTitle('내 컴퓨터 정보 V.0.2')
        self.setWindowIcon(QIcon('./Part1/studyPython/settings.png'))
        self.btnRefresh.clicked.connect(self.btnRefreshClicked)

        self.initInfo()

    def btnRefreshClicked(self):
        self.initInfo()
        
    def initInfo(self):
        cpu = psutil.cpu_freq()
        cpu_ghz = round(cpu.current / 1000 , 2) 
        self.lblCPU.setText(f'{cpu_ghz:.2f} GHz')

        core = psutil.cpu_count(logical=False)
        logical = psutil.cpu_count(logical=True)
        self.lblCore.setText(f'{core} 개 / 논리프로세서 {logical} 개')

        memory = psutil.virtual_memory()
        mem_total = round(memory.total / 1024 ** 3)
        self.lblMemory.setText(f'{mem_total} GB')

        disks = psutil.disk_partitions()
        for disk in disks:
            if disk.fstype == 'NTFS':
                du = psutil.disk_usage(disk.mountpoint)
                du_total = round(du.total / 1024 ** 3)
                msg = f'{disk.mountpoint} {disk.fstype} - {du_total} GB'

                self.lblDisk.setText(msg)
                break
        
        # print(psutil.net_if_addrs())
        in_addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        in_addr.connect(('www.google.com', 443))
        self.lblInnerNet.setText(in_addr.getsockname()[0])  
        # print(in_addr.getsockname()[0])
        
        # 210 = 외부 , 192 = 내부 , 127 = 로컬     
        req = requests.get('http://ipconfig.kr')
        out_Addr = req.text[req.text.find('<font color=red>')+17:req.text.find('</font><br>')]
        self.lblExtraNet.setText(out_Addr)
        
        net_stat = psutil.net_io_counters()
        sent = round(net_stat.bytes_sent / 1024 ** 2, 1)
        recv = round(net_stat.bytes_recv / 1024 ** 2, 1)
        self.lblNetStat.setText(f'송신 - {sent} MB / 수신 - {recv} MB')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    ex.show()
    sys.exit(app.exec_())