from stocks.dataOpen import KoreaDataAPI

def sorted_stock_by_stock_cap(stocks):

    result = []
    data_API = KoreaDataAPI()
    for stock in stocks:
        stock_cap = data_API.get_lastest_stock_info(stock)['mrktTotAmt']

        result.append([float(stock_cap), stock])

    result.sort()
    return result


if __name__ == "__main__":
    print(sorted_stock_by_stock_cap([]))