# selenium
"""selenium"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
""""""
import time
import random


class Selenium:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.set_options()
        self.driver = self.install_driver()

    def install_driver(self):
        browser = webdriver.DesiredCapabilities.CHROME
        browser['goog:loggingPrefs'] = {'browser' : 'SEVERE'}
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options, desired_capabilities=browser)

    def set_options(self):
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--headless")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        self.options.add_argument("start-maximized")

    def set_page(self, address):
        self.driver.get(address)

    def do_login(self):
        import os

        id = os.getenv("KAKAO_ID")
        passwod = os.getenv("KAKAO_PASSWORD")

        for i in id:
            self._get_element("/html/body/div[1]/div/div/main/article/div/div/form/div[1]/div/input", 70).send_keys(i)
            time.sleep(random.random())
            
        for i in passwod:
            self._get_element("/html/body/div[1]/div/div/main/article/div/div/form/div[2]/input", 70).send_keys(i)
            time.sleep(random.random())
        
        time.sleep(1)
        self._get_element("/html/body/div[1]/div/div/main/article/div/div/form/div[4]/button[1]", 70).click()
        

    #id = /html/body/div[1]/div/div/main/article/div/div/form/div[1]/div/input
    def _get_element(self, path, time=10):
        return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located((By.XPATH, path)))

        
    def teardown(self):
        self.driver.quit()