from sys import excepthook
from django.shortcuts import render, redirect
import pandas as pd
import requests
import simplejson as json
from .models import Corperations, Stocks
import os
import openpyxl
import datetime

windows_user_name = os.path.expanduser('~')

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

def get_code(names):
    df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    df = df[['회사명', '종목코드']]
    df = df.rename(columns={'회사명': 'Name', '종목코드': 'Code'})

    nc_df = pd.DataFrame(columns=['Name', 'Code'])
    for name in names:
        nc_df = pd.concat([nc_df, df.loc[df['Name'] == name]], ignore_index=True)

    # nc_filter = df['Name'].isin(names)
    # nc_df = df.loc[nc_filter].reset_index(drop=True)
    return nc_df

def get_price(code):
    try:
        url = f'http://finance.daum.net/api/charts/A{code}/days?limit=1000&adjusted=true'
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
        return df

    except Exception as ex:
        print(ex)


# Create your views here.
def main(request):
    return render(request, 'articles/main.html')

def read_excel(request):
    return render(request, 'articles/read_excel.html')


def read_data(request):
    df = get_price()
    Stock = Stocks()
    stocks = Stocks.objects.all()
    check = Stocks.objects.get[-1]
    n = check.date - datetime.now()
    print(n)
    for i in range(0, n, -1):
        Stock.code = df.iat[-n+i][0]
        Stock.date = df.iat[-n+i][1]
        Stock.tradePrice = df.iat[-n+i][3]
        Stock.candleAccTradeVolume = df.iat[-n+i][8]
        Stock.changePrice = df.iat[-n+i][13]
        Stock.changeRate = df.iat[-n+i][12]
        Stock.save()

    return redirect('articles:main')

def analyzed_data(request):
    return render(request, 'articles/analyzed.html')


def corperations(request):
    corps = Corperations.objects.all()
    context = {
        'corps': corps,
    }
    return render(request, 'articles/corperations/corperations.html', context)
