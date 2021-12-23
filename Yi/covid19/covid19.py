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
                    city =res.json()[i]['a03']
                    tw.append(city)
            else:
                x = 0
                break
        if twCount != 0:
            return f'公告日期：{date} 本土案例：{twCount}例，位於{set(tw)}；境外移入{others}例，總計：{twCount+others}例。'
        else:
            return f'公告日期：{date} 今日沒有本土案例，境外移入{others}例，總計：{twCount + others}例。'


print(covid19title())
