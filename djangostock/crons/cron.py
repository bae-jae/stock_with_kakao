
import requests
from util.crawling import NaverStockCrawling
from stocks.models import StockInfo, ThemaInfo
from stocks.dataOpen import KoreaDataAPI

def send_upper_limit_cron():
    """cron을 이용해 http://127.0.0.1:8000/sms/oauth로 요청을 보냄
    해당 뷰함수가 카카오톡을 이용해 나에게 메세지를 전송한다
    """
    res = requests.get("http://127.0.0.1:8000/sms/oauth")
    print(res.status_code)

def store_stock_info_in_DB():
    """cron을 이용해 테마와 테마에 속한 종목을 DB에 업데이트 함
    """
    data_api = KoreaDataAPI()
    stock_naver = NaverStockCrawling()

    thema_in_stock, stock_to_thema = stock_naver.get_stock_in_thema()

    for stock in stock_to_thema:
        stock_cap = data_api.get_lastest_stock_info(stock).get('mrktTotAmt', [])
        themas = stock_to_thema[stock].split('\n')[:-1]
        themas = ",".join(themas)
        if not StockInfo.objects.filter(stock_name=stock).exists():
            StockInfo.objects.create(stock_name=stock, stock_cap=stock_cap, themas=themas)
        else:
            obj = StockInfo.objects.get(stock_name=stock)
            obj.stock_name = stock
            obj.stock_cap = stock_cap
            obj.themas = themas
            obj.save()

    print("stock_info 업데이트 완료")

    for thema in thema_in_stock:
        stocks = ",".join(thema_in_stock[thema])

        if not ThemaInfo.objects.filter(thema_name=thema).exists():
            ThemaInfo.objects.create(thema_name=thema, stocks=stocks)
        else:
            obj = ThemaInfo.objects.get(thema_name=thema)
            obj.thema_name = thema
            obj.stocks = stocks
            obj.save()

    print("thema_in_stock 업데이트 완료")

    stock_naver.web.teardown()


        


