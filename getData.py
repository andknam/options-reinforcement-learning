import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import time


def options_chain(symbol):
    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    lastDay = datetime.date(2022, 4, 29)
    now = str(datetime.datetime.now())
    datetimeExps =[]

    for day in exps:
        dayList = day.split("-")
        expDay = datetime.date(int(dayList[0]), int(dayList[1]), int(dayList[2]))
        if lastDay >= expDay:
            datetimeExps.append(str(expDay))

    exps = tuple(datetimeExps)

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.concat([pd.DataFrame(), opt.calls, opt.puts])
        opt['expirationDate'] = e
        options = pd.concat([options, opt], ignore_index=True)

    if options.shape == (0,0):
        return pd.DataFrame()
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 # Calculate the midpoint of the bid-ask
    
    # Drop unnecessary and meaningless columns
    options = options.drop(columns = ['contractSize', 'currency', 'lastTradeDate', 'lastPrice'])
    
    info = tk.info
    sector = [info["sector"] for i in range(len(options))]
    industry = [info["industry"] for i in range(len(options))]
    grossMargins = [info["grossMargins"] for i in range(len(options))]
    targetLowPrice = [info["targetLowPrice"] for i in range(len(options))]
    recommendationKey = [info["recommendationKey"] for i in range(len(options))]
    targetMedianPrice = [info["targetMedianPrice"] for i in range(len(options))]
    currentPrice = [info["currentPrice"] for i in range(len(options))]
    targetMeanPrice = [info["targetMeanPrice"] for i in range(len(options))]
    targetHighPrice = [info["targetHighPrice"] for i in range(len(options))]
    pegRatio = [info["pegRatio"] for i in range(len(options))]
    forwardPE = [info["forwardPE"] for i in range(len(options))]
    fiftyDayAverage = [info["fiftyDayAverage"] for i in range(len(options))]
    # trailingPegRatio = [info["trailingPegRatio"] for i in range(len(options))]
    recommendationMean = [info["recommendationMean"] for i in range(len(options))]
    nowList = [now for i in range(len(options))]

    options.insert(options.shape[1], "sector", sector, allow_duplicates=True)
    options.insert(options.shape[1], "industry", industry, allow_duplicates=True)
    options.insert(options.shape[1], "grossMargins", grossMargins, allow_duplicates=True)
    options.insert(options.shape[1], "targetLowPrice", targetLowPrice, allow_duplicates=True)
    options.insert(options.shape[1], "recommendationKey", recommendationKey, allow_duplicates=True)
    options.insert(options.shape[1], "targetMedianPrice", targetMedianPrice, allow_duplicates=True)
    options.insert(options.shape[1], "currentPrice", currentPrice, allow_duplicates=True)
    options.insert(options.shape[1], "targetMeanPrice", targetMeanPrice, allow_duplicates=True)
    options.insert(options.shape[1], "targetHighPrice", targetHighPrice, allow_duplicates=True)
    options.insert(options.shape[1], "pegRatio", pegRatio, allow_duplicates=True)
    options.insert(options.shape[1], "forwardPE", forwardPE, allow_duplicates=True)
    options.insert(options.shape[1], "fiftyDayAverage", fiftyDayAverage, allow_duplicates=True)
    # options.insert(options.shape[1], "trailingPegRatio", trailingPegRatio, allow_duplicates=True)
    options.insert(options.shape[1], "recommendationMean", recommendationMean, allow_duplicates=True)
    options.insert(options.shape[1], "recordTime", nowList, allow_duplicates=True)

    return options


def controller(target, totalList):
    now = datetime.datetime.now()
    print(target[0], now)
    waitTime = (target[0] - now).total_seconds()
    print(waitTime)
    time.sleep(waitTime)
    f = open("data_4-29-22.csv", "a")
    count = 0
    errCount = 0
    for ticker in totalList:
        try:
            info = options_chain(ticker)
            if not info.empty:
                count += 1
                print("Count:", count, "Ticker:", ticker, "Shape:", info.shape)
                f.write(info.to_csv(index=False, header=None))
        except Exception as e:
            errCount += 1
            print(f"Count: {errCount} Ticker: {ticker} Error: {e}")
    f.close()

    old = target.pop(0)
    target.append(old + datetime.timedelta(days=1))
    controller(target, totalList)

def getList():
    f = open("tickerList.txt", "r")
    Lines = f.readlines()
    arr = []

    for line in Lines:
        arr.append(line.strip("\n"))
    
    return arr

totalList = getList()

# target = [datetime.datetime.combine(datetime.date.today(), datetime.time(hour=15)),
# datetime.datetime.combine(datetime.date.today(), datetime.time(hour=18)),
# datetime.datetime.combine(datetime.date.today(), datetime.time(hour=21))]

target= [datetime.datetime.combine(datetime.datetime.now(), datetime.time(hour=10, minute=17))]


f = open("data_4-29-22.csv", "a")
f.write("contractSymbol,strike,bid,ask,change,percentChange,volume,openInterest,impliedVolatility,inTheMoney,expirationDate,CALL,mark,sector,industry,grossMargins,targetLowPrice,recommendationKey,targetMedianPrice,currentPrice,targetMeanPrice,targetHighPrice,pegRatio,forwardPE,fiftyDayAverage,recommendationMean,recordTime\n")
f.close()
controller(target, totalList)
