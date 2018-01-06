#!/usr/bin/env python3
import misc_utils as misc

class ProfitMaker (misc.BPA):
	def __init__ (self, data, params):
		misc.BPA.__init__ (self, data, params)
		self._netbuy = self._params ['buy'] * (1 + self._params ['fee'])
		self._goal = self._params ['goal']
		self._fee  = self._params ['fee']
		self._studies = dict ()

	def goal_achieve (self, price):
		net_price = price * (1 - self._fee)
		return net_price >= self._netbuy * (1 + self._goal)  

	def predict_peak (self):
		pass 

	def CallBack (self, data):
		in_goal = self.goal_achieve (data['Last'])

