#!/usr/bin/python3.6
# -*- coding: utf8 -*-
# -*- date: 2019/10/18 -*-
# Author:joker2770

#先引入后面可能用到的包（package）
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import mpl_finance as mpf
import matplotlib.ticker as ticker
from matplotlib.pylab import date2num
import seaborn as sns
sns.set()

#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
#引入TA-Lib库
import talib as ta
#获取交易数据用于示例分析
import tushare as ts

#1.2.48
print(ts.__version__)

################################################################
'''
请到tusahre pro官网获取token
'''
token='036c29c2e44d587268a0c1f0a5fcd10dbf3c144dbc367da3f2237bed'
ts.set_token(token)
pro = ts.pro_api(token)
################################################################

#代码和数据获取
def get_data(code,start='20190101',end='20190712'):
 df=ts.pro_bar(ts_code=code,asset='I',adj='qfq', start_date=start, end_date=end)
 return df
df = pro.index_daily(ts_code='000300.SH', start_date='20190101')
df.index=pd.to_datetime(df.trade_date)
df = df.sort_index()[['open', 'close', 'high', 'low','vol']]
df.head()

df[['open', 'close', 'high', 'low']].plot(figsize=(12,5))
plt.title('沪深300指数',size=15)
plt.show()

#设定日期格式
def format_date(x,pos):
 if x<0 or x>len(date_tickers)-1:
  return ''
 return date_tickers[int(x)]
#提取原始日期格式
df['dates'] = np.arange(0, len(df))
df=df.reset_index()
df['trade_date2'] = df['trade_date'].copy()
df['trade_date'] = df['trade_date'].map(date2num)
date_tickers = (df.trade_date2).apply(lambda x:x.strftime('%Y%m%d')).values
# 画子图
figure = plt.figure(figsize=(12, 9))
gs = GridSpec(3, 1)
ax1 = plt.subplot(gs[:2, :])
ax2 = plt.subplot(gs[2, :])
# 画K线图
mpf.candlestick_ochl(
 ax=ax1,
 quotes=df[['dates', 'open', 'close', 'high', 'low']].values,
 width=0.7,
 colorup='r',
 colordown='g',
 alpha=0.7)
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
# 画均线，均线可使用talib来计算
for ma in ['5', '20', '30', '60', '120']:
 df[ma]=df.close.rolling(int(ma)).mean()
 ax1.plot(df['dates'], df[ma])
ax1.legend()
ax1.set_title('沪深300指数K线图', fontsize=15)
ax1.set_ylabel('指数')
# 画成交量
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
df['up'] = df.apply(lambda row: 1 if row['close'] >= row['open'] else 0, axis=1)
ax2.bar(df.query('up == 1')['dates'], df.query('up == 1')['vol'], color='r', alpha=0.7)
ax2.bar(df.query('up == 0')['dates'], df.query('up == 0')['vol'], color='g', alpha=0.7)
ax2.set_ylabel('成交量')
plt.show()
