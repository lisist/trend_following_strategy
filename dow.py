## 다우이론 (1900)

## 매수 규칙
## 1) 다우 추세가 하락에서 상승으로 반전
## 2) 손절매 : 다우 추세가 상승에서 하락으로 반전

## 매도 규칙
## 1) 다우 추세가 상승에서 하락으로 반전
## 2) 손절매 : 다우 추세가 하락에서 상승으로 반전


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
data = pd.read_csv("./data/nasdaq.csv",parse_dates=True, index_col="Date")
data = data.sort_index(ascending=True)
data = data[:]

local_peak = data[0:1]['High'].values[0]
local_bottom = data[0:1]['Low'].values[0]

local_peak_list = []
local_bottom_list =[]

state = 0
trading_list = []


for i in data.index[1:-2]:
    prev_high = data[data.index<=i][-2:-1]['High'].values[0]
    post_high = data[data.index>i][0:1]['High'].values[0]
    current_high = data[data.index==i]['High'].values[0]
    
    if current_high > prev_high and current_high > post_high:
        local_peak = current_high
    
    local_peak_list = local_peak_list + [local_peak]

    prev_low = data[data.index<=i][-2:-1]['Low'].values[0]
    post_low = data[data.index>i][0:1]['Low'].values[0]
    current_low = data[data.index==i]['Low'].values[0]
    
    if current_low < prev_low and current_low > post_low:
        local_bottom = current_low
    
    local_bottom_list = local_bottom_list + [local_bottom]


data = data[3:]
data['peak'] = local_peak_list
data['bottom'] = local_bottom_list

fee= 0.001 # 0.1% 수준 fee

for i in data.index:
    current_high = data[data.index==i]['High'].values[0]
    current_low = data[data.index==i]['Low'].values[0]
    prev_peak = data[data.index==i]['peak'].values[0]
    prev_bottom = data[data.index==i]['bottom'].values[0]


    if state == 0 and current_high > prev_peak:
        state = 1
        entry_price = prev_peak
        entry_date = i
    elif state == 0 and current_low < prev_bottom:
        state = -1
        entry_price = prev_bottom
        entry_date = i
    elif state == 1 and current_low < prev_bottom:
        state = -1
        exit_price = prev_bottom
        exit_date = i
        trading_list = trading_list + [entry_date,exit_date,exit_price/entry_price-1-fee]

        entry_price = prev_bottom
        entry_date = i
    elif state == -1 and current_high > prev_peak:
        state = 1
        exit_price = prev_peak
        exit_date = i
        trading_list = trading_list + [entry_date,exit_date,-(exit_price/entry_price-1)-fee]

        entry_price = prev_peak
        entry_date = i
    

total_ret = 1
total_ret_list = []
for i in range(0,int(len(trading_list)/3)):
    ret = trading_list[3*i+2]
    total_ret = total_ret * (1+ret)
    total_ret_list = total_ret_list + [total_ret]

print(total_ret)

plt.plot(total_ret_list)
plt.show()





