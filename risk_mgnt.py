#!/usr/bin/env python3
import misc_utils as misc

class RiskMgnt (misc.BPA):
	def __init__ (self, data, params):
		misc.BPA.__init__ (self, data, params)
		self._netbuy = self._params ['buy'] * (1 + self._params ['fee'])
		self._accepted_loss = sefl._params ['accepted_loss']
		self.in_risk = False

	def check_risk (self, price):
		return price <= self._netbuy * (1 - self._accepted_loss)

	def CallBack (self, data):
		in_risk = self.check_risk (data['Last'])
		self.BroadCast (in_risk) 
		
