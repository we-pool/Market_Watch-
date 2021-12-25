from stock_prediction.utils.CustomTiingoClient import CustomTiingoClient
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class CollectAndNormalizeData:
  tiingo_client = None
  stock_name = None
  train_cols = ['open','high','low','close','volume']
  api_key = None
  def __init__(self, stock_name, train_cols = None, api_key = None):
    self.stock_name = stock_name
    if train_cols is not None:
      self.train_cols = train_cols
    if api_key is not None:
      self.api_key = api_key

  def get_data(self, start_date, end_date):
    file_path = Path('dataset/'+self.stock_name+'_stocks_'+start_date+'_'+end_date+'.csv')
    if file_path.is_file():
      df = pd.read_csv(file_path, header=0, parse_dates=[0], index_col=0)
      return df
    else:
      return self.get_tiingo_data(start_date, end_date)
  
  def get_tiingo_data(self, start_date, end_date):
    if self.tiingo_client is None:
      if self.api_key is None:
        self.tiingo_client = CustomTiingoClient()
      else:
        self.tiingo_client = CustomTiingoClient(self.api_key)
    return self.tiingo_client.get_data_from_api(self.stock_name, start_date, end_date, self.train_cols)

  def get_stock_data_and_min_max_scaler(self, stock_name = None, N=150,start_date = None, end_date = None):
    if stock_name is not None:
      self.stock_name = stock_name
    if start_date is None or end_date is None:
      format = '%Y-%m-%d'
      today = datetime.now().date()
      n_days_ago = today - timedelta(days=N)
      start_date = n_days_ago.strftime(format)
      end_date = today.strftime(format)
    df = self.get_data(start_date, end_date)
    return df

  def scale_data(self, df, train_cols=None):
    '''Scale feature MinMax  - Train the scaler with training data and smooth data'''
    x = df.loc[:,self.train_cols if train_cols is None else train_cols].values
    min_max_scaler = MinMaxScaler()
    x_data = min_max_scaler.fit_transform(x)
    return x_data, min_max_scaler, df

  def prepare_forecast_input(self, df = None, n=200, train_cols= None):
    if df is None:
      df = self.get_stock_data_and_min_max_scaler(N = n)
    return self.scale_data(df, train_cols)