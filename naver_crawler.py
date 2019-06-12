from PyQt5 import QtCore, QtGui, QtWidgets
import re
import requests
import bs4
from openpyxl import load_workbook, Workbook
import os
import urllib.request
import urllib.parse
import urllib, http.cookiejar
import time
import json
import base_crawler as q
import excel as excel
import sys

index = 1
count = 1
img_total = 0
fail_total = 0
cj = http.cookiejar.LWPCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)
opener.addheaders = [
        ('User-Agent',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

    ]
urllib.request.install_opener(opener)
site = "https://blog.naver.com"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 465)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.url = QtWidgets.QLineEdit(self.centralwidget)
        self.url.setGeometry(QtCore.QRect(70, 60, 301, 41))
        self.url.setObjectName("lineEdit")

        self.a_variable = QtWidgets.QLineEdit(self.centralwidget)
        self.a_variable.setGeometry(QtCore.QRect(410, 60, 301, 41))
        self.a_variable.setObjectName("lineEdit_2")

        self.project_name = QtWidgets.QLineEdit(self.centralwidget)
        self.project_name.setGeometry(QtCore.QRect(70, 180, 301, 41))
        self.project_name.setObjectName("lineEdit_3")

        self.page = QtWidgets.QLineEdit(self.centralwidget)
        self.page.setGeometry(QtCore.QRect(410, 180, 301, 41))
        self.page.setObjectName("lineEdit_4")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 15, 301, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(410, 20, 301, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 140, 301, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 140, 301, 31))
        self.label_4.setObjectName("label_4")

        self.href_btn = QtWidgets.QPushButton(self.centralwidget)
        self.href_btn.setGeometry(QtCore.QRect(70, 260, 640, 51))
        self.href_btn.clicked.connect(self.project_href_event)

        self.crawling_btn = QtWidgets.QPushButton(self.centralwidget)
        self.crawling_btn.setGeometry(QtCore.QRect(70, 320, 640, 51))
        self.crawling_btn.clicked.connect(self.N_crawling_event)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def project_href_event(self):
        try:
            test = q.href(self.url.text(),self.a_variable.text())

            if len(test) == 0:
                print("링크가 존재하지않습니다")

            check = []
            for href in test:
                try:
                    project_url = href
                    if 'http' not in href:
                        project_url = "https://blog.naver.com" + href

                    print(project_url)
                    check.append(href)
                except:
                    continue
            print(len(check))
        except Exception as e:
            print(str(e))

    def N_crawling_event(self):
        global index
        global count
        global site
        global img_total
        global fail_total
        img_fail = 0
        img_down = 0
        page = self.page.text()
        page = int(page)
        now = 1
        name = self.project_name.text()
        folder_idx = "1"
        numpath = folder_idx + "." + name + "_사진자료/"
        if not os.path.isdir(numpath):
            os.mkdir(numpath)
        excel.create_excel(folder_idx, name)
        excel_data = []
        title = ""
        addr = ""
        category1 = ""
        category2 = ""
        attribute1 = ""
        attribute2 = ""
        attribute3 = ""
        hashtag = ""
        img_url = ""
        project_url = ""
        src = ""
        else_text = ""

        try:
            url = self.url.text()
            a_variable = self.a_variable.text()

            print("크롤링을 시작합니다")

            while now <= page:

                test = q.href(url.format(now), a_variable)
                for href in test:
                    project_url = href
                    if 'http' not in href:
                        project_url = site + href
                    title = q.content(project_url, "title", "", "").replace("： 네이버 블로그","").strip()

                    img_data = []

                    image1, images1 = q.src(project_url, "_photoImage", "data-lazy-src")
                    image2, images2 = q.src(project_url, "se-image-resource", "data-lazy-src")
                    image3, images3 = q.src(project_url, "se_mediaImage __se_img_el", "data-lazy-src")

                    if images1 != 0:
                        for src in image1:
                            img_data.append(src)

                    if images2 != 0:
                        for src in image2:
                            img_data.append(src)
                    if images3 != 0:
                        for src in image3:
                            img_data.append(src)

                    images = len(img_data)

                    for src in img_data:
                        try:
                            if 'http' not in src:
                                src = site + src

                            kor_src = q.img_name_kor3(src)
                            try:
                                img_url = q.wb_img_down(folder_idx, name, src, title, category1, category2,
                                                        attribute1, attribute2,
                                                        index)
                                img_down += 1
                            except:
                                try:

                                    img_url = q.wb_img_down(folder_idx, name, kor_src, title, category1, category2,
                                                            attribute1,
                                                            attribute2, index)
                                    img_down += 1
                                except Exception as e:
                                    img_fail += 1
                                    f = open(name + "_log.txt", 'a')
                                    f.write(str(e))
                                    f.write('\n')
                                    f.close()
                                    continue

                                # 리스트에 데이터 추가
                            excel_data.append([
                                str(index),
                                name,
                                title,
                                addr,
                                category1,
                                category2,
                                attribute1,
                                attribute2,
                                attribute3,
                                hashtag,
                                img_url,
                                project_url,
                                src,
                                else_text
                            ])
                            index += 1
                        except:
                            continue

                    img_total += img_down
                    fail_total += img_fail
                    q.title(now, title, count, project_url, images, img_down, img_fail, img_total, fail_total)
                    count += 1
                    img_down = 0
                    img_fail = 0

                count = 1
                now += 1
                # 엑셀에 리스트기반으로 저장
                excel.data_save(folder_idx, name, excel_data)
                excel_data = []

            print("크롤링을 종료합니다")

        except Exception as e:
            print(str(e))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "홈페이지 주소"))
        self.label_2.setText(_translate("MainWindow", "링크 변수"))
        self.label_3.setText(_translate("MainWindow", "회사 이름"))
        self.label_4.setText(_translate("MainWindow", "페이지"))
        self.href_btn.setText(_translate("MainWindow", "프로젝트 링크확인"))
        self.crawling_btn.setText(_translate("MainWindow", "크롤링 시작"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
