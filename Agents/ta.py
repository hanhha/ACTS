#!/usr/bin/env python3

import talib
from talib import abstract
import pandas as pd
from copy import deepcopy

CandleSticksPatternList = talib.get_function_groups()['Pattern Recognition']

def pandas_convert (dictdata):
	return pd.DataFrame (dictdata)

def scale_up (data, interest):
	sample = data[interest].max()
	if sample < 0.000001:
		mul = 1000000
	elif sample < 0.00001:
		mul = 100000
	elif sample < 0.0001:
		mul = 10000
	elif sample < 0.001:
		mul = 1000
	elif sample < 0.01:
		mul = 100
	elif sample < 0.01:
		mul = 10
	else:
		mul = 1
	_data = data.copy(True)
	_data[interest] = data[interest] * mul
	return _data, mul
	
def PVT (datalist, price, pre_pvt = 0):
	pvt = list ()
	for idx, data in enumerate(datalist):
		if idx > 0:
			_pre_price = datalist[idx - 1][price]
			_pre_pvt   = pvt [idx - 1]
		else:
			_pre_price = data ['O']
			_pre_pvt    = pre_pvt
		price_change = (data[price] - _pre_price) / _pre_price
		_pvt = _pre_pvt + price_change * data ['V']
		pvt.append (_pvt)

	return pvt.copy ()

def MA (data, period, interest, ma_type):
	ret = abstract.MA (data, timeperiod = period, price = interest, matype = ma_type)
	return ret

def sMA (data, period, interest, ma_type):
	_data, mul = scale_up (data, interest)
	return MA (_data, period, interest, ma_type) / mul
	
def SD (data, period, interest, ma_type):
	ret = abstract.STDDEV (data, timeperiod = period, price = interest, matype = ma_type)
	return ret
	
def sSD (data, period, interest, ma_type):
	_data, mul = scale_up (data, interest)
	return SD (_data, period, interest, ma_type) / mul

def pattern_recognize (data, op, cp, hp, lp):
	df = pd.DataFrame (data)
	inputs = {
			'open': df[op].values,
			'close': df[cp].values,
			'high': df[hp].values,
			'low': df[lp].values,
			}

	ret_list = list()
	for pt in CandleSticksPatternList:
		func = abstract.Function(pt)
		ret_list.append({'name':pt, 'marks': func (inputs)})

	return list(filter(lambda x: x['marks'][-1] != 0, ret_list))

def candle_indicator (data, pre_data):
	c_body     = (data['C'] + data['O'])/2
	c_volatile = (data['H'] + data['L'])/2
	body       = (data['C'] - data['O'])
	volatile   = data['H'] - data['L']

	pre_body       = (pre_data['C'] - pre_data['O'])
	pre_volatile   = pre_data['H'] - pre_data['L']

	if volatile > 0:
		weight     = abs(body)/volatile if volatile != 0 else 1
		body_changed   = abs(body) / abs(pre_body) if pre_body != 0 else 1

		distance   = (c_body - c_volatile)/(data['H'] - c_volatile) if data['H'] > c_volatile else 0

		if (pre_volatile < volatile) and (weight < abs(pre_body)/volatile): # epsilon to the trend
			return None 
		#if weight > 0.6: #reinforce trend
		#	if body_changed > 0.4:
		#		return True if (pre_body < 0) and (body > 0) else False if (pre_body > 0) and (body < 0) else None
		#	else:
		#		return None
		#elif weight < 0.08: # too small 
		#	return None 
		elif weight < 0.08: # too small 
			return None 
		if distance > 0.4:
			return True if (body > 0) else False if (body < 0) and (pre_body > 0) else None #(False if (body_changed > 0.4) else None) 
		if distance < -0.4:
			return False if (body < 0) else None
	else:
		return None

def find_optima (datalist, lastest_noo = 2):
	result_list = {'peak':[], 'canyon':[]}
	idx = len(datalist)
	nop, noc = 0, 0
	cur, mid, nxt = None, None, None

	while ((noc < lastest_noo) or (nop < lastest_noo)) and (idx > 0):
		idx -= 1

		nxt = mid
		mid = cur
		cur = datalist[idx]

		if (nxt is not None) and (mid is not None):
			if (mid >= cur) and (mid > nxt):
				result_list['peak'].append (mid)
				nop += 1

			elif (mid < cur) and (mid <= nxt):
				result_list['canyon'].append (mid)
				noc += 1

	return result_list
