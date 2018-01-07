#!/usr/bin/env python3
import talib
import misc_utils as misc
import exchange as exch

class Seeker (misc.BPA):
	def __init__ (self, source, params):
		misc.BPA.__init__ (self, source = source, params = params)
		self.archieve = list ()	
		if len(params) > 0:
			self.setParams (params)
		self._investment = 0
		self._qty_bought = 0
		self.studies = dict ()
		self.prediction = dict ()

	def setParams (self, params):
		misc.BPA.setParams (self, params)
		self._goal = self._params ['goal']
		self._fee  = self._params ['fee']

	def check_goal_achieved (self, price):
		gprice = price * (1 - self._fee)
		return (gprice * self._qty_bought) > (self._investment*(1 + self._goal))  

	def store (self, data):
		self.archieve.append (data)
		self.prediction = dict ()
	
	def predict (self, factor, data):
		if len(self.archieve) > 0 and data ['T'] != self.archieve [-1]['T']:
			self.store (data)
		
		return self.call_predict (factor, data) if factor not in self.prediction.keys() else self.prediction [factor]

	def call_predict (self, factor, data):
		if factor == 'hitgoal':
			return self.check_goal_achieved (data['O'] if data['C'] > data['O'] else data['C'])
		if factor == 'trend':
			return self.predict_trend (data)
		if factor == 'profitable':
			return self.predict_profitable (data)
		if factor == 'harvestable':
			return self.predict_harvestable (data)

	def predict_trend (self, data):
		#TODO
		return True

	def predict_profitable (self, data):
		#TODO
		return True

	def predict_harvestable (self, data):
		#TODO
		return True

	def CallBack (self, data):
		if data[0] == 'buy':
			self._investment = data[2]['price'] + data[2]['fee']
			self._qty_bought = data[2]['qty']
