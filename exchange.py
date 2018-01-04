#!/usr/bin/env python3

import bittrex as exchg
import acts_config as cfg

pAPIv1 = exchg.PublicAPI  (exchg.API_V1_1)
pAPIv2 = exchg.PublicAPI  (exchg.API_V2_0)

mAPI = exchg.MarketAPI  (exchg.API_V1_1, cfg.config['Bittrex']['API_KEY'].encode('utf-8'), cfg.config['Bittrex']['API_SECRET'].encode('utf-8')) 
aAPI = exchg.AccountAPI (exchg.API_V1_1, cfg.config['Bittrex']['API_KEY'].encode('utf-8'), cfg.config['Bittrex']['API_SECRET'].encode('utf-8')) 

def get_candle_ticks (market, interval, get_last_only = True):
	return pAPIv2.get_ticks (market, interval, get_last_only)

def get_balance (cur):
	return aAPI.get_balance (cur)

def buy_limit (market, qty, price):
	return mAPI.buy_limit (market, qty, price)

def sell_limit (market, qty, price):
	return sell_limit (market, qty, price)

def get_ticker (market):
	return pAPIv1.get_ticker (market)

