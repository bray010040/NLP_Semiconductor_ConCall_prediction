import pandas as pd
import datetime as dt
import json

df_money = pd.DataFrame(columns = ['Date','Money'])
transcript_score_data = pd.read_csv('/Users/a/Desktop/Cathay_Report/Cathay_Con_Call_Project/record_data.csv')
holding = {}
init_money = 1000000
filter_list = []
tmp_list = []

#generating portfolio filter
stop_buying = {}
can_buy = {} 
for i in range(len(transcript_score_data)):
    ff = transcript_score_data['F_name'][i].split('/')[2].split('_')
    date_num = f'{ff[0]}-{ff[1]}-{ff[2]}'
    if (transcript_score_data['result'][i]< -0.25):
        try:
            stop_buying[date_num].append(ff[3].split('.')[0])
        except:
            stop_buying[date_num] = [ff[3].split('.')[0]]
    else:
        try:
            can_buy[date_num].append(ff[3].split('.')[0])
        except:
            can_buy[date_num] = [ff[3].split('.')[0]]

#generating daily holding after filter
for i in range(6362):
    date_form = (dt.datetime(2004,12,31)+dt.timedelta(days=i)).strftime('%Y-%m-%d')
    try:
        if (date_form.split('-')[1]>='09'):
            un_list = pd.read_excel(f'/Users/a/Desktop/Cathay_Report/Cathay_Con_Call_Project/History_SOX_Component/SOX_{int(date_form.split("-")[0])+1}.xlsx')
        else:
            un_list = pd.read_excel(f'/Users/a/Desktop/Cathay_Report/Cathay_Con_Call_Project/History_SOX_Component/SOX_{int(date_form.split("-")[0])}.xlsx')
        un_list = list(un_list['Ticker'])
        un_list = [i.split(' ')[0] for i in un_list]
        if (date_form in stop_buying):
            for i in stop_buying[date_form]:
                filter_list.append(i)
        if (date_form in can_buy):
            filter_list = list(set(filter_list) - set(can_buy[date_form]))
        tmp_list = list(set(un_list)-set(filter_list))
        holding[date_form] = tmp_list#list(set(un_list)-set(filter_list))
    except:
        holding[date_form] = tmp_list

with open('daily_holding.json','w') as m:
    json.dump(holding,m)