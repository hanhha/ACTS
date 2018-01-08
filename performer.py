#!/usr/bin/env python3

import exchange as exch
import misc_utils as misc
from time import sleep

class Performer (misc.BPA):
	def __init__ (self, source, params):
		misc.BPA.__init__ (self, source = source, params = params)
		self._invest_stage = True
		self._capital = None
		self._avail_qty = 0 

	def process_order_params (self, data, price, qty, for_sell = False):
		_price = misc.norm(price)
		_qty   = misc.norm(qty)

		if type(_price) is str:
			_price = data [_price]
		
		if _qty == 'all':
			if for_sell:
				_qty = self._avail_qty 
			else:
				capital = self._capital if self._capital is not None else self._params['initial_capital']
				_qty = (capital / (1 + exch.fee)) / _price 
		
		return _price, _qty
		
	@staticmethod
	def buy (market, price, qty):
		_price, _qty = exch.process_order_params (market, price, qty, for_sell=False)
		if (_price is not None) and (_qty is not None):
			order_res, msg = exch.buy_limit (market, _qty, _price)
			result = (True, msg['uuid']) if order_res else (False, msg)
		return result

	@staticmethod
	def sell (market, price, qty):
		_price, _qty = exch.process_order_params (market, price, qty, for_sell=True)
		if (_price is not None) and (_qty is not None):
			order_res, msg = exch.sell_limit (market, _qty, _price)
			result = (True, msg['uuid']) if order_res else (False, msg)
		return result

	@staticmethod
	def wait (uuid):
		ret_dat = dict ()
		while True:
			res, order = exch.get_order (uuid)	
			if res and not order['IsOpen']:
				ret_data ['price'] = order ['Price']
				ret_data ['fee']   = order ['CommissionPaid'] 
				ret_data ['uuid']  = uuid
				ret_data ['qty']   = order ['Quantity']
				break
			sleep (1)
		return ret_dat

	def invest (self, params):
		qty    = params ['amount']
		price  = params ['price']
		tag    = params ['tag']
		mar    = self._params ['market']
		if self._params['trial']:
			p, q = self.process_order_params ({self._params['price']:params[self._params['price']]}, price, qty, False)
			if q > 0:
				ic = self._capital if self._capital is not None else self._params['initial_capital']
				self._capital = ic - p*q * (1+self._params['fee']) 
				self._avail_qty = self._avail_qty + q
				self.BroadCast (('buy', 0, {'price': q*p,
								'qty'  : q,
								'fee'  : p*q*self._params['fee'],
								'uuid' : '12345'}))	
			else:
				print ('Not enough base currency')
				
		else:
			status = self.buy (mar, price, qty)
			if status[0]:
				order_info = wait (status[1])
				self.BroadCast (('buy', tag, order_info)) 			
			else:
				print ('Buy order was not placed succesfully.')

	def harvest (self, params):
		qty    = params ['amount']
		price  = params ['price']
		mar    = self._params ['market']
		if self._params['trial']:
			p,q = self.process_order_params ({self._params['price']:params[self._params['price']]}, price, qty, True)		
			ic = self._capital if self._capital is not None else self._params['initial_capital']
			self._capital = ic + p*q * (1-self._params['fee']) 
			self._avail_qty = self._avail_qty - q
			self.BroadCast (('sell', {'price': q*p,
						  'qty'  : q,
						  'fee'  : p*q*self._params['fee'],
						  'uuid' : '12345'}))	
		else:
			status = self.sell (mar, price, qty)
			if status[0]:
				order_info = wait (status[1])
				self.BroadCast (('sell', order_info)) 			
			else:
				print ('Sell order was not placed succesfully.')

	def CallBack (self, data):
		if data['act'] [0] == 'buy':
			self.invest ({'amount': self._params ['buy'],
				      'price' : 'last',
				      'last'  : data ['Last'],
				      'tag'   : data ['act'][1]})	
		elif data['act'] [0] == 'sell':
			self.harvest ({'amount': self._params ['sell'],
				      'last'   : data ['Last'],
				      'price'  : 'last'})	
