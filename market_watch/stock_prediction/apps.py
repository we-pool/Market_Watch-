import nltk
nltk.download('vader_lexicon')
from django.apps import AppConfig
from collections import OrderedDict 
from keras.models import load_model
import os

stocks = OrderedDict()
train_cols = ['open','high','low','close','volume']
models_dict = None
class StockPredictionConfig(AppConfig):
    name = 'stock_prediction'

    def ready(self):
        #connect_drive()
        global stocks
        global models_dict
        stock_fb = {'name': 'Facebook', 'models': [], 'href': '/predict/FB'}
        stocks['FB'] = stock_fb
        stock_appl = {'name': 'Apple', 'models': [], 'href': '/predict/AAPL'}
        stocks['AAPL'] = stock_appl
        stock_amzn = {'name': 'Amazon', 'models': [], 'href': '/predict/AMZN'}
        stocks['AMZN'] = stock_amzn
        stock_msft = {'name': 'Microsoft', 'models': [], 'href': '/predict/MSFT'}
        stocks['MSFT'] = stock_msft
        stock_googl = {'name': 'Google', 'models': [], 'href': '/predict/GOOGL'}
        stocks['GOOGL'] = stock_googl
        models_dict = self.load_all_metrics_models(['FB', 'AAPL', 'AMZN', 'MSFT', 'GOOGL'])
        

    def load_all_metrics_models(self, stocknames): 
        models = {}
        for stockname in stocknames:
            model_path = 'models/'+stockname
            model_list = []
            for col in train_cols:
                model_list.append(load_model(os.path.join(model_path, col, 'lstm_model.h5')))
            models[stockname] = model_list
        return models