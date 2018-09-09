import json
from pprint import pprint
import urllib.request
import csv
import datetime
import requests
import configparser
import platform

configParser = configparser.RawConfigParser()   
configFilePath = r'Config.cfg'
configParser.read(configFilePath)
msftPath1=configParser.get('Paths', 'msftPath1')
msftPath2=configParser.get('Paths', 'msftPath2')
sgxPath=configParser.get('Paths', 'sgxPath')
saveStockDataPath=configParser.get('Paths', 'saveStockDataPath')

tickers=["CY6U","A17U","AU8U","M44U"]
for companyTicker in tickers:
    response=urllib.request.urlopen(msftPath1+companyTicker+msftPath2)
    content=response.read()
    data = json.loads(content.decode("utf8"))
    response.close()

    #Number of items under Stat
    #pprint("Length: "+str(len(data["stockEntityDetails"]["Stat"])))

    #check if object exists
    stockEntityObject=data.get("stockEntityDetails")
    if stockEntityObject:
        #Ticker
        ticker=data["stockEntityDetails"]["Stat"][0]["Tkr"]
        pprint(ticker)
        #Stock Price
        stockPrice=data["stockEntityDetails"]["Stat"][0]["Sp"]
        pprint(stockPrice)
        #Market Capital
        marketCapital=data["stockEntityDetails"]["Stat"][0]["Mc"]
        pprint(marketCapital)
        #Net Income
        netIncome=data["stockDetailsV2"]["Fh"]["In"]
        pprint(netIncome)
        #Shares Outstanding
        outstandingShares=data["stockEntityDetails"]["Stat"][0]["shrsOs"]
        pprint(outstandingShares)
        #Book Value per Share
        bookValuePerShare=data["stockEntityDetails"]["Stat"][0]["Bvps"]
        pprint(bookValuePerShare)
        #Earnings per Share
        earningsPerShare=data["stockEntityDetails"]["Stat"][0]["Eps"]
        pprint(earningsPerShare)
        #Price to Earnings ratio
        priceToEarningsRatio=data["stockEntityDetails"]["Stat"][0]["Pe"]
        pprint(priceToEarningsRatio)
        #Dividend Yield
        dividendYield=data["stockEntityDetails"]["Stat"][0]["Dy"]
        pprint(dividendYield)
        #Forward Dividend Yield
        forwardDividendYield=data["stockEntityDetails"]["Stat"][0]["FwdDYld"]
        pprint(forwardDividendYield)
        #Debt To Equity ratio
        debtToEquityRatio=data["stockEntityDetails"]["Stat"][0]["De"]
        pprint(debtToEquityRatio)

        #Enterprise Value
        enterpriseValue=data["shareStatistics"][0]["EpVl"]
        pprint(enterpriseValue)

        #Last Dividend Amount Paid
        #pprint(data["stockEntityDetails"]["Stat"][0]["AmtPd"])
        #Last Ex-Dividend Date
        #pprint(data["stockEntityDetails"]["Stat"][0]["ExdDt"])
        #Payout Ratio
        payoutRatio=data["stockEntityDetails"]["Stat"][0]["PytRt"]
        pprint(payoutRatio)
        #Quick Ratio
        quickRatio=data["stockEntityDetails"]["Stat"][0]["QckRt"]
        pprint(quickRatio)

        payload = {"id":ticker}
        r = requests.post(sgxPath, data=json.dumps(payload))
        r.headers["Content-Type"]="application/json"
        data=r.json()
        stockHighPrice=data["price"]["highPrice"]
        #Stock Low Price
        stockLowPrice=data["price"]["lowPrice"]

        if platform.system()=="Windows":
            fields=[datetime.datetime.now().strftime("%Y-%m-%d"),ticker,stockPrice,marketCapital,netIncome,outstandingShares,enterpriseValue,bookValuePerShare,earningsPerShare,priceToEarningsRatio,dividendYield,forwardDividendYield,debtToEquityRatio,payoutRatio,quickRatio,stockHighPrice,stockLowPrice]
            with open(saveStockDataPath+companyTicker+".csv", "a",newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
    else:
        if platform.system()=="Windows":        
            with open(saveStockDataPath+"log.txt", "a",newline='') as f:
                writer = csv.writer(f)
                fields=[datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),companyTicker,"Stock details wasn't found"]
                writer.writerow(fields)



