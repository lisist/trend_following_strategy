## 던키안의 4주 채널 (1960)
## 4주 채널
## 매수 : 4주 고가 채널을 상향 돌파할 때 매수
## 최초 손절매 : 4주 저가 채널을 하향 돌파할 때 매도
## 매도 : 4주 저가 채널을 하향 돌파할 때 매도
## 최초 손절매 : 4주 고가 채널을 상향 돌파할 때 매수

## 필터 : 매수할 때 현재가가 120일 이동평균보다 높아야함, 매도할 때는 반대

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

moving_average = 120

data = pd.read_csv("./data/btcusd.csv",parse_dates=True, index_col="Date")
data = data.sort_index(ascending=True)
data['d_rolling'] = data['Close'].rolling(window=moving_average).mean()
data = data[:]

status = 0
trading_list = []

for i, j  in zip(data.index[:-20],data.index[20:]):
    _4w_max = data[data.index>=i]['High'][:20].max()
    _4w_min = data[data.index>=i]['Low'][:20].min()

    current_high = data[data.index==j]['High'].values[0]
    current_low = data[data.index==j]['Low'].values[0]
    current_price = data[data.index==j]['Close'].values[0]

    _dma = data[data.index==j]['d_rolling'].values[0]
    
    if status == 0 :
        if current_high > _4w_max  and current_price > _dma:
            status = 1
            entry_price = _4w_max
            entry_date = j
        elif current_low < _4w_min and current_price < _dma:
            status = -1
            entry_price = _4w_min
            entry_date = j
    
    elif status == 1:
        if current_low < _4w_min:
            exit_price = _4w_min
            exit_date = j
            trading_list = trading_list + [[entry_date,exit_date,status,entry_price,exit_price,exit_price/entry_price-1]]
            
            status = 0

   
    elif status == -1:
        if current_high > _4w_max:
            exit_price = _4w_max
            exit_date = j
            trading_list = trading_list + [[entry_date,exit_date,status,entry_price,exit_price,-(exit_price/entry_price-1)]]

            status = 0
            

strategy_result = pd.DataFrame(data['Close'],index=data.index)
strategy_result['Buy_sell'] = np.repeat(0,len(strategy_result.index))
prev_total_ret = 1

for start,end,state,entry_p,exit_p,pnl in trading_list:
    for j in strategy_result[(strategy_result.index >= start) & (strategy_result.index <= end)].index:
        strategy_result.at[j,'Buy_sell']=state
        strategy_result.at[j,'entry_price']=entry_p
        strategy_result.at[j,'exit_price']=exit_p

        strategy_result.at[j,'pnl'] = prev_total_ret * (1+(strategy_result.at[j,'Close']/entry_p-1)*state)
        if j == end:
            prev_total_ret = prev_total_ret * (1+(exit_p/entry_p-1)*state)
            strategy_result.at[j,'pnl'] = prev_total_ret

prev_pnl = 1
for i in strategy_result.index:
    if np.isnan(strategy_result.at[i,'pnl']):
        strategy_result.at[i,'pnl'] = prev_pnl
    else:
        prev_pnl = strategy_result.at[i,'pnl']

        

strategy_result.to_csv("result.csv")


