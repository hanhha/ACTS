#!/usr/bin/env python3

import exchange as exch
import misc_utils as misc

def process_order_params (market, price, qty, for_sell = True):
	fee = 0.0025

	_price = misc.norm(price)
	_qty   = misc.norm(qty)

	price_avail, ticker = exch.get_ticker (market)

	if _price == 'last':
		_price = ticker ['Last'] if price_avail else None
	
	if for_sell:
		balance_avail, balance = exch.get_balance (market.split('-')[1])
	else:
		balance_avail, balance = exch.get_balance (market.split('-')[0])

	if _qty == 'all':
		if for_sell:
			_qty = balance ['Available'] if balance_avail else None
		else:
			 
			_qty = (balance ['Available'] / (1 + fee)) / _price if _price is not None else None 
	
	return _price, _qty

def sell (inpQ, outQ, params, Stop):
	market, price, qty = params
	assert (type(price) is str or type(price) is int or type(price) is float)
	assert (type(qty) is str or type(qty) is int or type(qty) is float)
	price = float(price) if type(price) is int or type(price) is float else price
	qty = float(qty) if type(qty) is int or type(qty) is float else qty
	
	while not Stop.is_set():
		if not inpQ.empty ():
			tmp = inpQ.get (block = False)
			sell_en = True if (type(tmp) is tuple and tmp[0] is True) or (tmp is True) else False
			price, qty = process_order_params (market, price, qty, for_sell = True)
			if sell_en and (price is not None) and (qty is not None):
				#print ('Actually sell {qty} {mar} at {pri}'.format (qty = qty, mar = market, pri = price))
				order_res, msg = exch.sell_limit (market, qty, price)
				result = (True, msg['uuid']) if order_res else (False, msg)
				misc.fill_outQ (outQ, result)
	
			else:
				misc.fill_outQ (outQ, (False, 'Can not get valid price or avaiable coins. Please check your trading script or exchanges\'s API'))

			inpQ.task_done ()

def buy (inpQ, outQ, params, Stop):
	market, price, qty = params
	assert (type(price) is str or type(price) is int or type(price) is float)
	assert (type(qty) is str or type(qty) is int or type(qty) is float)
	price = float(price) if type(price) is int or type(price) is float else price
	qty = float(qty) if type(qty) is int or type(qty) is float else qty

	while not Stop.is_set():
		if not inpQ.empty ():
			tmp = inpQ.get (block = False)
			buy_en = True if (type(tmp) is tuple and tmp[0] is True) or (tmp is True) else False
			price, qty = process_order_params (market, price, qty, for_sell = False)
	
			if sell_in and (price is not None) and (qty is not None):
				order_res, msg = exch.buy_limit (market, qty, price)
				result = (True, msg['uuid']) if order_res else (False, msg)
				misc.fill_outQ (outQ, result)
	
			else:
				misc.fill_outQ (outQ, (False, 'Can not get price or avaiable coins. Please check trading script or exchange\'s API'))

			inpQ.task_done ()

def cancel (inpQ, outQ, params, Stop):
	#TODO: cancel
	pass
