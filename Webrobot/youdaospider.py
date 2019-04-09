import requests
from bs4 import BeautifulSoup
import json
import os

class YoudaoSpider(object):
    
    def __init__(self):
        self.__url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.__history = [] 
        
    def __call__(self, content):
        self.query(content)
    
    def __show_result(self, json_content):
        result = json_content.get('translateResult')
        if (result):
            print('[Translate Result]\n')
            for paragraph in result:
               for sentence in paragraph:
                   print(sentence.get('tgt'), end = ' ')
               print('\n')

        smart_result = json_content.get('smartResult')
        if (smart_result):
            print('[Smart Result]')
            for item in smart_result.get('entries'):
                print(item)

    def query(self, content):
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie' : '_ntes_nnid=22ee0241b90f5f7316c8ccb4cf2f48d0,1548677729506; OUTFOX_SEARCH_USER_ID_NCOO=1423995136.3098977; OUTFOX_SEARCH_USER_ID="418317374@10.169.0.83"; JSESSIONID=aaamgzo7M7TEv5YUGx8Nw; ___rl__test__cookies=1554719157481',
            "Host" : "fanyi.youdao.com",
            "Origin" : "http://fanyi.youdao.com",
            "Referer" : "http://fanyi.youdao.com/",
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'X-Requested-With' : 'XMLHttpRequest'
            }
        salt = self.get_salt()
        data = {
            'i' : content,
            'from' : 'AUTO',
            'to' : 'AUTO',
            'smartresult ': 'dict',
            'client' : 'fanyideskweb',
            'salt' : str(salt),
            'sign': self.get_sign(content, salt),
            'doctype' : 'json',
            'version' : '2.1',
            'keyfrom' : 'fanyi.web',
            'action' : 'FY_BY_REALT',
            'typoResult' : 'false'
            }

        try:    
            self.__response = requests.post(self.__url, data = data, headers = headers, timeout = 10)
            self.__response.raise_for_status()
            self.__response.encoding = 'utf-8'
            resp_json = self.__response.json()
            #print(resp_json)
            self.__history.append((content, resp_json))
            self.__show_result(resp_json)

        except requests.Timeout: 
            print('[Error]Time out! Please check your network.')

        except requests.HTTPError:
            print('[Error]HTTP error! Status code: {}'.format(self.__response.status_code))
        
        except json.decoder.JSONDecodeError:
            print('[Error]Json decode error!');
        
        except:
            print('[Error]Unknown error!')

    def show_history(self):
        print('[History]\n')
        for item in self.__history:
            print(item[0] + '\n')
            self.__show_result(item[1])

    def clear_history(self):
        self.__history = []

    @staticmethod
    def get_salt():
        import time,random
        salt = int(time.time()*1000) + random.randint(0, 10)
        return salt

    @staticmethod
    def get_md5(v):
        import hashlib
        md5 = hashlib.md5()
        md5.update(v.encode("utf-8"))
        sign = md5.hexdigest()
        return sign

    @staticmethod
    def get_sign(key, salt):
        sign = "fanyideskweb" + key + str(salt) + "sr_3(QOHT)L2dx#uuGR@r"
        sign = YoudaoSpider.get_md5(sign)
        return sign

    @staticmethod
    def show_browser():
        from selenium import webdriver
        browser = webdriver.Chrome()
        browser.get('http://fanyi.youdao.com')
        return browser

    @classmethod
    def help(cls):
        return '''
[YoudaoSpider Command Help]

Use [content] to translate. (English <-> Chinese, using YoudaoDict)
Use ".[command]" to setting:
  .help       list commands
  .exit       exit the command
  .history    list query history
  .clear      clear query history
  .cls        clear the screen
        '''
    @staticmethod
    def command():
        print('Welcome to YoudaoSpider command!')
        command = YoudaoSpider()
        print('input the content to translate.(input ".help" to view help list)')
        content = input('-> ')
        while (content != '.exit'):
            if (content[0] == '.'):
                if (content == '.help'): 
                    print(YoudaoSpider.help())
                elif (content == '.history'):
                    command.show_history()
                elif (content == '.clear'):
                    command.clear_history()
                elif (content == '.cls'):
                    os.system('cls')
                else:
                    print('[Error] Unknown command "' + content + '".')
            else:
                command.query(content)

            content = input('-> ')

if __name__ == '__main__':
    YoudaoSpider.command()