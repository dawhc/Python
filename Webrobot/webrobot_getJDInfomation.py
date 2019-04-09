#getJDInfo

def getHTMLText(url, goods, page):
    import requests

    UAName = 'Mozilla/5.0'
    try:
       r = requests.get(url, params = {'keyword' : goods, 'enc': 'utf-8', 'page' : str(page * 2 - 1)}, headers = {'User-Agent' : UAName}, timeout = 10)
       r.raise_for_status()
       r.encoding = r.apparent_encoding
       return r.text
    except requests.HTTPError:
        print("HTTPError! Status code: {}". format(r.status_code))
    except requests.Timeout:
        print("Timeout error!")
    except requests.exceptions.MissingSchema:
        print("The url misses schema!")
    except:
        print("Unknown error!")
    return None

def parsePage(txt):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(txt, 'html.parser')
    info = []

    for li in soup('li', attrs = {'class' : 'gl-item'}):
        price = li.strong.i.string
        title = ''
        for em in li('em'):
            if em.text == None: continue
            elif em.text[0] == '￥': continue
            else:
                title = em.text
                break
        if title == '': continue
        info.append([title, price])

    return info

def printList(infoList):
    for i in range(len(infoList)):
        print('\t{0:^10}\t{1:20}\t{2:20}'. format(i + 1, infoList[i][0], infoList[i][1]))

def main():
    
    goods = input('Please input some keywords:')
    infoList = []
    depth = 2
    onepage_Amount = 48
    URL = 'https://search.jd.com/Search'

    for i in range(depth):
        htmlTxt = getHTMLText(URL, goods, i + 1)
        infoList = parsePage(htmlTxt)
        printList(infoList)

main()