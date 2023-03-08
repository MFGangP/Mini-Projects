# Qt Designer 디자인 사용

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverApi import *
from urllib.request import urlopen, Request
import webbrowser # 웹 브라우저 모듈

class qtApp(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('./Part1/studyPyQt/naverApiMovie.ui', self)
        self.setWindowIcon(QIcon('./Part1/studyPyQt/newspaper.png'))

        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 텍스트 박스에 검색어 입력 후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '영화명를 입력하세요!')
            return
        else:
            api = NaverApi() # NaverApi 클래스 객체 생성
            node = 'movie' # movie로 변경하면 영화 검색
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result) 개발 할 때만 쓰는거
            # 테이블 위젯에 출력하는 기능
            items = result['items'] # json결과 중에서 items 아래 배열만 추출
            self.makeTable(items) # 테이블 위젯에 데이터들을 할당 함수    

    def txtSearchReturned(self):
        self.btnSearchClicked() 

    def tblResultDoubleClicked(self):
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 5).text() # url 링크 컬럼 변경
        webbrowser.open(url) # 네이버 영화 웹사이트

    # 테이블 위젯에 데이터 표시 -- 네이버 영화 결과에 맞춰 변경
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일 선택만 되게 만듦
        self.tblResult.setColumnCount(7) # 컬럼 갯수 변경
        self.tblResult.setRowCount(len(items)) # 현재 100개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목','개봉년도', '감독', '배우진', '평점', '링크', '포스터'])
        # 컬럼 크기 조절
        self.tblResult.setColumnWidth(0, 150) # 영화제목
        self.tblResult.setColumnWidth(1, 60) # 개봉년도
        self.tblResult.setColumnWidth(4, 50) # 평점
        # 컬럼 데이터를 수정 금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 영화
            title = self.replaceHtmlTag(post['title']) # HTML 특수문자 변환
            pubDate = post['pubDate']
            director = post['director']
            actor = post['actor']
            userRating = post['userRating'] 
            link = post['link']
            image = QImage(requests.get(post['image'], stream=True), width=100)
            imgData = urlopen(post['image']).read()
            image = QPixmap()
            if imgData != None:
                image.loadFromData(imgData)
                imgLabel = QLabel()
                imgLabel.setPixmap(image)
                imgLabel.setGeometry(0, 0, 60, 100)
                imgLabel.resize(60, 100)

            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            if imgData != None:
                self.tblResult.setCellWidget(i, 6, imgLabel)

    def replaceHtmlTag(self, sentence) -> str:
        result = sentence.replace('&lt;','<') # lesser then 작다
        result = result.replace('&gt;', '>') # greater then 크다
        result = result.replace('<b>', '') # bold
        result = result.replace('</b>', '') # b
        result = result.replace('&apos;', "'") # apostropy 홑따옴표
        result = result.replace('&quot;', '"') # quotation mark 쌍따옴표
        # 줄여서 써도 되고 늘려서 써도 되고
        # 변환 안된 특수문자가 나타날 때 마다 추가
        return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp() # 지난 번에 MyApp()
    ex.show()
    sys.exit(app.exec_())