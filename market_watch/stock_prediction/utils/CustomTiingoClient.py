import numpy as np
from tiingo import TiingoClient
import time
import os

from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

class CustomTiingoClient:
  client = None
  __config = {}
  def __init__(self, api_key = '4a1c22f3f83c1d23688f1aa7f9161ae4d44dba3d'):
      # Set TIINGO_API_KEY in your environment variables in your .bash_profile, OR
      # pass a dictionary with 'api_key' as a key into the TiingoClient.
        self.__set_tiingo_config(api_key)

  def __set_tiingo_config(self, api_key):
        self.__config['api_key'] = api_key
        # To reuse the same HTTP Session across API calls (and have better performance), include a session key.
        self.__config['session'] = True
  
  def get_client(self):
    if self.client is None:
      #Initialize tiingo client
      self.client = TiingoClient(self.__config)
    return self.client

  def get_data_from_api(self, stockname, startDate, endDate, saveCsv=True, train_cols = ['open','high','low','close','volume']):
    print('fetching from tiingo')
    '''Download stock price data from TIINGO'''
    data = self.get_client().get_dataframe(stockname, startDate, endDate)
    df = data.drop(['adjClose','adjHigh','adjLow','adjOpen','adjVolume','divCash','splitFactor'],axis = 1)
    df = df.reindex(columns=train_cols)
    if saveCsv:
      df.to_csv('dataset/'+stockname+'_stocks_'+startDate+'_'+endDate+'.csv')
    return df