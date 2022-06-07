import json
import pandas as pd
import datetime as dt
import bokeh
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import Range1d, Legend
from bokeh.layouts import column
from bokeh.plotting import figure, output_file, show
import copy

daily_money = {}
init_money = 300000
base_money = 0
temp_hold = {}
for ticker in df1.columns:
    temp_hold[ticker] = 0
for i in range(6362):
    date_form = (dt.datetime(2004,12,31)+dt.timedelta(days=i)).strftime('%Y-%m-%d')
    if (date_form in list(df1['Date'])):
        #print(1)
        base_money = 0
        tmp_data = df_backup[df_backup['Date']==date_form]
        for ticker in temp_hold:
            try:
                if (float(tmp_data[ticker])==1):
                    continue
                if (temp_hold[ticker]>0 and ticker not in holding[date_form]):
                    init_money+=((temp_hold[ticker]*float(tmp_data[ticker])))
                    temp_hold[ticker] = 0
                elif (temp_hold[ticker]==0 and ticker in holding[date_form]):
                    temp_hold[ticker] = (max(int(init_money/30),10000))/float(tmp_data[ticker])
                    init_money-=max(int(init_money/30),10000)
                    base_money+=10000
                elif (temp_hold[ticker]>0 and ticker in holding[date_form]):
                    base_money+=(temp_hold[ticker]*float(tmp_data[ticker]))
            except:
                #print(f'{date_form}:{ticker}')
                pass
    daily_money[date_form] = init_money+base_money



def plot_return_chart(daily_money, output_name='MyStrategy_Return'):
    append_list = {}
    #global calendar
    #global t_table
    df = pd.DataFrame(columns=['Date_time', 'Datetime2', 'Money'])
    for i in range(6362):
        date_form = (dt.datetime(2004,12,31)+dt.timedelta(days=i)).strftime('%Y-%m-%d')
            #append_list['Date_time'] = pd.to_datetime(f'{str(i)[:4]}/{str(i)[4:6]}/{str(i)[6:]},{j}', format="%m/%d/%Y,%H:%M:%S")
        append_list['Date_time'] = pd.to_datetime(f'{date_form}',format="%Y-%m-%d")
        append_list['Datetime2'] = f"{date_form}"
        append_list['Money'] = daily_money[date_form]
        df = df.append(append_list, ignore_index=True)
    
    df2 = pd.read_csv('SOX.csv')
    df2['Close'] = (df2['Close']/df2['Close'][0])*300000
    df2['Datetime2'] = df2['Date']
    df2['Date'] = pd.to_datetime(df2['Date'])
    hover = HoverTool(
        tooltips=[
            ("Date", "@Datetime2"),
            ("Money", "@Money"),
            ("SOX", "@Close")],
        formatters={"@Date_time": "datetime"})

    p = figure(
        plot_width=1280,
        plot_height=960,
        x_axis_type="datetime",
        tools=[hover, 'pan,box_zoom,reset,save'])
    p.title.text = 'Money_Chart'
    source = ColumnDataSource(df)
    source2 = ColumnDataSource(df2)
    p.line(x="Date_time", y="Money", line_width=2, color='blue', alpha=0.8,
           muted_color='blue', muted_alpha=0.2, legend_label='Money', source=source)
    p.line(x="Date",y="Close", line_width=2, color='red', alpha=0.8,
           muted_color='red', muted_alpha=0.2, legend_label='SOX',source=source2)
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    output_file(f'{output_name}.html')
    show(p)

import copy
def generate_analysis_frame(dataf, file_name):
    #global calendar
    a = pd.DataFrame(columns=['Date', 'Money'])
    final_table = pd.DataFrame(columns=['Type', 'Content'])
    for i in range(6362):
        date_form = (dt.datetime(2004,12,31)+dt.timedelta(days=i)).strftime('%Y-%m-%d')
        append_list = {}
        append_list['Money'] = dataf[date_form]#["10:02:00"]
        append_list['Date'] = pd.to_datetime(f'{date_form}')
        a = a.append(append_list, ignore_index=True)

    # -------------------------------------------------
    total_return = (dataf['2022-06-01']/dataf['2004-12-31']) - 1
    append_list = {}
    append_list['Type'] = 'Total_Return'
    append_list['Content'] = total_return
    final_table = final_table.append(append_list, ignore_index=True)
    # -------------------------------------------------
    IRR = (1 + total_return) ** (365 / len(a)) - 1
    append_list = {}
    append_list['Type'] = 'Internal_Rate_Return'
    append_list['Content'] = IRR
    final_table = final_table.append(append_list, ignore_index=True)
    # -------------------------------------------------
    volatility = RISK(a)
    append_list = {}
    append_list['Type'] = 'Volatility'
    append_list['Content'] = float(volatility)
    final_table = final_table.append(append_list, ignore_index=True)
    # -------------------------------------------------
    sharpe_ratio = SHARPE(a)
    append_list = {}
    append_list['Type'] = 'Sharpe_Ratio'
    append_list['Content'] = float(sharpe_ratio)
    final_table = final_table.append(append_list, ignore_index=True)
    # ------------------------------------------------
    md, md_start, md_end, md_continuos = MDD(a)
    append_list = {}
    append_list['Type'] = 'Max_Drawdown'
    append_list['Content'] = md
    final_table = final_table.append(append_list, ignore_index=True)
    append_list = {}
    append_list['Type'] = 'Max_Drawdown_Start'
    append_list['Content'] = md_start
    final_table = final_table.append(append_list, ignore_index=True)
    append_list = {}
    append_list['Type'] = 'Max_Drawdown_End'
    append_list['Content'] = md_end
    final_table = final_table.append(append_list, ignore_index=True)
    append_list = {}
    append_list['Type'] = 'Max_Drawdown_Continuos_Days'
    append_list['Content'] = md_continuos
    final_table = final_table.append(append_list, ignore_index=True)
    # ------------------------------------------------

plot_return_chart(daily_money,'PnL')
generate_analysis_frame(daily_money,'analysis_frame')