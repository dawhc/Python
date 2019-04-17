from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
from os.path import abspath, dirname
import time

TEMPLATES_FOLDER = dirname(abspath(__file__)) + '/templates/'

class WeiboCookies(object):
    def __init__(self, username, password, browser = None):
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
        if browser == None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            self.browser = webdriver.Chrome(chrome_options = chrome_options)
        else:
            self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def open(self):
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(0.5)
        submit.click()

    def password_error(self):
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误')))
        except TimeoutException:
            return False

    def login_successfully(self):
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf-profile'))))
        except TimeoutException:
            return False

    def get_position(self):
        try:
            img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'patt-shadow')))
        except TimeoutException:
            print('Captcha not found.')
            self.open()
        time.sleep(1)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self, name = 'captcha.png'):
        top, bottom, left, right = self.get_position()
        print('Captcha position:', 'top = ', top, 'bottom = ', bottom, 'left = ', left, 'right = ', right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha

    def is_pixel_equal(self, image1, image2, x, y):
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 20
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1]- pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def same_image(self, image, template):
        threshold = 0.99
        count = 0
        for x in range(image.width):
            for y in range(image.height):
                if self.is_pixel_equal(image, template, x, y):
                    count += 1
        result = float(count) / (image.weight * image.height)
        if (result > threshold):
            print("Successfully matched.")
            return True
        return False

    def detect_image(self, image):
        for template_name in listdir(TEMPLATES_FOLDER):
            print('matching...[template image: ', template_name, ']')
            template = Image.open(TEMPLATES_FOLDER + template_name)
            if self.same_image(image, template):
                numbers = [int(number) for number in list(template_name.split('.')[0])]
                print('Dragging order: ', numbers)
                return numbers

    def move(self, numbers):
        try:
            circles = self.browser.find_elements_by_css_selector('.patt-wrap .patt-circ')
            dx = dy = 0
            for index in range(4):
                circle = circles[numbers[index] - 1]

                if index == 0:
                    ActionChains(self.browser) \
                        .move_to_element_with_offset(circle, circle.size['width'] / 2, circle.size['height'] / 2) \
                        .click_and_hold().perform()
                else:
                    times = 30
                    for i in range(times):
                        ActionChains(self.browser).move_by_offset(dx / times, dy / times).perform()
                        time.sleep(1 / times)
                if index == 3:
                    ActionChains(self.browser).release().perform()
                else:
                    dx = circles[numbers[index + 1] - 1].location['x'] - circle.location['x']
                    dy = circles[numbers[index + 1] - 1].location['y'] - circle.location['y']
        except:
            return False
        return True
    def get_cookies(self):
        return self.browser.get_cookies()

    def main(self):
        self.open()
        if self.password_error():
            return {
                'status' : 2,
                'content' : '用户名或密码错误'
            }
         
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status' : 1,
                'content' : cookies
            }

        image = self.get_image('captcha.png')
        numbers = self.detect_image(image)
        self.move(numbers)
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status' : 1,
                'content' : cookies
            }
        else:
            return {
                'status' : 3,
                'content' : '验证失败'
            }

if __name__ == '__main__':
    result = WeiboCookies('username', 'password').main()
    print(result['content'])