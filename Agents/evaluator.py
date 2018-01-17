from datetime import datetime as dt

from . import misc_utils as misc
from . import chart_utils as chart

import simplejson as json
from pandas import DataFrame

class Evaluator (misc.BPA):
	def __init__ (self, source):
		misc.BPA.__init__ (self, source = source)
		self.archieve = list ()  
		self.pdarchieve = DataFrame ()

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
	
	def visualize (self):
		assert "Not implemented yet.", 0

	def save (self, filename):
		try:
			with open (filename, 'w') as cf:
				json.dump (self.archieve, cf, default = misc.to_serializable)
		except IOError:
			print ("Can not save data of last session to file.")
		else:
			print ('Data of last session was saved to {fn}'.format (fn = filename))

	def load (self, filename):
		json_data = list()
		try:
			with open (filename, 'r') as cf:
				json_data = json.load (cf)
		except IOError:
			print ("Can not open data file.")
		else:
			for data in json_data:
				data['T'] = dt.strptime(data['T'],'%Y-%m-%dT%H:%M:%S')
				self.record (data)

class ProfitEvaluator (Evaluator):
	def record (self, data):
		# request data [type, timestamp, order_info]
		# store [timestamp, buy_order_uuid, sell_order_uuid, profit]
		if data[0] == 'buy':
			self.archieve.append ([data[1], data[2]['uuid']])
			self._gross_invest = data[2]['price'] + data[2]['fee']
			print ('\rBought with gross price {price}'.format (price = self._gross_invest), end = '', flush = True)
		elif data[0] == 'sell':
			gross_return = data[2]['price'] - data[2]['fee']
			d = gross_return - self._gross_invest
			profit = {'diff': d, 'percent': d / self._gross_invest}
			self.archieve[-1].extend ([data[1], data[2]['uuid'], profit])
			print ('\rBought with gross price {iprice} - Sold with gross price {hprice} - Profit {p}'.format (iprice = self._gross_invest, hprice = gross_return, p = d))
		else:
			print ('Unknown data for profit evaluation.')

class PredictEvaluator (Evaluator):
	def record (self, data):
		self.add_data (data)
		self.evaluate ()
		
		# Broadcast plotting data
		if data['act'][0] == 'buy':
			decision = True
		elif data['act'][0] == 'sell':
			decision = False
		else:
			decision = None

		plot_data = {'T': data['T'],
					 'L': data['L'],
					 'H': data['H'],
					 'C': data['C'],
					 'O': data['O'],
					 'D': decision} 

		self.BroadCast (plot_data)	
	
	def add_data (self, data):
		new_data = data.copy ()
		self.archieve.append (data.copy())

		new_data ['buy_decision'] = None
		if new_data ['act'][0] == 'buy':
			new_data ['buy_decision'] = True
		elif new_data ['act'][0] == 'sell':
			new_data ['buy_decision'] = False

		self.pdarchieve = self.pdarchieve.append (new_data, ignore_index = True)

	def visualize (self):
		fig = chart.draw_candlesticks (self.pdarchieve, 'H','C','O','L','T', name = 'CandleSticks with buy/sell decisions', decision = 'buy_decision')
		return fig

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
