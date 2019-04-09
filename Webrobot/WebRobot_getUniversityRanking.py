#getUniversityRanking

def getHTMLText(URL):
    import requests
    
    UAName = 'Google Chrome/64.0.0.0'

    try:
        r = requests.get(URL, headers = {'User-Agent' :UAName})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text;
    except requests.HTTPError:
        print("HTTPError! Status code: {}". format(r.status_code))
    except requests.Timeout:
        print("Timeout error!")
    except requests.exceptions.MissingSchema:
        print('''Missing schema! Maybe the URL misses "http://" ? ''')
    except:
        print("Unknown error!")
    return -1

def getInfo(Text):
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(Text, 'html.parser')
    
    info = []
    
    #get the titles
    ths = []

    for th in soup.find('tr')('th'):
        if(th.string == None):
            break
        ths.append(th.string)
    info.append(ths)

    #get the datas
    for tr in soup('tr', 'alt'):
        tds = []
        for td in tr('td'):
            tds.append(td.string)
        info.append(tds)

    return info

def printInfo(info, num):
    lineLength = len(info[0])
    for i in range(num + 1):
        for j in range(lineLength):
            print('\t{0:^20}'. format(info[i][j]), end = '')
        print('\n')

def main():
    URL = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming2018.html"
    txt = getHTMLText(URL)

    info = getInfo(txt)
    printInfo(info, 30)

main()