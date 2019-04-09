from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool
from functools import partial
import numpy as np
import requests
import time
import os

class BaiduImageSpider(object):

    def __init__(self, kw = ''):
        self.keyword = kw
        self.__browser = self.get_page(kw)

    def __del__(self):
        self.__browser.close()
    
    def __str__(self):
        return type(self)

    def __function_decorator(func):
        func_name = func.__name__
        def decorate(*args, **kwargs):
            print('[Function ' + func_name + '] Running...')
            func(*args, **kwargs)
            print('[Function ' + func_name + '] Finished!')
        return decorate

    @staticmethod
    def save_image(url, path):
        dir = path + url.split('/')[-1]
        if not os.path.exists(dir):
            try:
                img_response = requests.get(url, timeout = 10)
                img_response.raise_for_status()
                with open(dir, 'wb+') as f:
                    f.write(img_response.content)
            except:
                return 1
        return 0

    @__function_decorator
    def download_images(self, sum = 10, path = 'C:/Users/Editor/Desktop/BaiduImages/'):
        if not os.path.exists(path):
            os.makedirs(path)

        for i in range((sum // 60) + 2):
            for j in range(3):
                self.__browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(0.1)

        imgitems = self.__browser.find_elements(By.CSS_SELECTOR, 'div#imgContainer li.imgitem')
        img_urls = [item.get_attribute('data-objurl') for item in imgitems[:sum]]

        # Download process
        pool = Pool()

        result = np.array(pool.map(partial(self.save_image, path = path), img_urls))
        err_counter = result.sum()
        print('Result: {} successfully download, {} failed'.format(sum - err_counter, err_counter))
        print('Path: {}'.format(path))
        pool.close() 
        pool.join()

    def current_url(self):
        return self.__browser.current_url

    def browse(self):
        webdriver.Chrome().get(self.current_url())

         
    @staticmethod
    def get_page(kw, is_visible = False):
        if not is_visible:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options = chrome_options)
        browser.get('https://image.baidu.com')
        wait = WebDriverWait(browser, 10)
        input = wait.until(EC.presence_of_element_located((By.ID, 'kw')))
        span = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 's_search')))
        input.send_keys(kw)
        time.sleep(0.5)
        span.click()
        return browser

if __name__ == '__main__':
    keyword = input('Input the keyword:')
    bdimg = BaiduImageSpider(keyword)
    bdimg.download_images(60)