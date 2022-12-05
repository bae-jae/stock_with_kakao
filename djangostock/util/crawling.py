import requests
from bs4 import BeautifulSoup

from util.webpage_load import Selenium

class NaverStockCrawling():

    def __init__(self) -> None:
        self.web = Selenium()
        print("Created NaverStockCrawling")

    def _load_page_source(self, URL):
        self.web.set_page(URL)

        return self.web.driver.page_source

    def get_upper_limit_today(self):
        url = "https://finance.naver.com/sise/"
        page_source = self._load_page_source(url)
        html = BeautifulSoup(page_source, 'html.parser')

        upper_limit_div = html.select_one("#contentarea > div.box_type_l")
        upper_limit_table = upper_limit_div.select_one('table > tbody')
        upper_limit = upper_limit_table.find_all('a')

        names = []

        for stock_name in upper_limit:
            names.append(stock_name.get_text())

        return names

    def get_stock_in_thema(self):
        thema_in_stock = {}
        stock_to_thema = {}

        for i in range(1, 7):
            page_source = self._load_page_source("https://finance.naver.com/sise/theme.nhn?&page=" + str(i))
            soup = BeautifulSoup(page_source, "lxml")

            for i in soup.find_all('a'):        #a속성 모두 찾기
                cand = str(i)

                if "/sise/sise_group_detail" in cand:
                    start = 0
                    end = 0

                    for index in range(1, len(cand)): #형식이 <>target<이런 식임
                        if cand[index] == '>':
                            start = index + 1

                        if cand[index] == '<':
                            end = index
                            break

                    name_list = self.get_include_names("https://finance.naver.com" + i['href'])
                    thema_in_stock[cand[start:end]] = name_list

                    for name in name_list:
                        if name in stock_to_thema.keys():
                             stock_to_thema[name] = stock_to_thema[name] + cand[start:end] + "\n"
                        else:
                            stock_to_thema[name] = cand[start:end] + "\n"

        return thema_in_stock, stock_to_thema


    def get_include_names(self, address):
        soup = BeautifulSoup(requests.get(address).text, "lxml")
        name = []

        for i in soup.find_all('a'):
            cand = str(i)

            if "code" in cand:
                start = 0
                end = 0

                for index in range(1, len(cand)):
                    if cand[index] == '>':
                        start = index + 1

                    if cand[index] == '<':
                        end = index
                        break

                if len(cand[start:end]) >= 2:
                    name.append(cand[start:end])
        return name

if __name__ == "__main__":
    stock = NaverStockCrawling()
    # page = stock.load_page_source(stock.URL)
    # print(stock.get_upper_limit_today(page))

    print(stock.get_stock_in_thema())


    stock.web.teardown()