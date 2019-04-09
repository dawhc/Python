#getStockInfo

def getStockName(URL):
    import requests
    from bs4 import BeautifulSoup

    try:
        r = requests.get(URL, timeout = 10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print('Error at request!')
        return ''

    stockList = []

    s = BeautifulSoup(r.text, 'html.parser')
    qox = s.find('div', attrs = {'class' : 'qox'})
    for ul in qox('ul'):
        nameList = []
        for a in ul('a'):
            nameList.append(a.text)
        stockList.append(nameList)

    return stockList[0], stockList[1]

    return nameList

def printStockInfo(URL, ls, stype):
    import requests
    from time import perf_counter
    from bs4 import BeautifulSoup

    for stock in ls:
        _begin_time = perf_counter()

        print('{0:*^50}'. format(stock))
        
        subURL = URL + stype + stock[-7 : -1] + '.html'
        
        try:
            r = requests.get(subURL, timeout = 10)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
        except:
            print("Request failed!", end = '\n\n')
            continue

        s = BeautifulSoup(r.text, 'html.parser')
        info = s.find('div', attrs = {'class' : 'stock-bets'})

        #printTotalInfo
        try:
            for classContent in ['stop', 'down', 'up']:
                total = info.find('div', attrs = {'class' : 'price s-' + classContent + ' '})
                if total == None: continue
                else: 
                    print('{}  {}  {}'.format(total.strong.text, total('span')[0].text, total('span')[1].text), end = '\n\n')
                    break
        except:
            print('Getting title failed!', end = '\n\n')
            continue

        #printContentInfo
        try:
            content = info.find('div', attrs = {'class' : 'bets-content'})
            for dl in content('dl'):
             print('{} : {}'.format(dl.dt.text, dl.dd.text), end = '\n')
        except:
            print('Getting content failed!', end = '\n\n')
            continue

        _end_time = perf_counter()
        print('\nFinished after {0:.2f}s.'. format(_end_time - _begin_time), end = '\n\n')



def main():
    
    URL_Sina = 'http://finance.sina.com.cn/stock'
    URL_Baidu = 'https://gupiao.baidu.com/stock/'
    URL_Eastmoney = 'http://quote.eastmoney.com/stocklist.html'

    SHStockName, SZStockName = getStockName(URL_Eastmoney)

    printStockInfo(URL_Baidu, SHStockName[500:600], 'sh')
    printStockInfo(URL_Baidu, SZStockName[500:600], 'sz')

main()
    