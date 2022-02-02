import requests
import pandas as pd
import json

import os
from datetime import datetime

windows_user_name = os.path.expanduser('~')
today = datetime.today().strftime('%Y-%m-%d')


# input = 파일 경로 ouput = 종목 이름 리스트
def read_excel(path):
    if path[-1] == 'x':
        try:
            input_data = pd.read_excel(path)
            names = []
            for i in range(len(input_data['회사명'])):
                names.append(input_data['회사명'][i])
            return names
        except Exception as ex:
            print(ex)

    else:
        try:
            input_data = pd.read_csv(path)
            names = []
            for i in range(len(input_data['회사명'])):
                names.append(input_data['회사명'][i])
            return names
        except Exception as ex:
            print(ex)


# 종목이름 리스트 ==> 이름 코드 데이터프레임
def get_code(names):
    df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    df = df[['회사명', '종목코드']]
    df = df.rename(columns={'회사명': 'Name', '종목코드': 'Code'})

    nc_filter = df['Name'].isin(names)
    nc_df = df.loc[nc_filter].reset_index(drop=True)
    return nc_df


def get_price(code):
    try:
        url = f'http://finance.daum.net/api/charts/A{code}/days?limit=90&adjusted=true'
        headers = {'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Connection': 'keep-alive',
                   'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; '
                             'webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; '
                             '_gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{'
                             '%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{'
                             '%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; '
                             'TIARA=C-Tax5zAJ3L1CwQFDxYNxe'
                             '-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; '
                             'webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; '
                             '_dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
                   'Host': 'finance.daum.net', 'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
                   'Referer': 'http://finance.daum.net/quotes/A%s' % code,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/70.0.3538.77 Safari/537.36'}
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
        df = pd.DataFrame(data['data'])

        url_1000 = f'http://finance.daum.net/api/charts/A{code}/days?limit=1000&adjusted=true'
        headers_1000 = {'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Connection': 'keep-alive',
                        'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; '
                                  'webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; '
                                  '_gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=['
                                  '{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{'
                                  '%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; '
                                  'TIARA=C-Tax5zAJ3L1CwQFDxYNxe'
                                  '-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; '
                                  'webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; '
                                  '_dfs'
                                  '=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
                        'Host': 'finance.daum.net', 'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
                        'Referer': 'http://finace.daum.et/quotes/A%s' % code,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/70.0.3538.77 Safari/537.36'}
        r_1000 = requests.get(url_1000, headers=headers_1000)

        data_1000 = json.loads(r_1000.text)
        df_1000 = pd.DataFrame(data_1000['data'])

        s_code = df.iat[2, 0]
        s_price = df.iat[-1, 3]
        y_price = df.iat[-2, 3]
        y_difference = s_price - y_price
        w_price = df.iat[-8, 3]
        w_difference = s_price - w_price

        s_highest = df["highPrice"].max()
        s_lowest = df["lowPrice"].min()

        s_highest_1000 = df_1000["highPrice"].max()
        s_lowest_1000 = df_1000["lowPrice"].min()

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

        market_cap = df_MC.iat[0, 1]

        df_informations = pd.DataFrame(
            {"Code": [s_code], "Price": [s_price], "Y_Price": [y_price], "1day_D": [y_difference],
             "W_Price": [w_price], "1주일_D": [w_difference], "90일_H": [s_highest], "90_L": [s_lowest],
             "90_P": [s_percentile], "1000일_H": [s_highest_1000], "1000일_L": [s_lowest_1000],
             "1000일_P": [s_percentile_1000], "매출_21": [Sales_2021], "영업_21": [OperatingIncome_2021],
             "순이익_21": [NetIncome_2021], "매출_20": [Sales_2020], "영업_20": [OperatingIncome_2020],
             "순이익_20": [NetIncome_2020], "시가총액": [market_cap]})

        return df_informations

    except Exception as ex:
        df_exception = pd.DataFrame({"Code": [s_code], "Price": [s_price]})

        return df_exception


def get_prices(corp_name_code_df):
    df = pd.DataFrame()
    for i in range(len(corp_name_code_df)):
        in_code = str(corp_name_code_df.iat[i, 1]).zfill(6)
        df = df.append(get_price(in_code))

    corp_name_code_df = corp_name_code_df.reset_index()
    df = df.reset_index()

    merged_df = pd.concat([corp_name_code_df, df], axis=1)
    final = merged_df.drop(['Code', 'index'], axis=1)
    return final


def make_excel():
    global drt
    corperations = read_excel(drt)
    corps = get_code(corperations)
    final = get_prices(corps)
    print(final)
    final.to_excel(f'{windows_user_name}/Desktop/{today}.xlsx')


from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QPushButton, QMessageBox, QLabel, QTextEdit, \
    QWidget, QProgressBar
import sys

drt = ''


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
        self.exe_btn.clicked.connect(make_excel)
        self.exe_btn.setGeometry(580, 60, 95, 32)

        self.quit_btn = QPushButton('취소', self)
        self.quit_btn.setGeometry(685, 60, 95, 32)
        self.quit_btn.clicked.connect(QApplication.instance().quit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
