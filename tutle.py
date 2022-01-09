## 터틀 매매 전략 (1983)
## 변수 : 4주 진입채널, 2주 손절매 채널

## 매수 규칙
## 1) 예비신호 : 주간 채널이 직접 4주 고가 채널 중 최고점
## 2) 필터 : 직전 매매에서 손실을 보았을 때만 매매
## 3) 진입 신호 : 직전 4주 고가 채널을 상향 돌파할 때 매수
## 4) 손절매 : 직전 2주 저가 채널을 하향 돌파할 때 매도

## 매도 규칙
## 1) 예비신호 : 주간 채널이 4주 저가 채널중 최저점
## 2) 필터 : 직전 매매에서 손실을 보았을 때만 매매
## 3) 진입 신호 : 직전 4주 저가 채널을 하향 돌파할 때 매도
## 4) 손절매 : 직전 2주 고가 채널을 상향 돌파할 때 매수

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
data = pd.read_csv("./data/nasdaq.csv",parse_dates=True, index_col="Date")
data = data.sort_index(ascending=True)

status = 0  # buy or sell, neutral
trading_list = []
prev_ret_buy = -0.01
prev_ret_sell = -0.01

for i, j, k,l in zip(data.index[:-25],data.index[10:-15],data.index[20:-5],data.index[25:]):
    #주간 채널
    weekly_max = data[data.index>=k][:5].Close.max() ## 주간 채널 max
    weekly_min = data[data.index>=k][:5].Close.min() ## 주간 채널 min

    # 4주 채널
    _4w_max = data[data.index >= i][:20].Close.max() ## 4주 채널 max
    _4w_min = data[data.index >= i][:20].Close.min() ## 4주 채널 min

    # 2주 채널
    _2w_max = data[data.index >= j][:10].Close.max() ## 2주 채널 max
    _2w_min = data[data.index >= j][:10].Close.min() ## 2주 채널 min

    current_price = data[data.index == l]
    

    # 매수 시작
    if status == 0:
        if weekly_max >= _4w_max:   # 예비신호
            if current_price['High'].values >= _4w_max and prev_ret_buy < 0: # 해당일 high가 직전 4주 최고치를 돌파할 때
                entry_price = _4w_max
                entry_date = l
                status = 1
        elif weekly_min <= _4w_min:  # 예비신호
            if current_price['Low'].values <= _4w_min and prev_ret_sell < 0: # 해당일 저점이 직전 4주 최저치를 하향 돌파할 때
                entry_price = _4w_min
                entry_date = l
                status = -1

    elif status == 1:
        if current_price['Low'].values <= _2w_min:  ## 손절매 규칙 : 해당일 low가 직전 2주 최저치를 하향 돌파할 때
            exit_price = _2w_min
            exit_date = l
            prev_ret_buy = (exit_price/entry_price-1) * status
            prev_ret_sell = -0.01
            trading_list = trading_list + [entry_date,exit_date,prev_ret_buy]
            status = 0
    
    elif status == -1:
        if current_price['High'].values >= _2w_max :    ## 손절매 규칙 : 해당일 high가 직전 2주 최고치를 상향 돌파할 때
            exit_price = _2w_max
            exit_date = l
            prev_ret_sell = (exit_price/entry_price-1) * status
            prev_ret_buy = -0.01
            trading_list = trading_list + [entry_date,exit_date,prev_ret_sell]
            status = 0
    
total_ret = 1
total_ret_list = []
for i in range(0,int(len(trading_list)/3)):
    ret = trading_list[3*i+2]
    total_ret = total_ret * (1+ret)
    total_ret_list = total_ret_list + [total_ret]

print(total_ret)

plt.plot(total_ret_list)
plt.show()
        

    

