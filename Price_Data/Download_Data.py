import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader as web
import datetime as dt

start = '2001-01-01'
end = '2022-06-01'

for ticker in ticker_list:
    try:
        dataframe = web.DataReader(ticker,'yahoo',start,end)
        data = dataframe.reset_index()
        print(ticker)
        print(data.head())
        data.to_csv(f'{ticker}.csv',encoding='utf_8',index=False)
    except:
        print(f'{ticker} failed')


df1 = pd.read_csv('ADI.csv')
df1 = df1[['Date','Close']]
df1.columns = df1.columns.str.replace('Close', 'ADI')
for ticker in ticker_list[1:]:
    try:
        df2 = pd.read_csv(f'{ticker}.csv')
        if ('Close' in df2.columns):
            df2 = df2[['Date','Close']]
            df2.columns = df2.columns.str.replace('Close', ticker)
            df1 = pd.merge(df1,df2,on='Date',how='outer')
        elif ('Price' in df2.columns):
            df2['Date'] = pd.to_datetime(df2.Date)
            df2['Date'] = df2['Date'].dt.strftime('%Y-%m-%d')
            df2 = df2[['Date','Price']]
            df2.columns = df2.columns.str.replace('Price', ticker)
            df1 = pd.merge(df1,df2,on='Date',how='outer')
        else:
            print(f'{ticker} ???')
    except:
        print(ticker)
df1 = df1.sort_values(['Date'],ascending=True)
df1.fillna(value=1,inplace = True)
df1.to_csv("Combined_Price.csv",index=False)