
import requests

def send_upper_limit_cron():
    """cron을 이용해 http://127.0.0.1:8000/sms/oauth로 요청을 보냄
    해당 뷰함수가 카카오톡을 이용해 나에게 메세지를 전송한다
    """
    res = requests.get("http://127.0.0.1:8000/sms/oauth")
    print(res.status_code)
