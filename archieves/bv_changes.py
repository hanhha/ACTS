#!/usr/bin/env python3

from time import sleep

import bittrex as bt
import analysis_agent as ag

import matplotlib.pyplot as plt

pAPIv2 = bt.PublicAPI (bt.API_V2_0)
pAPIv1 = bt.PublicAPI (bt.API_V1_1)

dataset = {'BTC': list(), 'ETH': list(), 'USDT': list()}
all_bv_hist = {'BTC': dict(), 'ETH': dict(), 'USDT': dict()}

timeframe = 'oneMin'

res, all_markets = pAPIv1.get_markets () 
for market in all_markets:
    mar = market ['MarketName']
    base = market ['BaseCurrency']
    if base == 'BTC':
        print (mar)
        res, tick_hist = pAPIv2.get_ticks (mar, timeframe)
        print (len(tick_hist))
        for tick in tick_hist:
            timestamp = tick ['T']
            if timestamp in all_bv_hist [base].keys ():
                all_bv_hist [base] [timestamp] += tick ['BV']
            else:
                all_bv_hist [base] [timestamp] = tick ['BV']

print (all_bv_hist['BTC'])
print (all_bv_hist['ETH'])
print (all_bv_hist['USDT'])
