#WebRobot

def getHTMLText(URL):
    import requests
    try:
        r = requests.get(URL)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except requests.HTTPError:
        print("HTTPError! Status code: {}". format(r.status_code))
    except requests.Timeout:
        print("Time out!")
    except:
        print("Unknown Error!")

    return ""

def getMovieName(txt):
    from bs4 import BeautifulSoup

    s = BeautifulSoup(txt, 'html.parser')

    movieList = []

    for p in s.find('div', attrs = {"class" : "b-wrap bbox"})('p'):
        if p.a != None:
            movieList.append(p.a.text)

    return movieList
def main():

    URL = "https://www.meijutt.com"

    HTMLText = getHTMLText(URL)
    NameList = getMovieName(HTMLText)

    for name in NameList:
        print(name)

main()
