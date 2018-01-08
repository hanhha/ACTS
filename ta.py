#!/usr/bin/env python3

from talib import abstract
import pandas as pd

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