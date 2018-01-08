#!/usr/bin/env python3

import bittrex as exchg
import acts_config as cfg

fee = 0.0025

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

def get_order_status (uuid):
	return aAPIv1.get_order (uuid)

def process_candle (candle, params):
	""" Supported features:
	DP: delta price < 0 means RED candle, >=0 mean GREEN candle
	LP : lowest price
	HP : highest price
	CP : close price
	OP : open price
	"""
	ret_info = dict ()
	if 'DP' in params ():
		ret_info ['DP'] = candle ['C'] - candle ['O']
	if 'LP' in params ():
		ret_info ['LP'] = candle ['L']
	if 'HP' in params ():
		ret_info ['HP'] = candle ['H']
	if 'CP' in params ():
		ret_info ['CP'] = candle ['C']
	if 'OP' in params ():
		ret_info ['OP'] = candle ['O']
	return ret_info.copy ()
	
def process_order_params (market, price, qty, for_sell = True):
	global fee
	_price = misc.norm(price)
	_qty   = misc.norm(qty)

	price_avail, ticker = exch.get_ticker (market)

	if type(_price) is str:
		_price = ticker [_price] if price_avail else None
	
	if for_sell:
		balance_avail, balance = get_balance (market.split('-')[1])
	else:
		balance_avail, balance = get_balance (market.split('-')[0])

	if _qty == 'all':
		if for_sell:
			_qty = balance ['Available'] if balance_avail else None
		else:
			 
			_qty = (balance ['Available'] / (1 + exch.fee)) / _price if _price is not None else None 
	
	return _price, _qty
