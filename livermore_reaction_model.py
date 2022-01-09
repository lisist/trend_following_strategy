## 리버모어 반응모델 (1900)

## 매수 규칙
## 1) 예비신호 : 다우 추세가 하락에서 상승으로 전환, 새로운 상승 추세에 반발하는 두 번의 되돌림 반응
## 2) 진입신호 : 직전 스윙 포인트의 고점을 돌파할 때 매수
## 3) 손절매 : 직전 스윙 포인트의 저점을 돌파할 때 매도

## 매도 규칙
## 1) 예비신호 : 다우 추세가 상승에서 하락으로 전환, 새로운 하락 추세에 반발하는 두 번의 되돌림 반응
## 2) 진입신호 : 직전 스윙 포인트의 저점을 돌파할 때 매수
## 3) 손절매 : 직전 스윙 포인트의 고점을 돌파할 때 매도

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
data = pd.read_csv("./data/nasdaq.csv",parse_dates=True, index_col="Date")
data = data.sort_index(ascending=True)
data = data[-200:]

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

prepare_signal = 0
reaction = 0 

data.to_csv("data.csv")

# for i in data.index:
#     current_high = data[data.index==i]['High'].values[0]
#     current_open = data[data.index==i]['Open'].values[0]
#     current_low = data[data.index==i]['Low'].values[0]
#     prev_peak = data[data.index==i]['peak'].values[0]
#     prev_bottom = data[data.index==i]['bottom'].values[0]

#     if state == 0:
#         # 1) 다우 추세가 하락에서 상승으로 전환한다면 예비 신호
#         if prepare_signal == 0:
#             if current_high > prev_peak:
#                 prepare_signal = 1 ## prepare to buy
#             elif current_low < prev_bottom:
#                 prepare_signal = -1 ## prepare to sell  

#         # 2) 예비 신호가 떴는데 상승세 되돌림이 있다면 reaction += 1
#         elif prepare_signal == 1:
            


#         # 3) 만약 reaction >= 2 and prev_peak < current high 라면 buy signal



#     elif state == 1:
#         pass
#     elif state == -1:
#         pass