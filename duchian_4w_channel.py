## 던키안의 4주 채널 (1960)
## 4주 채널
## 매수 : 4주 고가 채널을 상향 돌파할 때 매수
## 최초 손절매 : 4주 저가 채널을 하향 돌파할 때 매도
## 매도 : 4주 저가 채널을 하향 돌파할 때 매도
## 최초 손절매 : 4주 고가 채널을 상향 돌파할 때 매수

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("kospi2.csv",parse_dates=True, index_col="Date")
data = data.sort_index(ascending=True)
data['120d_rolling'] = data['Close'].rolling(window=120).mean()
data = data[120:]

status = 0
trading_list = []

for i, j  in zip(data.index[:-20],data.index[20:]):
    _4w_max = data[data.index>=i]['High'][:20].max()
    _4w_min = data[data.index>=i]['Low'][:20].min()

    current_high = data[data.index==j]['High'].values[0]
    current_low = data[data.index==j]['Low'].values[0]
    current_price = data[data.index==j]['Close'].values[0]

    _120dma = data[data.index==j]['120d_rolling'].values[0]
    
    if status == 0 :
        if current_high > _4w_max  and current_price > _120dma:
            status = 1
            entry_price = _4w_max
            entry_date = j
        elif current_low < _4w_min and current_price < _120dma:
            status = -1
            entry_price = _4w_min
            entry_date = j
    
    elif status == 1:
        if current_low < _4w_min:
            exit_price = _4w_min
            exit_date = j
            trading_list = trading_list + [entry_date,exit_date,exit_price/entry_price-1]
            
            status = 0


    
    elif status == -1:
        if current_high > _4w_max:
            exit_price = _4w_max
            exit_date = j
            trading_list = trading_list + [entry_date,exit_date,-(exit_price/entry_price-1)]

            status = 0
            


print(trading_list)

total_ret = 1
total_ret_list = []
for i in range(0,int(len(trading_list)/3)):
    ret = trading_list[3*i+2]
    total_ret = total_ret * (1+ret)
    total_ret_list = total_ret_list + [total_ret]

print(total_ret)

plt.plot(total_ret_list)
plt.show()
