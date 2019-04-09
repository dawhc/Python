import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return None

def getPoems(txt):
    s = BeautifulSoup(txt, 'html.parser')
    
    title = s.find('div', attrs = {'class' : 'page-header'}).h2.text
    title = title.split(' ')[-1]

    article = s.find('div', attrs = {'class' : 'article'})
    [p.extract() for p in article('p')]
    [div_t.extract() for div_t in article('div', attrs = {'class' : 'topads'})]
    content =  article.text.strip().split('\n')
    return title, content

def main():
    URL = 'http://www.300tangshi.com/'

    for i in range(1, 310):
        current_url = URL + str(i) + '.html'
        pagetxt = getHTMLText(current_url)
        if pagetxt != None:
            # get the title and the content of a poem
            title, content = getPoems(pagetxt) 
            print('\n' + title)
            for i in content:
                print(i)
main()
