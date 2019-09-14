# -*- coding: UTF-8 -*-
import pandas as pd
from pandas import Series
import numpy as np
import csv
import talib

point_value = {"XAUUSD": 10}
record_name = "result.csv"

initial_data=pd.read_csv("XAUUSD_DAY.csv")
#print(type(initial_data))  #dataframe



def write_csv(filename,info):
    filetowrite = open(filename,'a',newline="")
    writer=csv.writer(filetowrite)
    writer.writerow(info)
    filetowrite.close()

write_csv(record_name, ["code", "openPrice", "closePrice", "sign", "openDate", "closeDate",
                                    "profit", "holdBars", "sumProfits", "maxWin", "maxLoss"])

high = initial_data.high
open = initial_data.open
close = initial_data.close
low = initial_data.low
date = initial_data.date

hold_day = 0
market_position = False
open_price = 0.0
open_date = ""
high_price = 0
low_price = 0
max_loss = 0.0
tp = 0
sl = 0
sumProfits = 0.0

#find the sub_high point in initial data
sub_high = (high > high.shift(1)) & (high > high.shift(-1)) & (high > high.shift(2)) & (
        high > high.shift(-2)) & (high > high.shift(3)) & (high > high.shift(-3)) & (
                    high > high.shift(4)) & (high > high.shift(-4)) & (
                    high > high.shift(5)) & (
                    high > high.shift(-5))

initial_data["new_high"] = sub_high * high  # fins the value of the sub_high point
new_high = initial_data["new_high"]  # creat a new column 'new_high' in initial data
#print(type(new_high)) # Series type

#get the index of the high point，array type
new_high_array =np.array(new_high)
new_high_index=np.flatnonzero(new_high_array)
#print(new_high_index)
#print(type(new_high_index))

#find the sub_low point in initial data
sub_low = (low < low.shift(1)) & (low < low.shift(-1)) & (low < low.shift(2)) & (
            low < low.shift(-2)) & (low < low.shift(3)) & (
                       low < low.shift(-3)) & (low < low.shift(4)) & (
                       low < low.shift(-4)) & (low < low.shift(5)) & (
                       low < low.shift(-5))
initial_data["new_low"] = sub_low * low
new_low = initial_data["new_low"]
new_low_array =np.array(new_low)
new_low_index=np.flatnonzero(new_low_array)
#print(new_low_index)

for i in range(len(initial_data)):
    if i < 400:
        continue
    slice_data = initial_data[i - 400:i]
    slice_low = slice_data["low"]

    slice_min = slice_low.min()  # find the lowest point in each window
    # print(slice_min)
    slice_min_index = slice_low.idxmin()
    # print(slice_min_index)

    k = 0
    for k in new_high_index:
        if k > slice_min_index:
            break
    wave1 = high[k] - slice_min
    sub_high_index = k
    # print(sub_high_index)
    #print(wave1)

    j = 0
    for j in new_low_index:
        if j > sub_high_index and j > slice_min_index:
            break
    sub_low_index = j
    # print(sub_low_index)
    wave2 = high[sub_high_index] - low[sub_low_index]
    #print(wave2)



#take profit / stop loss
    tp = low[sub_low_index]+1*[high[sub_high_index]-slice_min]
    #print(tp)
    sl = low[sub_low_index]
    #print(sl)
    symbol = "XAUUSD"
    open_date = date[i]
    close_date = date[i+hold_day]
    open_price = close[i]

    #long
    if market_position == True :
        hold_day += 1
        if close[i] > high[sub_high_index]:
            pass

        # take profit
        if high[i] > tp:
            sumProfits = sumProfits + (tp - open_price)
            info = [symbol, open_price, tp, 1, open_date, close_date,
                    tp - open_price, hold_day, sumProfits,
                    high_price - open_price, max_loss]
            write_csv(record_name, info)
            market_position = False

        #stop loss
        if low[i] < sl:
            sumProfits = sumProfits + (sl - open_price)
            info = [symbol, open_price, sl, 1, open_date, close_date,
                    sl - open_price, hold_day, sumProfits,
                    high_price - open_price, max_loss]
            write_csv(record_name, info)
            market_position = 0




