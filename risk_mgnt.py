#!/usr/bin/env python3
import misc_utils as misc

class RiskMgnt (misc.BPA):
	def __init__ (self, source, params):
		misc.BPA.__init__ (self, source = source, params = params)
		if len(params) > 0:
			self.setParams (params)
		self._gprice        = 0
		self._bqty          = 0
		self._enable        = False

	def setParams (self, params):
		misc.BPA.setParams (self, params)
		self._spmul         = (1 - self._params ['fee'])
		self._accepted_loss = self._params ['loss']

	def check_risk (self, ppu):
		return self._enable and ((ppu * self._bqty) <= (self._gprice * (1 - self._accepted_loss)))

	def set_bought_price (self, price, commission, qty):
		print ('Keep track {p} - {q}'.format (p = price, q = qty))
		self._bqty   = qty
		self._gprice = price + commission	
		self._enable = True

	def done (self):
		self._enable = False

	def CallBack (self, data):
		if data[0] == 'buy':
			self.set_bought_price (data[2]['price'], data[2]['fee'], data[2]['qty'])
		elif data[0] == 'sell':
			self.done ()
