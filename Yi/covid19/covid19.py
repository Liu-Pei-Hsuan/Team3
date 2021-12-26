def covid19title():
    import requests
    url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN'
    res = requests.get(url)
    date = res.json()[0]['a04']
    total = res.json()[0]['a05']
    today = res.json()[0]['a06']
    return f'公告日期：{date}。\n 確診人數為：{today}人，累計確診人數為：{total}人。'


def covid19City():
    import requests
    url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5001&limited=全部縣市'
    res = requests.get(url)
    date = res.json()[0]['a02']
    tw = []
    twCount = 0
    others = 0
    x = 1
    while x == 1:
        for i in range(0, len(res.json())):
            if res.json()[i]['a02'] == date:
                if res.json()[i]['a03'] == '境外移入':
                    others += 1
                else:
                    twCount += 1
                    city = res.json()[i]['a03']
                    tw.append(city)
            else:
                x = 0
                break
        if twCount != 0:
            return f'公告日期：{date} 本土案例：{twCount}例，位於{set(tw)}；境外移入{others}例，總計：{twCount + others}例。'
        else:
            return f'公告日期：{date} 今日沒有本土案例，境外移入{others}例，總計：{twCount + others}例。'


TW = []
def covid19CountryCity():
    import requests
    TW.clear()
    url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5001&limited=全部縣市'
    res = requests.get(url)
    date = res.json()[0]['a02']
    for i in range(0, len(res.json())):
        if res.json()[i]['a02'] == date:
            loc = res.json()[i]['a03']
            TW.append(loc)
        else:
            break

    KEL = TW.count('基隆市')
    NTPC = TW.count('新北市')
    TPE = TW.count('台北市')
    TYN = TW.count('桃園市')
    HSZC = TW.count('新竹市')
    HSZ = TW.count('新竹縣')
    ZMIC = TW.count('苗栗市')
    ZMI = TW.count('苗栗縣')
    TXG = TW.count('台中市')
    CHWC = TW.count('彰化市')
    CHW = TW.count('彰化縣')
    NTCC = TW.count('南投市')
    NTC = TW.count('南投縣')
    YUN = TW.count('雲林縣')
    CYIC = TW.count('嘉義市')
    CYI = TW.count('嘉義縣')
    TNN = TW.count('台南市')
    KHH = TW.count('高雄市')
    PIF = TW.count('屏東縣')
    PIFC = TW.count('屏東市')
    ILAC = TW.count('宜蘭市')
    ILA = TW.count('宜蘭縣')
    HUNC = TW.count('花蓮市')
    HUN = TW.count('花蓮縣')
    TTTC = TW.count('台東市')
    TTT = TW.count('台東縣')
    PEH = TW.count('澎湖縣')
    OTH = TW.count('境外移入')
    return KEL, NTPC, TPE, TYN, HSZC, HSZ, ZMIC, ZMI, TXG, CHWC, CHW, NTCC, NTC, YUN, CYIC, CYI, TNN, KHH, PIF, PIFC, ILAC, ILA, HUNC, HUN, TTTC, TTT, PEH, OTH
