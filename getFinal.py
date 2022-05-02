import pandas as pd
import datetime
def getOurData(dataFile, resFile, resDay, finalFile):
    fData = open(dataFile, "r")
    dataLines = fData.readlines()

    fRes = open(resFile, "r")
    dataRes = fRes.readlines()

    resDict = {}
    for line in dataRes:
        arr = line.split(",")
        resDict[arr[0]] = arr[1] 
    # print(resDict)

    # finalData = ["Symbol", "Strike", "Implied Volatility", "In the Money", "Expiration Date", "Call", "Mark", "Sector", "Industry", "Record Time", "Success", "Profit"]
    finalData = []

    for line in dataLines:
        try:
            arr = line.split(",")
            if arr[10] == resDay and getTicker(arr[0]) in resDict.keys() and float(arr[6]) >= 15:
                dataApp = []
                dataApp.append(getTicker(arr[0]))
                dataApp.append(arr[1])
                dataApp.append(arr[19])

                dataApp.append(arr[8])
                dataApp.append(arr[6])
                dataApp.append(arr[9])
                dataApp.append(arr[10])
                dataApp.append(arr[11])
                dataApp.append(arr[12])
                dataApp.append(arr[13])
                dataApp.append(arr[14])
                dataApp.append(arr[26].strip("\n"))
                dataApp.append((datetime.date.fromisoformat(arr[10]) - datetime.date.fromisoformat(arr[26].split(" ")[0])).days)

                if arr[11] == "True": 
                    dataApp.append(float(arr[12]) + float(arr[1]))
                else: 
                    dataApp.append(float(arr[1]) - float(arr[12]))
                dataApp.append(resDict[getTicker(arr[0])])
                dataApp.append(str(round(((float(arr[12]) + float(arr[1]) - float(arr[19])) / float(arr[19])) * 100, 3)))

                if arr[11] == "True":
                    succ = "0" if (float(resDict[getTicker(arr[0])]) - (float(arr[12]) + float(arr[1]))) < 0 else "1"
                    profit = float(resDict[getTicker(arr[0])]) - (float(arr[12]) + float(arr[1]))
                else:
                    succ = "0" if ((float(arr[1]) - float(arr[12])) - float(resDict[getTicker(arr[0])])) < 0 else "1"
                    profit = float((float(arr[1]) - float(arr[12])) - float(resDict[getTicker(arr[0])]))

                dataApp.append(succ)
                dataApp.append(profit)

                finalData.append(dataApp)
        except Exception as e:
            print(f"Error: {e}")
            # print("1", arr[12], "2", arr[1], "3", arr[19])
    
    finalDF = pd.DataFrame(finalData, columns=["Symbol", "Strike", "Current Price", "Implied Volatility", "Volume", "In the Money", "Expiration Date", "Call", "Mark", "Sector", "Industry", "Record Time", "Days to Expire", "Breakeven Price", "Final Price", "Needed Percent Change", "Success", "Profit"])

    f = open(finalFile, "a")
    f.write(finalDF.to_csv(index=False, header=False))
    f.close()

    # print(finalRes)

def getTicker(string):
    res = ""
    for i in string:
        if i.isdigit():
            break
        res += i
    return res        



data1 = ["data_3-9-22.csv", "data_3-10-22.csv", "data_3-11-22.csv"]
res1 = "results_03-11.csv"

data2 = ["data_3-16-22.csv", "data_3-17-22.csv", "data_3-18-22.csv"]
res2 = "results_03-18.csv"

data3 = ["data_3-21-22.csv", "data_3-22-22.csv", "data_3-23-22.csv", "data_3-24-22.csv", "data_3-25-22.csv"]
res3 = "results_03-25.csv"

data4 = ["data_3-28-22.csv", "data_3-29-22.csv", "data_3-30-22.csv", "data_3-31-22.csv", "data_4-01-22.csv"]
res4 = "results_04-01.csv"

data5 = ["data_4-04-22.csv", "data_4-05-22.csv", "data_4-06-22.csv", "data_4-07-22.csv", "data_4-08-22.csv"]
res5 = "results_04-08.csv"

data6 = ["data_4-11-22.csv", "data_4-12-22.csv", "data_4-13-22.csv", "data_4-14-22.csv"] # No Friday cause of Good Friday
res6 = "results_04-14.csv"

data7 = ["data_4-18-22.csv", "data_4-19-22.csv", "data_4-20-22.csv", "data_4-21-22.csv", "data_4-22-22.csv"]
res7 = "results_04-22.csv"



def week1():
    f = open("finalData_1_t.csv", "w")
    f.write("Symbol,Strike,Current Price,Implied Volatility,Volume,In the Money,Expiration Date,Call,Mark,Sector,Industry,Record Time,Days to Expire,Breakeven Price,Final Price,Needed Percent Change,Success,Profit\n")
    f.close()
    for i in data1:
        getOurData(i, res1, "2022-03-11", "finalData_1_t.csv")

def week2():
    f = open("finalData_2_t.csv", "w")
    f.write("Symbol,Strike,Current Price,Implied Volatility,Volume,In the Money,Expiration Date,Call,Mark,Sector,Industry,Record Time,Days to Expire,Breakeven Price,Final Price,Needed Percent Change,Success,Profit\n")
    f.close()
    for i in data1:
        getOurData(i, res2, "2022-03-18", "finalData_2_t.csv")
    for i in data2:
        getOurData(i, res2, "2022-03-18", "finalData_2_t.csv")
    
def week3():
    f = open("finalData_3_t.csv", "w")
    f.write("Symbol,Strike,Current Price,Implied Volatility,Volume,In the Money,Expiration Date,Call,Mark,Sector,Industry,Record Time,Days to Expire,Breakeven Price,Final Price,Needed Percent Change,Success,Profit\n")
    f.close()
    for i in data1:
        getOurData(i, res3, "2022-03-25", "finalData_3_t.csv")
    for i in data2:
        getOurData(i, res3, "2022-03-25", "finalData_3_t.csv")
    for i in data3:
        getOurData(i, res3, "2022-03-25", "finalData_3_t.csv")

def week4():
    f = open("finalData_4_t.csv", "w")
    f.write("Symbol,Strike,Current Price,Implied Volatility,Volume,In the Money,Expiration Date,Call,Mark,Sector,Industry,Record Time,Days to Expire,Breakeven Price,Final Price,Needed Percent Change,Success,Profit\n")
    f.close()
    for i in data1:
        getOurData(i, res4, "2022-04-01", "finalData_4_t.csv")
    for i in data2:
        getOurData(i, res4, "2022-04-01", "finalData_4_t.csv")
    for i in data3:
        getOurData(i, res4, "2022-04-01", "finalData_4_t.csv")
    for i in data4:
        getOurData(i, res4, "2022-04-01", "finalData_4_t.csv")

def week5():
    f = open("finalData_5_t.csv", "w")
    f.write("Symbol,Strike,Current Price,Implied Volatility,Volume,In the Money,Expiration Date,Call,Mark,Sector,Industry,Record Time,Days to Expire,Breakeven Price,Final Price,Needed Percent Change,Success,Profit\n")
    f.close()
    for i in data1:
        getOurData(i, res5, "2022-04-08", "finalData_5_t.csv")
    for i in data2:
        getOurData(i, res5, "2022-04-08", "finalData_5_t.csv")
    for i in data3:
        getOurData(i, res5, "2022-04-08", "finalData_5_t.csv")
    for i in data4:
        getOurData(i, res5, "2022-04-08", "finalData_5_t.csv")
    for i in data5:
        getOurData(i, res5, "2022-04-08", "finalData_5_t.csv")

def week6():
    f = open("finalData_6_t.csv", "w")
    f.write("Symbol,Strike,Current Price,Implied Volatility,Volume,In the Money,Expiration Date,Call,Mark,Sector,Industry,Record Time,Days to Expire,Breakeven Price,Final Price,Needed Percent Change,Success,Profit\n")
    f.close()
    for i in data1:
        getOurData(i, res6, "2022-04-14", "finalData_6_t.csv")
    for i in data2:
        getOurData(i, res6, "2022-04-14", "finalData_6_t.csv")
    for i in data3:
        getOurData(i, res6, "2022-04-14", "finalData_6_t.csv")
    for i in data4:
        getOurData(i, res6, "2022-04-14", "finalData_6_t.csv")
    for i in data5:
        getOurData(i, res6, "2022-04-14", "finalData_6_t.csv")
    for i in data6:
        getOurData(i, res6, "2022-04-14", "finalData_6_t.csv")

def week7():
    f = open("finalData_7_t.csv", "w")
    f.write("Symbol,Strike,Current Price,Implied Volatility,Volume,In the Money,Expiration Date,Call,Mark,Sector,Industry,Record Time,Days to Expire,Breakeven Price,Final Price,Needed Percent Change,Success,Profit\n")
    f.close()
    for i in data1:
        getOurData(i, res7, "2022-04-22", "finalData_7_t.csv")
    for i in data2:
        getOurData(i, res7, "2022-04-22", "finalData_7_t.csv")
    for i in data3:
        getOurData(i, res7, "2022-04-22", "finalData_7_t.csv")
    for i in data4:
        getOurData(i, res7, "2022-04-22", "finalData_7_t.csv")
    for i in data5:
        getOurData(i, res7, "2022-04-22", "finalData_7_t.csv")
    for i in data6:
        getOurData(i, res7, "2022-04-22", "finalData_7_t.csv")
    for i in data7:
        getOurData(i, res7, "2022-04-22", "finalData_7_t.csv")

# week1()
# week2()
# week3()
# week4()
# week5()
# week6()
# week7()