import datetime
import random
import nolds
from slintraday import simulate_trade,extract_signal_trades
from datetime import date, timedelta
from numpy.lib.stride_tricks import as_strided
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt1
from scipy.stats import norm
import pandas as pd
import numpy as np
from  pathlib import Path
from os import path
import shutil
import os
import pdb

s=0
k1=pd.read_pickle('/home/sahil/Downloads/AARTIIND_intraday.pkl')
k1['Date']=k1.date.apply(lambda x:x.date())

k1['ahead_ret'] = ((k1.Close.shift(-1)-k1.Close)/k1.Close)*100
k1['signal'] = 0
k1.loc[k1.rsi5>.9,'signal']=-1
k1.loc[k1.rsi5<.1,'signal']=1

k3 = k1.iloc[0:100000]

sl=-1
tp=2
sday=0
sdayret=[]
s1dayret=[]
sret=[]
s1=0
s1ret=[]
l=0
c=0
for j in k3.Date.unique():
    k2 = k3[k3.Date==j]
    l=0
    sday=0
    s1day=0
    sstoped_out=0
    s1stoped_out=0
    
    # k4=k2.reset_index()
    c=c+1
       
    sdayret.append(extract_signal_trades(k2.drop('level_0',1).reset_index()))
    

# print(s)
print(sum(sdayret))
# print(sum(s1dayret))
sdayret=np.array(sdayret)
# s1dayret=np.array(s1dayret)
print("sharpe: ",sdayret.mean()/sdayret.std())
# print(s1dayret.mean()/s1dayret.st

s=1000
s1=[]
for i in [random.choice(sdayret) for _ in range(3000)]:# Sampling with replacement
  s=s*(1+2*i/100)# 2 is the leverage multiplier
  s1.append(s)
print(s)
s1=pd.Series(s1)
Roll_Max = s1.cummax()
Daily_Drawdown = s1/Roll_Max - 1.0
Max_Daily_Drawdown = Daily_Drawdown.cummin()
print("Drawdown Percentage from Monte Carlo simulation: ",Max_Daily_Drawdown.iloc[-1]*100)
