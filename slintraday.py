import datetime
import random
import nolds
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
from mle import *

#pr = pd.DataFrame(columns=["open","high","low","close","signal",],data=np.ones((20,5)))
#pr['signal']=0
#pr.loc[10,'signal']=-1
#pr.loc[12,'high']=1.05
#pr.loc[13,'low']=0.97
#pr.loc[15,'close']=1.012
#print(pr)
#s=0
## Assuming stop loss of 1% and take-profit of 2%
sl=-1
tp=2
long_short='long'
stopped_out=0
def simulate_trade(pr,long_short):
    #pr['oh']=(pr.high-pr.open)/pr.open * 100
    #pr['ol']=(pr.low-pr.open)/pr.open * 100
    #pr['oc']=(pr.close-pr.close.shift(1))/pr.close.shift(1) * 100
    #pr.loc[0,'oc'] = (pr.close.loc[0]-pr.open.loc[0])/pr.open.loc[0] * 100

    print(pr)
    s=0
    for index,row in pr.iloc[0:len(pr)].iterrows():
        if(long_short=='long'): 
           if (s+row.oh>tp):
               s=tp
               break
           elif(s+row.ol<sl):
               s=sl
               break
           else:
               s=s+row.oc
        else:
           if (s-row.oh<sl):
               s=sl
               break
           elif(s-row.ol>tp):
               s=tp
               break
           else:
               s=s-row.oc

    return s
def extract_signal_trades(pr):
    
    pr['oh']=(pr.high-pr.open)/pr.open * 100
    pr['ol']=(pr.low-pr.open)/pr.open * 100
    pr['oc']=(pr.close-pr.close.shift(1))/pr.close.shift(1) * 100
    pr.loc[0,'oc'] = (pr.close.loc[0]-pr.open.loc[0])/pr.open.loc[0] * 100


    k2=pr
    # Index of the signals
    rets=0
    signal_up=k2[k2.signal==1].index.values

    signal_down=k2[k2.signal==-1].index.values
    if((len(signal_up)!=0) & (len(signal_down)!=0)):#Condition for long trade with exit within the day
      signal_up=signal_up[0]

      signal_down=signal_down[0]

      if(signal_up<signal_down):
      
        rets=simulate_trade(k2.iloc[signal_up+1:signal_down+1],'long')

      else: # Condition for short trade with exit within the day

        rets=simulate_trade(k2.iloc[signal_down+1:signal_up+1],'short')

    elif((len(signal_up)>0) & (len(signal_down)==0)):#Condition for long trade with exit at the end of the day

      signal_up=signal_up[0]
      
      rets=simulate_trade(k2.iloc[signal_up+1:],'long')

    else:# Condition for short trade with exit at the end of the day
      signal_down=signal_down[0]

      rets=simulate_trade(k2.iloc[signal_down+1:],'short')

    return rets

