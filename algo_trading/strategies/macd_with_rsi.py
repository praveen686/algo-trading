import yfinance as yf
import backtrader as bt
import datetime

class MacdWithRsi(bt.Strategy):
    params = (
        ('macd_slow_period', 12),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
