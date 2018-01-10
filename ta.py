#!/usr/bin/env python3

from talib import abstract
import pandas as pd

def pandas_convert (dictdata):
	return pd.DataFrame (dictdata)

def scale_up (data, interest):
	sample = data[interest] .max()
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
			_pre_price = data_list[idx - 1][price]
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
