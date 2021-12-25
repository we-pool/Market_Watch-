from stock_prediction.utils.ModelInput import ModelInput
from datetime import datetime, timedelta
import pandas as pd
from stock_prediction.apps import train_cols, models_dict

class ForecastMarket:
  models = None
  stock_name = None
  train_cols = ['open','high','low','close','volume']
  days_to_predict = None
  inputData = None 
  batch_size = None
  time_steps=  None

  def __init__(self, stock_name, batch_size, time_steps, train_cols = None):
    self.stock_name = stock_name
    self.models = models_dict[self.stock_name]
    self.batch_size = batch_size
    self.time_steps = time_steps
    if train_cols is not None:
      return train_cols

  def get_all_predictions(self, X_T, min_max_scaler, train_cols):
    values = []
    for col in train_cols:
      idx = train_cols.index(col)
      x_t_idx = 0 if len(X_T) == 1 else train_cols.index(col)
      predictData = ModelInput()
      value = (self.models[idx].predict(predictData.trim_dataset(X_T[x_t_idx], self.batch_size), self.batch_size).flatten())[-1]
      value = (value * min_max_scaler.data_range_[x_t_idx]) + min_max_scaler.data_min_[x_t_idx] 
      values.append(value)
    return tuple(values)

  def forecast(self, normalized_data, x_data, min_max_scaler, df, days_to_predict = 15):
    input = ModelInput()
    X_T, Y_T = input.get_data(x_data, self.batch_size, self.time_steps, train_cols = self.train_cols)
    next_day_val = None
    tuple1 = self.get_all_predictions(X_T, min_max_scaler, train_cols)
    tuple_temp = tuple1
    master_df = df.copy()
    
    while days_to_predict > 1:
      days_to_predict = days_to_predict - 1
      df = df.iloc[1:]
      last_date = df.iloc[[-1]].index
      last_date = pd.to_datetime(last_date) + timedelta(days=1)
      data = {}
      for col in train_cols:
        data[col] = tuple_temp[train_cols.index(col)]
      df = df.append(pd.DataFrame(data, index=[(last_date.to_pydatetime())[0]]))
      master_df = master_df.append(pd.DataFrame(data, index=[(last_date.to_pydatetime())[0]]))
      x_data, min_max_scaler, df = normalized_data.prepare_forecast_input(df = df)
      input = ModelInput()
      X_T, Y_T = input.get_data(x_data, self.batch_size, self.time_steps, train_cols = self.train_cols)
      tuple_temp = self.get_all_predictions(X_T, min_max_scaler, train_cols)
      
    return tuple1, master_df
