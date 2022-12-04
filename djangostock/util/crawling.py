from bs4 import BeautifulSoup
from .webpage_load import Selenium

class NaverStockCrawling():
    URL = "https://finance.naver.com/sise/"

    def __init__(self) -> None:
        self.web = Selenium()
        print("Created NaverStockCrawling")

    def load_page_source(self, URL):
        self.web.set_page(URL)

        return self.web.driver.page_source

    def get_upper_limit_today(self, page_source):
        html = BeautifulSoup(page_source, 'html.parser')

        upper_limit_div = html.select_one("#contentarea > div.box_type_l")
        upper_limit_table = upper_limit_div.select_one('table > tbody')
        upper_limit = upper_limit_table.find_all('a')

        names = []

        for stock_name in upper_limit:
            names.append(stock_name.get_text())

        return names







if __name__ == "__main__":
    stock = NaverStockCrawling()
    page = stock.load_page_source(stock.URL)
    print(stock.get_upper_limit_today(page))
