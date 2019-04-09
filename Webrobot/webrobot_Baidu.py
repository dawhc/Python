#HollandRadarDraw
URL = 'http://www.baidu.com/s'

import requests as rqs

NeedtoSearchStr = input("Input a key word: ")
kv = {'wd' : NeedtoSearchStr}

r = rqs.get(URL, params = kv)
r.encoding = r.apparent_encoding

try:
    r.raise_for_status
except:
    print("Error! Status Code: {}".format(r.status_code), end = '\n\n')

print("{0:*^100}".format("Webpage Text"), end = '\n\n')
print(r.text)
