# PyQt에 folium 지도 표시
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import pandas as pd
import sys
import io # 파일 저장
import folium
import mp24_universityLoc

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('전국대학교 위치')
        self.width, self.height = 1400, 900
        self.setMinimumSize(self.width, self.height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        filePath = 'C:/Source/Mini-Projects/Part1/studyPython/university_locations.xlsx'
        df_excel = pd.read_excel(filePath, engine='openpyxl', header=None)
        df_excel.columns = ['학교명', '주소', 'lng', 'lat']

        # print(df_excel)
        name_list = df_excel['학교명'].to_list()
        addr_list = df_excel['주소'].to_list()
        lng_list = df_excel['lng'].to_list()
        lat_list = df_excel['lat'].to_list()

        # url = 'https://www.naver.com'
        m = folium.Map(location=[37.553175, 126.989326], zoom_start=10)
        
        for i in range(len(name_list)):# 446
            if lng_list[i] != 0: # 위,경도값이 0이 아니면 출력 안된다.
                marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i],
                                        icon=folium.Icon(color='blue'))
                marker.add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        # webView.load(QUrl(url))
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    ex.show()
    sys.exit(app.exec_())