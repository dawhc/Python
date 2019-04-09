#getHTMLurl

import requests
from bs4 import BeautifulSoup

def main():

    URL = 'https://www.baidu.com'

    r = requests.get(URL, timeout = 10)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
        print(link.get('href'))

main()