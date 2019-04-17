REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

BROWSER_TYPE = 'Chrome'

GENERATOR_MAP = {
    'weibo' : 'WeiboCookiesGenerator'
}
TESTER_MAP = {
    'weibo' : 'WeiboValidTester'    
}
TEST_URL_MAP = {
    'weibo' : 'https://m.weibo.cn/'
}
CYCLE = 5

API_HOST = '127.0.0.1'
API_PORT = 5000

GENERATOR_PROCESS = False

VALID_PROCESS = True

API_PROCESS = True