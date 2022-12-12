import requests
import json
import os
import threading

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from sms.login import KakaoLogin
from util.crawling import NaverStockCrawling
from stocks.dataOpen import KoreaDataAPI
from util import handling
from stocks.models import StockInfo, ThemaInfo


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
        stock.web.teardown()

        t = threading.Thread(target=self.send_sms_in_background, args=(token, upper_limits))
        t.start()
        
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
    
    def send_sms_in_background(self, token, upper_limits):
        """상한가와 관련된 주식 목록을 DB에서 가져와 카카오톡으로 전송한다.

        Args:
            token (_type_): 카카오톡에서 발급받은 토크
            upper_limits (_type_): 당일 상한가 목록
        """
        
        for upper_stocks in upper_limits:
            stock_info_of_upeer_stock = StockInfo.objects.filter(stock_name=upper_stocks)
            
            if stock_info_of_upeer_stock.exists():
                stock_info_of_upeer_stock = stock_info_of_upeer_stock.first()
            else:
                print("존재하지 않는 이름은 ", upper_stocks)
                continue

            if stock_info_of_upeer_stock.themas:
                for thema in stock_info_of_upeer_stock.themas.split(','):
                    cand_stocks = ThemaInfo.objects.get(thema_name=thema).stocks.split(',')
                    cand_stocks = handling.sorted_stock_by_stock_cap(cand_stocks)

                    if cand_stocks:
                        self._send_SMS_to_me(token, "www.naver.com", upper_stocks + "\n" + thema + "\n" + str(cand_stocks))

    
    def _send_SMS_to_me(self, access_token, url, text):
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
