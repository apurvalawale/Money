import json
from pprint import pprint
import urllib.request
import csv
import datetime
import requests
import configparser
import platform
import matplotlib.pyplot as plt

configParser = configparser.RawConfigParser()   
configFilePath = r'Config.cfg'
configParser.read(configFilePath)
msftPath1=configParser.get('Paths', 'msftPath1')
msftPath2=configParser.get('Paths', 'msftPath2')
sgxPath=configParser.get('Paths', 'sgxPath')
saveStockDataPath=configParser.get('Paths', 'saveStockDataPath')

tickers=["T12","F99","Z74","A17U","M44U","CY6U","AU8U"]
for ticker in tickers:
    payload = {"id":ticker}
    r = requests.post(sgxPath, data=json.dumps(payload))
    if r.status_code==200:
        r.headers["Content-Type"]="application/json"
        data=r.json()
        openPrice=data["company"]["companyInfo"]["openPrice"]
        highPrice=data["company"]["companyInfo"]["highPrice"]
        lowPrice=data["company"]["companyInfo"]["lowPrice"]
        closePrice=data["company"]["companyInfo"]["closePrice"]
        volume=data["company"]["companyInfo"]["volume"]
        enterpriseValue=data["company"]["companyInfo"]["enterpriseValue"]
        BVperShare=data["company"]["companyInfo"]["bvShare"]
        eps=data["company"]["companyInfo"]["eps"]
        netIncome=data["company"]["companyInfo"]["netIncome"]
        netProfitMargin=data["company"]["companyInfo"]["netProfitMargin"]
        peRatio=data["company"]["companyInfo"]["peRatio"]
        totalDebtEquity=data["company"]["companyInfo"]["totalDebtEquity"]

        if platform.system()=="Windows":
            fields=[datetime.datetime.now().strftime("%Y-%m-%d"),ticker,openPrice,highPrice,lowPrice,closePrice,volume,enterpriseValue,BVperShare,eps,netIncome,netProfitMargin,peRatio,totalDebtEquity]
            with open(saveStockDataPath+ticker+".csv", "a",newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
    else:
        if platform.system()=="Windows":        
            with open(saveStockDataPath+"log.txt", "a",newline='') as f:
                writer = csv.writer(f)
                fields=[datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),ticker,"Stock details wasn't found"]
                writer.writerow(fields)



