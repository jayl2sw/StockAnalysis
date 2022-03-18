from django.shortcuts import render, redirect, get_object_or_404
from .models import Corperations, PriceinDate
import pandas as pd
import json
import requests
import lxml
from datetime import datetime

df_name_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
baseDate = datetime.strptime("2021-12-31", "%Y-%m-%d")

StockDate = [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0,
             0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1,
             0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,
             1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0,
             0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1,
             0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,
             1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0,
             1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1,
             1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1,
             0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1,
             1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1,
             1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0]


# Create your views here.
def getFullCode(c_name):
    code = df_name_code.loc[df_name_code['회사명'] == c_name].iat[0, 1]
    str_code = 'A' + str(code).zfill(6)
    return str_code


def getName(c_code):
    if c_code[0] == 'A':
        c_code = c_code[1:]
    c_code = int(c_code)
    name = df_name_code.loc[df_name_code['종목코드'] == c_code].iat[0, 0]

    return name


def get_df(code, days):
    url = f'http://finance.daum.net/api/charts/{code}/days?limit={days}&adjusted=true'
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
               'Referer': 'http://finance.daum.net/quotes/%s' % code,
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/70.0.3538.77 Safari/537.36'}

    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    df = pd.DataFrame(data['data'])
    df = df[['symbolCode', 'date', 'tradePrice', 'openingPrice', 'highPrice', 'lowPrice', 'candleAccTradeVolume']]
    return df


def get_price(code):
    df = get_df(code, 1)
    price = df.iat[-1, 2]
    return price


def getInfo(code):
    print(code)
    url_JMJP = 'http://finance.naver.com/item/main.nhn?code=%s' % (code[1:])
    tables = pd.read_html(url_JMJP, encoding='euc-kr')
    df_JMJP = tables[3]
    df_MC = tables[5]
    if '2022.12(E)' in df_JMJP.columns[4]:
        i = 3
    else:
        i = 4
    sales_21 = int(df_JMJP.iat[0, i])
    operatingincome_21 = int(df_JMJP.iat[1, i])
    netincome_21 = int(df_JMJP.iat[2, i])
    sales_20 = int(df_JMJP.iat[0, i - 1])
    operatingincome_20 = int(df_JMJP.iat[1, i - 1])
    netincome_20 = int(df_JMJP.iat[2, i - 1])
    market_cap = df_MC.iat[0, 1]
    result = {'sales_21': sales_21, 'operatingincome_21': operatingincome_21, 'netincome_21': netincome_21,
              'sales_20': sales_20, 'operatingincome_20': operatingincome_20, 'netincome_20': netincome_20,
              'market_cap': market_cap}

    return result


def updatePriceinDate(code, N):
    df = get_df(code, N)
    df_corp = df.to_dict()
    name=getName(df_corp['symbolCode'][0])
    model_instances = [PriceinDate(
        c_name=name,
        c_code=df_corp['symbolCode'][i],
        date=df_corp['date'][i],
        tradePrice=df_corp['tradePrice'][i],
        openingPrice=df_corp['openingPrice'][i],
        highPrice=df_corp['highPrice'][i],
        lowPrice=df_corp['lowPrice'][i],
        volume =df_corp['candleAccTradeVolume'][i]
    ) for i in range(len(df_corp['symbolCode']))]

    PriceinDate.objects.bulk_create(model_instances)


def main(request, warning=None):
    if request.method == 'POST':
        corp = Corperations()
        c_name = request.POST.get('name')
        c_code = request.POST.get('code')

        if c_code == "":
            if c_name == "":
                redirect('stockdata:main')
            corp.c_name = c_name
            try:
                code = getFullCode(c_name)
            except:
                pass
            corp.c_code = code
            corp.c_price = get_price(code)

        elif c_name == "":
            print(2)
            if str(c_code)[0] != 'A':
                code = 'A' + str(c_code).zfill(6)
            corp.c_code = code
            try:
                corp.c_name = getName(code)
                corp.c_price = get_price(code)
            except:
                pass
        try:
            informations = getInfo(code)

            corp.sales_21 = informations['sales_21']
            corp.operatingincome_21 = informations['operatingincome_21']
            corp.netincome_21 = informations['netincome_21']
            corp.sales_20 = informations['sales_20']
            corp.operatingincome_20 = informations['operatingincome_20']
            corp.netincome_20 = informations['netincome_20']
            corp.market_cap = informations['market_cap']
            corp.save()
        except:
            pass

        return redirect('stockdata:main')

    else:
        corps = Corperations.objects.all()
        for corp in corps:
            corp.c_price = int(get_price(corp.c_code))
            corp.save()

        context = {
            'corps': corps,
            'warning': warning,
        }

    return render(request, 'corperations/main.html', context)


def detail(request, corp_code=None):
    # corp = Corperations.object.get(pk=corp_code)
    # if request.method == "POST":
    #     temp = sqlite3.connect("../db.sqlite3")

    corp = get_object_or_404(Corperations, pk=corp_code)

    if request.method == 'POST':
        if str(corp.last_updated_date) == '2000-01-01':
            updatePriceinDate(corp_code, 1000)
        
        else:
            datetocompare = corp.last_updated_date
            difference = (datetime.now().date() - datetocompare).days
            if difference == 0:
                priceinDate = PriceinDate.objects.filter(c_code=corp_code)
                context = {
                    'corp': corp,
                    'priceinDate': priceinDate
                }
                return render(request, 'corperations/detail.html', context)
                
            start = (datetocompare - baseDate).days
            N = sum(StockDate[start:start+int(difference)+1])
            updatePriceinDate(corp_code, N)

        corp.last_updated_date = datetime.today()
        corp.save()

    priceinDate = PriceinDate.objects.filter(c_code=corp_code)
    context = {
        'corp': corp,
        'priceinDate': priceinDate
    }
    return render(request, 'corperations/detail.html', context)


def delete(request, corp_code):
    if request.method == 'POST':
        corp = get_object_or_404(Corperations, pk=corp_code)
        corp.delete()
    return redirect('stockdata:main')