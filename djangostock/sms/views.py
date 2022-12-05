import requests
import json
import os

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from sms.login import KakaoLogin
from util.crawling import NaverStockCrawling

REST_KEY = os.environ.get("REST_KEY")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
class OAuth(APIView):

    def get(self, request):
        """url로 요청을 보내 kakaoAPI를 쓸 수 있도록 로그인 작업을 수행함

        Args:
            request (_type_): _description_

        Returns:
            _type_: result of token
        """
        
        url = "https://kauth.kakao.com/oauth/authorize?client_id=" + REST_KEY + "&redirect_uri=" + REDIRECT_URI + "&response_type=code"
        print(url)
        try:
            login = KakaoLogin()
            login.set_page(url)
            login.do_login()
            return Response("SUCCESS", status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Error", status.HTTP_400_BAD_REQUEST)

class KakaoAPI(APIView):
    def get(self, request):
        auth = request.GET.get('code', "None")

        if not auth:
             Response("Can't get auth code", status.HTTP_400_BAD_REQUEST)
        token = self._get_token(auth)

        stock = NaverStockCrawling()
        upper_limits = stock.get_upper_limit_today()
        thema_in_stock, stock_to_thema = stock.get_stock_in_thema()
        stock.web.teardown()

        for upper_stocks in upper_limits:
            thema_of_upper_stocks = stock_to_thema.get(upper_stocks, [])

            if thema_of_upper_stocks:
                print(thema_of_upper_stocks.split('\n'))
                for thema in thema_of_upper_stocks.split('\n'):
                    cand_stocks = thema_in_stock.get(thema, [])

                    if cand_stocks:
                        self.send_SMS_to_me(token, "www.naver.com", upper_stocks + "\n" + thema + "\n" + str(cand_stocks))

        return Response(token, status.HTTP_200_OK)

    def _get_token(self, authentication):
        """_summary_

        Args:
            authentication (_type_): _description_

        Returns:
            _type_: _description_
        """

        data = {
            "grant_type": "authorization_code",
            "client_id": REST_KEY,
            "redirect_uri": REDIRECT_URI,
            "code": authentication,
        }

        response = requests.post('https://kauth.kakao.com/oauth/token', data=data)
        tokens = response.json()
        
        return tokens['access_token']
    
    def send_SMS_to_me(self, access_token, url, text):
        """text변수에 나에게 보낼 내용을 입력하면 나에게 메세지가 전송 됨
            POST /v2/api/talk/memo/default/send HTTP/1.1
            Host: kapi.kakao.com
            Authorization: Bearer ${ACCESS_TOKEN}

        Args:
            text (_type_): _description_
        """

        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {"Authorization": "Bearer " + access_token}
        
        data = {
            "template_object": json.dumps({
            "object_type" : "text",
            "text": text,
            "link": {
                "web_url": url
                }
            })
        }

        response = requests.post(url, headers=headers, data=data)
        return Response(response.status_code, response.status_code,)
