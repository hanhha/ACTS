#!/usr/bin/env python3

from . import misc_utils as misc

class Evaluator (misc.BPA):
	def __init__ (self, source):
		misc.BPA.__init__ (self, source = source)
		self.archieve = list ()  

	def record (self, data):
		assert 'Not implemented yet', 0

	def CallBack (self, data):
		self.record (data)
	
	def print_all (self, idx = None):
		if idx is not None:
			print ('Monitored data at time {t}'.format (t = idx))
			print (self.archieve [idx])
		else:
			for i, entry in enumerate(self.archieve):
				print ('Monitored data at time {t}'.format (t = i))
				print (entry)
				print ('----------------')

class ProfitEvaluator (Evaluator):
	def record (self, data):
		# request data [type, timestamp, order_info]
		# store [timestamp, buy_order_uuid, sell_order_uuid, profit]
		if data[0] == 'buy':
			self.archieve.append ([data[1], data[2]['uuid']])
			self._gross_invest = data[2]['price'] + data[2]['fee']
		elif data[0] == 'sell':
			gross_return = data[2]['price'] - data[2]['fee']
			d = gross_return - self._gross_invest
			profit = {'diff': d, 'percent': d / self._gross_invest}
			self.archieve[-1].extend ([data[1], data[2]['uuid'], profit])
		else:
			print ('Unknown data for profit evaluation.')

class PredictEvaluator (Evaluator):
	def record (self, data):
		self.add_data (data)
		self.evaluate ()
	
	def add_data (self, data):
		new_data = data.copy ()
		self.archieve.append (new_data)

	def evaluate (self):
		# TODO: need to improve
		if len (self.archieve) > 2:
			ed = [a['C'] for a in self.archieve [-3:]]
			if ed[0] < ed[1] > ed[2]:
				self.archieve [-2] ['reality'] = 'peak'
			elif ed[0] > ed[1] < ed[2]:
				self.archieve [-2] ['reality'] = 'canyon'
			elif ed[0] > ed[1]:
				self.archieve [-2] ['reality'] = 'falling'
			elif ed[0] < ed[1]:
				self.archieve [-2] ['reality'] = 'rising'
			elif ed[0] == ed[1]:
				self.archieve [-2] ['reality'] = 'stable'
			else:
				print ('Not an expected case')
