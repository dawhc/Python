#HollandRadarDraw
URL = 'https://www.amazon.cn/gp/product/B01M8L5Z3Y'

import requests
try:
    r = requests.get(URL)
    r.encoding = r.apparent_encoding
    r.raise_for_status()
    print(r.text)
except:
    print("Error!", end = '')
    print("Status Code: {}".format(r.status_code))
    print("{0:*^100}".format("Headers"), end = '\n\n')
    print(r.request.headers, end = '\n\n')
    print("{0:*^100}".format("ResponseText"), end = '\n\n')
    print(r.text, end = '\n\n')
    if(r.status_code == 503):
        kv = {'User-Agent' : 'Google Chrome/69.0.3497.81'}
        r = requests.get(URL, headers = kv)
        try:
            r.encoding = r.apparent_encoding
            r.raise_for_status()
            print("{0:*^100}".format("Successfully get webpage text"))
            print(r.text)
        except:
            print("Error!", end = '')
            print("Status Code: {}".format(r.status_code))
            print("{0:*^100}".format("Headers"), end = '\n\n')
            print(r.request.headers, end = '\n\n')
            print("{0:*^100}".format("ResponseText"), end = '\n\n')
            print(r.text, end = '\n\n')
