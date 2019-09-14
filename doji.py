# -*- coding: UTF-8 -*-
import pandas as pd
import csv
import talib

point_value = {"XAUUSD": 10, "XAGUSD": 100, "GBPUSD": 10000, "USDJPY": 100, "EURUSD": 10000, "AUDUSD": 10000,
               "NZDUSD": 10000, "USDCAD": 10000, "USDCHF": 10000}
record_name = "result.csv"

def write_csv(filename, info):
    filetowrite = open(filename, 'a',newline="")
    writer = csv.writer(filetowrite)
    writer.writerow(info)


def strategy(symbol, data):
    write_csv(record_name, ["code", "openPrice", "closePrice", "sign", "openDate", "closeDate",
                                    "profit", "holdBars", "sumProfits", "maxWin", "maxLoss"])
    high = data.high
    open = data.open
    close = data.close
    low = data.low

    sumProfits = 0.0
    stop_loss = 5

    hold_day = 0
    marketposition = 0
    openprice = 0.0
    opendate = ""
    high_price = 0
    low_price = 0
    max_loss = 0.0 #float
    tp = 0
    sl = 0

    cci = talib.CCI(high, low, close, timeperiod=13)
    data["cci"] = cci
    data.to_csv("data.csv")


    for index, row in data.iterrows():
        # print row["date"]
        if index < 5:
            continue

        # long
        if marketposition == 1:
            hold_day += 1 #count hold_day
            if high_price < row["high"]:
                # high_price = row["high"]
                pass

            if row["low"] - openprice < max_loss:
                # max_loss = row["low"] - openprice
                pass
            
            # take profit
            if row["high"] > tp:
                sumProfits = sumProfits + (tp - openprice)
                info = [symbol, openprice, tp, 1, opendate, row["date"],
                        tp - openprice, hold_day, sumProfits,
                        high_price - openprice, max_loss]
                write_csv(record_name, info)
                marketposition = 0


            # stop loss
            if row["low"] < sl:
                sumProfits = sumProfits + (sl - openprice)
                info = [symbol, openprice, sl, 1, opendate, row["date"],
                        sl - openprice, hold_day, sumProfits,
                        high_price - openprice, max_loss]
                write_csv(record_name, info)
                marketposition = 0


        # short
        if marketposition == -1:
            pass

        if marketposition == 0:
            real_now = abs(row["open"] - row["close"]) * point_value[symbol]
            real_before_1 = abs(open[index-1] - close[index-1]) * point_value[symbol]
            real_before_2 = abs(open[index - 2] - close[index - 2]) * point_value[symbol]


            condition1 = close[index-2] < open[index-2] and real_before_2 > 10 and low[index-2] > low[index-1]
            condition2 = real_before_1 < 10
            condition3 = row["close"] > row["open"] and real_now > 10 and row["low"] > low[index-1]
            condition4 = low[index - 1] < low[index - 100:index-2].min()

            condition5 = cci[index-2] < cci[index-1] and cci[index-1] < -100

            if condition1 and condition2 and condition3 and condition4 and condition5:
                high_list = high[index-101:index-31]
                high_limit = list((high_list > high_list.shift(-1)) & (high_list > high_list.shift(-2)))
                p = 0
                for i in range(len(high_list)):

                    if high_limit[i] and high[index - 101 + i] >= high[index-101:index].max():
                        p = i
                    else:
                        high_limit[i] = False
                if p <= 0:
                    continue

                tp = row["close"] + ((high[index-101+p])-low[index - 1]) * 0.786
                sl = low[index - 1] - float(stop_loss) / point_value[symbol]

                marketposition = 1

                opendate= row["date"]
                openprice = row["close"]
                max_loss = 0.0
                high_price = row["close"]
                hold_day = 0





if __name__ == '__main__':
    symbol = "USDCHF"
    period = "240MIN"
    df = pd.read_csv("USDCHF_240MIN.csv")
    strategy(symbol, df)

