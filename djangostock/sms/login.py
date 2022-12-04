from util.webpage_load import Selenium

import time
import random


class KakaoLogin(Selenium):
    def __init__(self):
        super().__init__()

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
