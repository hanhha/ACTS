# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 10:18:21 2018

@author: hha
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.finance import candlestick2_ohlc
from Agents import exchange as exch
from talib import abstract

res, ticks = exch.get_candle_ticks ('BTC-ETH', 'fiveMin', False)

df = pd.DataFrame (ticks)

rsi_s = abstract.RSI (df, 12, price = 'C') - 50
rsi_l = abstract.RSI (df,864, price = 'C') - 50
#rsi_avg = rsi_s - rsi_l

df_rsi_s = pd.DataFrame(rsi_s + 300).set_index(df['T'])
df_rsi_l = pd.DataFrame(rsi_l + 200).set_index(df['T'])
bdf_rsi_s = pd.DataFrame(rsi_s).set_index(df['T'])
bdf_rsi_l = pd.DataFrame(rsi_l).set_index(df['T'])
sdf_rsi = pd.DataFrame((rsi_s + rsi_l)/2.0).set_index(df['T'])
df_rsi_avg = pd.DataFrame(rsi_s + 100).set_index(df['T'])
df_rsi_avg_up = pd.DataFrame(rsi_l + 100 + 30).set_index(df['T'])
#df_rsi_avg_lo = pd.DataFrame((0 - rsi_l) - 30).set_index(df['T'])
df_rsi_avg_lo = pd.DataFrame(rsi_l + 100 - 30).set_index(df['T'])

#fig, (ax_candles, ax_rsi6, ax_rsi288, ax_rsi_avg) = plt.subplots (nrows = 4, ncols = 1)
#fig, (ax0, ax1) = plt.subplots (nrows = 2, ncols = 1)
fig, ax0 = plt.subplots ()
#candlestick2_ohlc (ax_candles, df['O'], df['H'], df['L'], df['C'], width = 0.5, colorup='g', colordown='r', alpha=1.0)
candlestick2_ohlc (ax0, df['O'] * 20000 - 500, df['H'] * 20000 - 500, df['L'] * 20000 - 500, df['C'] * 20000 - 500, width = 0.5, colorup='g', colordown='r', alpha=1.0)
df_rsi_s.plot (ax = ax0, use_index = True, legend = False)
df_rsi_l.plot (ax = ax0, use_index = True, legend = False)
df_rsi_avg.plot (ax = ax0, use_index = True, legend = False)
df_rsi_avg_up.plot (ax = ax0, use_index = True, legend = False)
df_rsi_avg_lo.plot (ax = ax0, use_index = True, legend = False)
bdf_rsi_s.plot (ax = ax0, use_index = True, legend = False)
bdf_rsi_l.plot (ax = ax0, use_index = True, legend = False)
sdf_rsi.plot (ax = ax0, use_index = True, legend = False)

ax0.axhline (y = 30 + 300, xmin = 0, xmax = 3,c='blue', linewidth=0.5, zorder = 0)
ax0.axhline (y = -30 + 300, xmin = 0, xmax = 3,c='blue', linewidth=0.5, zorder = 0)
ax0.axhline (y = 30 + 200, xmin = 0, xmax = 3,c='blue', linewidth=0.5, zorder = 0)
ax0.axhline (y = -30 + 200, xmin = 0, xmax = 3,c='blue', linewidth=0.5, zorder = 0)
#ax0.axhline (y = 30, xmin = 0, xmax = 3,c='blue', linewidth=0.5, zorder = 0)
#ax0.axhline (y = -30, xmin = 0, xmax = 3,c='blue', linewidth=0.5, zorder = 0)

fig.autofmt_xdate ()
plt.tight_layout()
