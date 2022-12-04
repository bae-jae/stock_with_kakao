import requests
import json
import os

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from sms.login import KakaoLogin

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
        self.send_SMS_to_me(token, "나에게")

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
    
    def send_SMS_to_me(self, access_token, text):
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
                "web_url":"www.daum.net"
                }
            })
        }

        response = requests.post(url, headers=headers, data=data)
        return Response(response.status_code, response.status_code,)
        

    def send_SMS(self, friends, text, token):
        """
        POST /v1/api/talk/friends/message/default/send HTTP/1.1
        Host: kapi.kakao.com
        Authorization: Bearer ${ACCESS_TOKEN}

        Args:
            uuid_list (_type_): _description_
        """

        # send_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        send_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        headers = {"Authorization": "Bearer " + token}
        for friend in friends['elements']:
            receiver_uuids = friend['uuid']
            print("uuid는", receiver_uuids)
            data = {
                'receiver_uuids': '["{}"]'.format(receiver_uuids),
                "template_object":
                    json.dumps({
                        "object_type": "text",
                        "text": text,
                        "link": {
                            "web_url":"www.daum.net",
                            "web_url":"www.naver.com"
                        },
                        "button_title": "바로 확인"
                    })
            }

            response = requests.post(send_url, headers=headers, data=data)

        return Response(response.status_code, status.HTTP_200_OK)