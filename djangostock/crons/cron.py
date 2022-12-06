
import requests

def send_upper_limit_cron():
    res = requests.get("http://127.0.0.1:8000/sms/oauth")
    print(res.status_code)
