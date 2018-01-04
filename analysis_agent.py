#!/usr/bin/env python3

import misc_utils as misc
import re
#TODO: analysis_agent

def get_base_volumes (all_24hsum):
	base_volumes = dict()
	for mar in all_24hsum:
		base = mar ['MarketName'].split ('-')[0]
		if base in base_volumes.keys():
			base_volumes [base] += mar ['BaseVolume']
		else:
			base_volumes [base] = mar ['BaseVolume']
	return base_volumes

def price_compare (price, cmp_cond, pivot):
	assert (type(cmp_cond) is str)
	_cmp_cond = misc.norm (cmd_cond)
	_pivot = misc.norm (pivot)
	if type(_pivot) is str:
		percent = re.compile ('(\d+)%')
		_pivot = price * int(percent.match (_pivot)[1]) / 100.0 if percent.match (_pivot) else None
	if _pivot == None:
		print ('Invalid parameter {p}'.format (p = pivot))
	else:
		if cmp_cond == 'ge':
			return price >= _pivot
		elif cmp_cond == 'g':
			return price > _pivot
		elif cmp_cond == 'e':
			return price == _pivot
		elif cmp_cond == 'l':
			return price < _pivot
		elif cmp_cond == 'le':
			return price <= _pivot
		else:
			print ('Invalid comparison {c}'.format(c = cmp_cond))
			return False

def process_market_data (mdata):
	pass

def pcmp (inpQ, outQ, params, Stop):
	while not Stop.is_set():
		if not inpQ.empty ():
			pass
			inpQ.task_done ()


