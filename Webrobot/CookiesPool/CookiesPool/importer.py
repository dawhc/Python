import requests
from db import RedisClient

class Importer(object):
    def __init__(self, website):
        self.website = website
        self.conn = RedisClient('accounts', website)

    def set(self, account):
        username, password = account[0].strip(), account[1].strip()
        result = self.conn.set(username, password)
        print('Username: {}, Password: {}'.format(username, password))
        print('Saved the account successfully!' if result else 'Failed to save the account.')

    def input_accounts(self):
        print('Input new account [username , password]:(Input exit to exit)')
        while True:
            input_content = input('->')
            if (input_content == 'exit'):
                break
            account = input_content.split(',')
            self.set(account)

if __name__ == '__main__':
    pass