import json
import openpyxl
import pandas as pd
import requests
from dateutil.utils import today
from datetime import datetime
import os
import sys
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QPushButton, QMessageBox, QLabel, QTextEdit,  QWidget, QProgressBar
from PyQt5.QtCore import QBasicTimer
7
today = datetime.today().strftime('%Y-%m-%d')
drt = ()
windows_user_name = os.path.expanduser('~')


def get_price_k(code):
    try:
        url = 'http://finance.daum.net/api/charts/A%s/days?limit=%d&adjusted=true' % (code, 90)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
            'Host': 'finance.daum.net',
            'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
            'Referer': 'http://finance.daum.net/quotes/A069500',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        headers['Referer'] = 'http://finance.daum.net/quotes/A%s' % code
        r = requests.get(url, headers=headers)

        url_1000 = 'http://finance.daum.net/api/charts/A%s/days?limit=%d&adjusted=true' % (code, 1000)
        headers_1000 = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
            'Host': 'finance.daum.net',
            'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
            'Referer': 'http://finance.daum.net/quotes/A069500',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        headers_1000['Referer'] = 'http://finace.daum.et/quotes/A%s' % code
        r_1000 = requests.get(url_1000, headers=headers_1000)

        data_1000 = json.loads(r_1000.text)
        df_1000 = pd.DataFrame(data_1000['data'])

        s_highest_1000 = df_1000["highPrice"].max()
        s_lowest_1000 = df_1000["lowPrice"].min()

        url_JMJP = 'http://finance.naver.com/item/main.nhn?code=%s' % (code)
        tables = pd.read_html(url_JMJP, encoding='euc-kr')
        df_JMJP = tables[3]
        df_MC = tables[5]

        Sales_2021 = df_JMJP.iat[0, 4]
        OperatingIncome_2021 = df_JMJP.iat[1, 4]
        NetIncome_2021 = df_JMJP.iat[2, 4]

        Sales_2020 = df_JMJP.iat[0, 3]
        OperatingIncome_2020 = df_JMJP.iat[1, 3]
        NetIncome_2020 = df_JMJP.iat[2, 3]

        marketcap = df_MC.iat[0, 1]

        # DATA를 보기 좋게 편집하는 부분 입니다.
        data = json.loads(r.text)
        df = pd.DataFrame(data['data'])

        s_code = df.iat[2, 0]
        s_price = df.iat[-1, 3]
        y_price = df.iat[-2, 3]
        y_difference = s_price - y_price
        w_price = df.iat[-8, 3]
        w_difference = s_price - w_price

        s_highest = df["highPrice"].max()
        s_lowest = df["lowPrice"].min()
        try:
            s_percentile = "{:.2f}".format((s_price - s_lowest) / (s_highest - s_lowest))
        except Exception as exp:
            print(exp)
            s_percentile = 0

        try:
            s_percentile_1000 = "{:.2f}".format((s_price - s_lowest_1000) / (s_highest_1000 - s_lowest_1000))
        except Exception as exp:
            print(exp)
            s_percentile_1000 = 0

        df1 = pd.DataFrame({"Code": [s_code], "Price": [s_price], "Y_Price": [y_price], "1day_D": [y_difference],
                            "W_Price": [w_price], "1주일_D": [w_difference], "90일_H": [s_highest], "90_L": [s_lowest],
                            "90_P": [s_percentile], "1000일_H": [s_highest_1000], "1000일_L": [s_lowest_1000],
                            "1000일_P": [s_percentile_1000], "매출_21": [Sales_2021], "영업_21": [OperatingIncome_2021],
                            "순이익_21": [NetIncome_2021], "매출_20": [Sales_2020], "영업_20": [OperatingIncome_2020],
                            "순이익_20": [NetIncome_2020], "시가총액": [marketcap]})
        return df1
    except Exception as ex:
        try:
            url = 'http://finance.daum.net/api/charts/A%s/days?limit=%d&adjusted=true' % (code, 90)
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
                'Host': 'finance.daum.net',
                'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
                'Referer': 'http://finance.daum.net/quotes/A069500',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }
            headers['Referer'] = 'http://finance.daum.net/quotes/A%s' % code
            r = requests.get(url, headers=headers)

            url_1000 = 'http://finance.daum.net/api/charts/A%s/days?limit=%d&adjusted=true' % (code, 1000)
            headers_1000 = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
                'Host': 'finance.daum.net',
                'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
                'Referer': 'http://finance.daum.net/quotes/A069500',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }
            headers_1000['Referer'] = 'http://finace.daum.et/quotes/A%s' % code
            r_1000 = requests.get(url_1000, headers=headers_1000)

            data_1000 = json.loads(r_1000.text)
            df_1000 = pd.DataFrame(data_1000['data'])

            s_highest_1000 = df_1000["highPrice"].max()
            s_lowest_1000 = df_1000["lowPrice"].min()

            data = json.loads(r.text)
            df = pd.DataFrame(data['data'])

            s_code = df.iat[2, 0]
            s_price = df.iat[-1, 3]
            y_price = df.iat[-2, 3]
            y_difference = s_price - y_price
            w_price = df.iat[-8, 3]
            w_difference = s_price - w_price

            s_highest = df["highPrice"].max()
            s_lowest = df["lowPrice"].min()
            try:
                s_percentile = "{:.2f}".format((s_price - s_lowest) / (s_highest - s_lowest))
            except Exception as exp:
                print(exp)
                s_percentile = 0

            try:
                s_percentile_1000 = "{:.2f}".format((s_price - s_lowest_1000) / (s_highest_1000 - s_lowest_1000))
            except Exception as exp:
                print(exp)
                s_percentile_1000 = 0

            df1 = pd.DataFrame({"Code": [s_code], "Price": [s_price], "Y_Price": [y_price], "1day_D": [y_difference],
                                "W_Price": [w_price], "1주일_D": [w_difference], "90일_H": [s_highest], "90_L": [s_lowest],
                                "90_P": [s_percentile], "1000일_H": [s_highest_1000], "1000일_L": [s_lowest_1000],
                                "1000일_P": [s_percentile_1000], "매출_21": None, "영업_21": None,
                                "순이익_21": None, "매출_20": None, "영업_20": None,
                                "순이익_20": None, "시가총액": None})
            return df1
        except Exception as ex:
            print(ex, type(ex))
            df2 = pd.DataFrame({"Code": [s_code], "Price": [s_price]})

            return df2


def get_info():
    global drt

    df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    print("A")
    df = df[['회사명', '종목코드']]
    df = df.rename(columns={'회사명': 'Name', '종목코드': 'Code'})

    if drt[-1] == 'x':
        in_df = pd.read_excel(drt)
    else:
        in_df = pd.read_csv(drt)
    i = 0

    while i < len(in_df):
        in_name = in_df.iat[i, 0]
        if i == 0:
            nc_df = df.loc[df.index[df['Name'] == in_name]]
            fnc_df = nc_df
            i = i + 1
        else:
            nc_df = df.loc[df.index[df['Name'] == in_name]]
            fnc_df = fnc_df.append(nc_df)
            i = i + 1

    j = 0
    while j < len(fnc_df):
        in_code = str(fnc_df.iat[j, 1]).zfill(6)
        if j == 0:
            cphl_df = get_price_k(in_code)
            fcphl_df = cphl_df
            j = j + 1
        else:
            cphl_df = get_price_k(in_code)
            fcphl_df = fcphl_df.append(cphl_df)
            j = j + 1

    fnc_df = fnc_df.reset_index()
    fcphl_df = fcphl_df.reset_index()

    f = pd.concat([fnc_df, fcphl_df], axis=1)
    final = f.drop(['index', 'Code'], axis=1)

    global windows_user_name
    global today
    final.to_excel('{}/Desktop/{}.xlsx'.format(windows_user_name, today))


class MainWindow(QMainWindow):
    def btnRun_clicked(self):
        btn = self.sender()
        btn.setText('runing')
        btn.setDisabled(True)  # 버튼 비활성화

    def filedialog_open(self):

        fname = QFileDialog.getOpenFileName(self, 'Open File', '',
                                            'All File(*);; html File(*.html *.htm)')
        global drt
        drt = str(fname[0])

        if fname[0]:
            # 튜플 데이터에서 첫 번째 인자 값이 주소이다.
            self.path.setText(drt)
            print('filepath : ', drt)
            print('filesort : ', fname[1])

        else:
            QMessageBox.about(self, 'Warning', '파일을 선택하지 않았습니다.')

    def __init__(self):
        global drt

        super().__init__()
        # 윈도우 설정
        self.setGeometry(300, 200, 800, 120)  # x, y, w, h
        self.setWindowTitle('주식분석기!')

        self.Lbl1 = QLabel(self)
        self.Lbl1.setText('주식 종목 파일:')
        self.Lbl1.setGeometry(20, 20, 180, 32)

        # QButton 위젯 생성 - FileDialog 을 띄위기 위한 버튼
        self.button = QPushButton('Search...', self)
        self.button.clicked.connect(self.filedialog_open)
        self.button.setGeometry(580, 20, 200, 32)

        # QTextEdit 파일 읽은 내용 표시

        self.path = QTextEdit(self)
        self.path.setGeometry(165, 20, 400, 74)

        self.exe_btn = QPushButton('확인', self)
        self.exe_btn.clicked.connect(get_info)
        self.exe_btn.setGeometry(580, 60, 95, 32)

        self.quit_btn = QPushButton('취소', self)
        self.quit_btn.setGeometry(685, 60, 95, 32)
        self.quit_btn.clicked.connect(QApplication.instance().quit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())