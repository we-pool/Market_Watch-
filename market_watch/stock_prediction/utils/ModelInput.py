import numpy as np
from tiingo import TiingoClient
import time
import os

from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

class ModelInput:
  train_cols = ['open','high','low','close','volume']

  def __init__(self, train_cols = None):
    if self.train_cols is None:
      self.train_cols = train_cols

  '''Filtering datasets for training model'''
  def trim_dataset(self, mat, batch_size):
    #trims dataset to a size that's divisible by BATCH_SIZE
    no_of_rows_drop = mat.shape[0] % batch_size

    if no_of_rows_drop > 0:
        return mat[:-no_of_rows_drop]
    else:
        return mat

  '''Transform data into time series format
    Divides in chunk of time steps'''
  def build_timeseries(self, input_array, time_steps):
    input_array = input_array.reshape(input_array.shape[0],1)
    dim_0 = input_array.shape[0] - time_steps
    #dim_1 = input_array.shape[1] - Since we want only one col as input
    dim_1 = 1
    x = np.zeros((dim_0, time_steps, dim_1))
    y = np.zeros((dim_0,))
    for i in range(dim_0):
        #if time_step = 60, Sequence of 0 to 60 days
        x[i] = input_array[i:time_steps+i]
        #Value of 61th day
        y[i] = input_array[time_steps+i]
    return x, y
  
  def get_data(self, x_data, batch_size, time_steps, is_test = False, col_name = None, train_cols = None):
    train_cols_ = train_cols if train_cols is not None else self.train_cols
    X_T = []
    Y_T = []
    if is_test:
      X_Val = []
      Y_Val = []
    for col in train_cols_:
      if col_name is None or col == col_name:
        idx = 0 if x_data.shape[1] == 1 else train_cols_.index(col)
        x_t, y_t = self.build_timeseries(x_data[:,idx], time_steps)
        x_t = self.trim_dataset(x_t, batch_size)
        y_t = self.trim_dataset(y_t, batch_size)
        if is_test:
          x_val, x_test_t = np.array_split(x_t, 2)
          y_val, y_test_t = np.array_split(y_t, 2)
          X_T.append(x_test_t)
          Y_T.append(y_test_t)
          X_Val.append(x_val)
          Y_Val.append(y_val)
        else:
          X_T.append(x_t)
          Y_T.append(y_t)
    if is_test:
      return X_T, Y_T, X_Val, Y_Val
    else:
      return X_T, Y_T