import time
from multiprocessing import Process
from api import app
from config import *
from generator import WeiboCookiesGenerator
from tester import WeiboValidTester

class Scheduler(object):
    @staticmethod
    def check_cookie(cycle = CYCLE):
        counter = 0
        while True:
            counter += 1
            print('[Start cookies checking process...{} times]'.format(counter))
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    result = tester.run()
                    print('Succeessful to check "{}"'.format(website))
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        counter = 0
        while True:
            counter += 1
            print('[Start cookies generating process...{} times]'.format(counter))
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Succeessful to generate "{}"'.format(website))
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('[Start to run API]')
        app.run(host = API_HOST, port = API_PORT)

    def run(self):
        if API_PROCESS:
            api_process = Process(target = Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generator_process = Process(target= Scheduler.generate_cookie)
            generator_process.start()

        if VALID_PROCESS:
            valid_process = Process(target = Scheduler.check_cookie)
            valid_process.start()
        
if __name__ == '__main__':
    cookiespool = Scheduler();
    cookiespool.run();