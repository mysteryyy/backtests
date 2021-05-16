import unittest
import pandas as pd
import numpy as np
import slintraday
from slintraday import extract_signal_trades,simulate_trade
class TestTrades(unittest.TestCase):
    
    pr = pd.DataFrame(columns=["open","high","low","close","signal",],data=np.ones((20,5)))
    
    def test_sl_short(self):
        pr=self.pr
        pr['signal']=0
        pr.loc[10,'signal']=-1
        pr.loc[12,'high']=1.05
        pr.loc[13,'low']=0.97
        pr.loc[15,'close']=1.012

        self.assertEqual(extract_signal_trades(pr), -1, "Should be -1")

    def test_tp_short(self):
        pr=self.pr
        pr['signal']=0
        pr.loc[10,'signal']=-1
        pr.loc[12,'high']=1.005
        pr.loc[13,'low']=0.97
        pr.loc[15,'close']=1.012

        self.assertEqual(extract_signal_trades(pr), +2, "Should be +2")
        
    def test_sl_long(self):
        pr=self.pr
        pr['signal']=0
        pr.loc[10,'signal']=+1
        pr.loc[12,'high']=1.005
        pr.loc[13,'low']=0.97
        pr.loc[15,'close']=1.012
        pr.loc[15,'signal']=-1

        self.assertEqual(extract_signal_trades(pr), -1, "Should be -1")
     

    def test_tp_long(self):
        pr=self.pr
        pr['signal']=0
        pr.loc[10,'signal']=+1
        pr.loc[12,'high']=1.05
        pr.loc[13,'low']=0.995
        pr.loc[15,'close']=1.012
        pr.loc[15,'signal']=-1

        self.assertEqual(extract_signal_trades(pr), +2, "Should be +2")
     

    def test_long_sigend(self): # test exiting before end of the day
        pr=self.pr
        pr['signal']=0
        pr.loc[10,'signal']=+1
        pr.loc[12,'high']=1.01
        pr.loc[13,'low']=0.995
        pr.loc[15,'close']=1.012
        pr.loc[15,'signal']=-1
        

        self.assertEqual(round(extract_signal_trades(pr),1), +1.2, "Should be 1.2")
     

    def test_long_eod(self): # test exiting before end of the day
        pr=self.pr
        pr['signal']=0
        pr.loc[10,'signal']=+1
        pr.loc[12,'high']=1.01
        pr.loc[13,'low']=0.995
        pr.loc[15,'close']=1.012
        pr.loc[15,'signal']=1
        
        pr.loc[len(pr)-1,'close']=1.015
        pr.loc[len(pr)-1,'signal']=-1
        

        self.assertEqual(round(extract_signal_trades(pr),1), +1.5, "Should be 1.5")
     




if __name__=='__main__':
   unittest.main()
