from stocks.dataOpen import KoreaDataAPI

def sorted_stock_by_stock_cap(stocks):

    result = []
    data_API = KoreaDataAPI()
    for stock in stocks:
        stock_cap = data_API.get_lastest_stock_info(stock).get('mrktTotAmt', [])

        if stock_cap:
            result.append([float(stock_cap), stock])

    result.sort()

    for i in range(len(result)):
        stock_value = result[i][0] // 100000000
        stock_value = str(stock_value) + "억"
        result[i][0] = stock_value
    return result


if __name__ == "__main__":
    print(sorted_stock_by_stock_cap([]))