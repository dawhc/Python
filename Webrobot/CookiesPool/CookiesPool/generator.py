from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from config import *
from db import RedisClient
from login.weibo.cookies import WeiboCookies
import json

class CookiesGenerator(object):
    def __init__(self, website = 'default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
        self.init_browser()

    def __del__(self):
        self.close()

    def init_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options = chrome_options)
        
    def new_cookies(self, username, password):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    def process_cookies(self, cookies):
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value'] 
        return dict

    def run(self):
        account_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        for username in account_usernames:
            if not username in cookies_usernames:
                password = self.accounts_db.get(username)
                print('Generating new cookies...[username: {} password: {}]'.format(username, password))
                result = self.new_cookies(username, password)
                
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('Generated successfully!')
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('Saved new cookies successfully!')
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('Deleted invalid account successfully! [username: {}]'.format(username))
                else:
                    print(result.get('content'))
        else:
            print('All accounts has got cookies successfully!')

    def close(self):
        try:
            print('Closing browser...')
            self.browser.close()
            del self.browser
            print('Browser has closed!')
        except TypeError:
            print('Browser not opened!')

class WeiboCookiesGenerator(CookiesGenerator):
    def new_cookies(self, username, password):
        weibo_cookies = WeiboCookies(username = username, password = password, browser = self.browser)
        return weibo_cookies.main()
