from django.shortcuts import render
from stock_prediction.apps import stocks, train_cols
from stock_prediction.utils.CollectAndNormalizeData import CollectAndNormalizeData
from stock_prediction.utils.ForecastMarket import ForecastMarket
from stock_prediction.utils.Sentiment import Sentiment
from stock_prediction.utils.Utility import human_format
import time
import pandas as pd
from django.conf import settings as djangoSettings

# Create your views here.
def predict(request, stock_key = 'FB'):
    stock = stocks[stock_key]
    batch_size = 20
    time_steps = 60
    days_to_predict = 15
    normalized_data = CollectAndNormalizeData(stock_key)
    x_data, min_max_scaler, df = normalized_data.prepare_forecast_input()
    output = ForecastMarket(stock_key, batch_size, time_steps)
    output_tuple, df_prediction = output.forecast(normalized_data, x_data, min_max_scaler, df, days_to_predict = days_to_predict)
    df_prediction.reset_index(level=0, inplace=True)
    df_prediction = df_prediction.rename(columns = {'index':'date'})
    df = pd.DataFrame({'date': ['01-01-2020', '02-01-2020', '03-01-2020', '04-01-2020', '05-01-2020', '06-01-2020', '07-01-2020', '08-01-2020', '09-01-2020', '10-01-2020'], 
                       'headline': ['headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr', 'headline1 sdsf f f f rf rfe4 e4 eet gt4e t tr eg rt r tr5 y r5y 5r y t5ty tr5rt y5 yu76 u 65u 65u 76 f ef e t4e t4e tr'],
                       'sentiment': [0,1,1,1,1,1,1,0,1,0],
                       'compound' : [0,1,1,0,1,0,1,0,1,0]})
    s1=Sentiment(stock_key, 10)      #class object
    headlines_sentiment = s1.fv_sentiment()         #calling class function
    context = {
        'stock_name': stock['name'],
        'stock_key': stock_key,
        'headlines_sentiment' : headlines_sentiment,
        'positive' : len([x for x in headlines_sentiment if x['sentiment'] == 1]),
        'negative' : len([x for x in headlines_sentiment if x['sentiment'] == 0]),
        'df_prediction':df_prediction.to_json(orient='index', date_format='iso', date_unit='s')
    }
    for col in train_cols:
        if col == 'volume':
            context[col] = human_format(round(output_tuple[train_cols.index(col)]))
        else:
            context[col] = round(output_tuple[train_cols.index(col)])
    return render(request,
                  'stock_prediction.html',
                  context)
    
