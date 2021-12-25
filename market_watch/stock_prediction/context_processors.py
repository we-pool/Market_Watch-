from stock_prediction.apps import stocks, train_cols
import json

def stocks_menu(request):
    menu = []
    for k, v in stocks.items():
        stock = {
            'key': k,
            'href': v['href'],
            'name': v['name']
        }
        menu.append(stock)
    return {
        'menu': menu,
        'cols': json.dumps(train_cols)
    }