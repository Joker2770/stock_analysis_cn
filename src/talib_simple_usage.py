#!/usr/bin/python3.6

#先引入后面可能用到的包（package）
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt

#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
#引入TA-Lib库
import talib as ta
#获取交易数据用于示例分析
import tushare as ts
###################################################
'''
股票代码
'''
stock_code = "000001"
'''
起始日期
'''
start_time = "2019-08-01"
###################################################
def get_data(code,start='2015-01-01'):
    df=ts.get_k_data(code,start)
    df.index=pd.to_datetime(df.date)
    df=df.sort_index()
    return df
#获取上证指数收盘价、最高、最低价格
df=get_data(stock_code)[['open','close','high','low']]
#开盘价，最高价，最低价，收盘价的均值
df['average']=ta.AVGPRICE(df.open,df.high,df.low,df.close)
#最高价，最低价的均值
df['median']=ta.MEDPRICE(df.high,df.low)
#最高价，最低价，收盘价的均值
df['typical']=ta.TYPPRICE(df.high,df.low,df.close)
#最高价，最低价，收盘价的加权
df['weight']=ta.WCLPRICE(df.high,df.low,df.close)
df.head()

'''
通用函数名：MA
代码：ta.MA(close,timeperiod=30,matype=0)
移动平均线系列指标包括：SMA简单移动平均线、
                    EMA指数移动平均线、
                    WMA加权移动平均线、
                    DEMA双移动平均线、
                    TEMA三重指数移动平均线、
                    TRIMA三角移动平均线、
                    KAMA考夫曼自适应移动平均线、
                    MAMA为MESA自适应移动平均线、
                    T3三重指数移动平均线。
其中，close为收盘价，时间序列，timeperiod为时间短，默认30天，指标类型matype分别对应：0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
'''
types=['SMA','EMA','WMA','DEMA','TEMA',
'TRIMA','KAMA','MAMA','T3']
df_ma=pd.DataFrame(df.close)
for i in range(len(types)):
    df_ma[types[i]]=ta.MA(df.close,timeperiod=5,matype=i)
df_ma.tail()
df_ma.loc[start_time:].plot(figsize=(16,6))
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title('上证指数各种类型移动平均线',fontsize=15)
plt.xlabel('')
plt.show()

'''
计算方法：首先计出过去 N 日收巿价的标准差 SD(Standard Deviation) ，通常再乘 2 得出 2 倍标准差
        ， Up 线为 N日平均线加 2 倍标准差， Down 线则为 N日平均线减 2 倍标准差。
代码：ta.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
'''
H_line,M_line,L_line=ta.BBANDS(df.close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
df1=pd.DataFrame(df.close,index=df.index,columns=['close'])
df1['H_line']=H_line
df1['M_line']=M_line
df1['L_line']=L_line
df1.tail()
df1.loc[start_time:].plot(figsize=(12,6))
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title(u'上证指数布林线',fontsize=15)
plt.xlabel('')
plt.show()


#画5、30、120、250指数移动平均线
N=[5,30,120,250]
for i in N:
    df['ma_'+str(i)]=ta.EMA(df.close,timeperiod=i)
df.tail()
df.loc[start_time:,['close','ma_5','ma_30','ma_120','ma_250']].plot(figsize=(16,6))
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.title('上证指数走势',fontsize=15)
plt.xlabel('')
plt.show()

