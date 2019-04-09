#WebRobot
import requests
import os

URL = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1544262073882&di=53148d26351c8ee8a1a1903eaaa6f7f4&imgtype=0&src=http%3A%2F%2Fstatic01.coloros.com%2Fbbs%2Fdata%2Fattachment%2Fforum%2F201503%2F11%2F111210yjpy6yuojw7pw9ij.jpg'
UAName = 'Mozilla/5.0'
PicName = 'picture.jpg'
root = 'D:/'
path = root + PicName

def getPic():
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
           f.write(r.content)
           f.close()
           print('Successfully downloaded the picture.')
    else:
        print('File already exists.')

r = requests.get(URL)
try:
    r.raise_for_status()
    getPic()
except requests.HTTPError:
    print("Error! Status code: {}".format(r.status_code), end = '\n\n')
    if(r.status_code == 503):
        r = requests.get(URL, headers = {'user-agent' : UAName})
        print('The user-agent name has changed to ' + UAName)
        try:
            r.raise_for_status()
            getPic()
        except:
            print("Error! Status code: {}".format(r.status_code), end = '\n\n')




