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
from talib import MA_Type
from Agents.misc_utils import MouseLine
from Agents import misc_utils as misc

res, ticks = exch.get_candle_ticks ('BTC-ETH', 'fiveMin', False)

df = pd.DataFrame (ticks)

rsi_s = abstract.RSI (df, 24, price = 'C') - 50
rsi_s_ma = abstract.MA (pd.DataFrame({'RSI':rsi_s}), 3, price = 'RSI', matype = MA_Type.SMA)
rsi_l = abstract.RSI (df,476, price = 'C') - 50
#rsi_avg = rsi_s - rsi_l

df_rsi_s = pd.DataFrame(rsi_s).set_index(df['T'])
#df_rsi_s = pd.DataFrame(rsi_s_ma).set_index(df['T'])
df_rsi_l = pd.DataFrame(rsi_l).set_index(df['T'])

df_rsi_avg = pd.DataFrame(rsi_s).set_index(df['T'])
#df_rsi_avg = pd.DataFrame(rsi_s_ma).set_index(df['T'])
#df_rsi= pd.DataFrame(rsi_s * (1+(rsi_l/100.0))).set_index(df['T'])
df_rsi_avg_up = pd.DataFrame((0 - rsi_l) + 35).set_index(df['T'])
df_rsi_avg_lo = pd.DataFrame((0 - rsi_l) - 35).set_index(df['T'])

fig, (ax0, ax1, ax2, ax3) = plt.subplots (nrows = 4, ncols = 1, sharex = True)

candlestick2_ohlc (ax0, df['O'], df['H'], df['L'], df['C'], width = 0.5, colorup='g', colordown='r', alpha=1.0)

df_rsi_s.plot (ax = ax1, use_index = True, legend = False)
df_rsi_l.plot (ax = ax2, use_index = True, legend = False, sharey = ax1)

df_rsi_avg.plot (ax = ax3, use_index = True, legend = False, sharey = ax1)
df_rsi_avg_up.plot (ax = ax3, use_index = True, legend = False, sharey = ax1)
df_rsi_avg_lo.plot (ax = ax3, use_index = True, legend = False, sharey = ax1)

misc.draw_hthresholds (ax1, 0, 35, -35, 'blue')
misc.draw_hthresholds (ax2, 0, 35, -35, 'blue')
misc.draw_hthresholds (ax3, 0, 35, -35, 'blue')

plt.tight_layout()
vl = MouseLine([ax0, ax1, ax2, ax3], color='red', direction = 'V')
hl0 = MouseLine([ax0], color='red', direction = 'H')
hl1 = MouseLine([ax1], color='red', direction = 'H')
hl2 = MouseLine([ax2], color='red', direction = 'H')
hl3 = MouseLine([ax3], color='red', direction = 'H')
fig.canvas.mpl_connect('motion_notify_event', vl.show_line)
fig.canvas.mpl_connect('motion_notify_event', hl0.show_line)
fig.canvas.mpl_connect('motion_notify_event', hl1.show_line)
fig.canvas.mpl_connect('motion_notify_event', hl2.show_line)
fig.canvas.mpl_connect('motion_notify_event', hl3.show_line)
plt.show ()
