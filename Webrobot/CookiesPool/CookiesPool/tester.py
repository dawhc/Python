import json
import requests
from config import *
from requests.exceptions import ConnectionError
from db import RedisClient

class ValidTester(object):
    def __init__(self, website = 'default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)

class WeiboValidTester(ValidTester):
    def __init__(self, website = 'weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('Testing cookies...[Username = {}]'.format(username))
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Illegal cookies![Username = {}]'.format(username))
            self.cookies_db.delete(username)
            print('Cookies has been deleted successfully.')
            return 1
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies = cookies, timeout = 5, allow_redirects = False)
            if response.status_code == 200:
                print('Valid cookies. [Username = {}]'.format(username))
                return 0
            else:
                print('Invalid cookies! [Username = {}]'.format(username))
                print('Response status code: {}'.format(response.status_code))               
                self.cookies_db.delete(username)
                print('Cookies has been deleted successfully.')
                return 1
        except ConnectionError as e:
            print('[Error]Connection error! ', e.args)

if __name__ == '__main__':
    WeiboValidTester.run()