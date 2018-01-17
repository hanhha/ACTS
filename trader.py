#!/usr/bin/env python3
from time import time, sleep
from math import pi

from bokeh.plotting import figure
from bokeh.models.glyphs import VBar, Segment
from bokeh.models.markers import Triangle 

from Agents           import misc_utils as misc
from Agents.monitor   import Monitor as Mon
from Agents.evaluator import (ProfitEvaluator, PredictEvaluator) 
from Agents.strategy  import Strategy
from Agents.performer import Performer as Perf
from Agents.risk_mgnt import RiskMgnt as Risk

from Agents.console_utils import *
from Agents           import chart_utils as chart

import trader_cfg as cfg

class Trader (misc.BPA):
	def __init__ (self, source, params, agent_params):
		misc.BPA.__init__ (self, source, params)

		self.monitor     = Mon      (params = params)
		self.risk        = Risk (None, {})
		self.strategy    = Strategy (source = self.monitor, agents = agent_params, params = params, risk_mgnt = self.risk) 
		self.performer   = Perf     (source = self.strategy, params = params) 
		self.predict_eva = PredictEvaluator (source = self.strategy)
		self.profit_eva  = ProfitEvaluator  (source = self.performer)

		self.risk.Bind (self.performer)
		self.strategy.seeker.Bind (self.performer)

	def start (self):
		if not self._params ['simulation']:
			self.monitor.start ()
		else:
			self.monitor.start_sim ()

		while self.monitor._Stop.is_set ():
			self.monitor._Stop.wait (1)

	def idle (self):
		try:
			while not self.monitor._Stop.is_set():
				self.monitor._Stop.wait (1)
		except	(KeyboardInterrupt, SystemExit): 
			print ("\rInterrupt received. Stoping auto trading system ...")

		self.monitor.stop ()	

		self.predict_eva.save ('predict_{mar}.json'.format(mar = cfg.configuration['market']))
		self.profit_eva.save ('profit_{mar}.json'.format(mar = cfg.configuration['market']))

def get_figure ():
	p = figure(x_axis_type = 'datetime', sizing_mode = 'scale_width', plot_height = 200)
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha = 0.6

	return p

def draw_up_candles ():
	g0 = Segment (x0 = 'T', y0 = 'H', x1 = 'T', y1 = 'L', line_color = 'black')
	g1 = VBar    (x = 'T', top = 'C', bottom = 'O', width = 250000, fill_color = 'green', line_color = 'black')
	
	return (g0, g1)

def draw_down_candles ():
	g0 = Segment (x0 = 'T', y0 = 'H', x1 = 'T', y1 = 'L', line_color = 'black')
	g1 = VBar    (x = 'T', top = 'O', bottom = 'C', width = 250000, fill_color = 'red', line_color = 'black')
	
	return (g0, g1) 

def draw_stand_candles ():
	g0 = Segment (x0 = 'T', y0 = 'H', x1 = 'T', y1 = 'L', line_color = 'black')
	g1 = VBar    (x = 'T', top = 'O', bottom = 'C', width = 250000, fill_color = 'black', line_color = 'black')
	
	return (g0, g1) 

def draw_sell ():
	g0 = Triangle (x = 'T', y = 'price', size = 10, fill_color = 'red', angle = pi, fill_alpha = 0.8)

	return g0 

def draw_buy ():
	g0 = Triangle (x = 'T', y = 'price', size = 10, fill_color = 'green', angle = 0.0, fill_alpha = 0.8)

	return g0 

class DataCvt(misc.BPA):
	def CallBack (self, data):
		new_data = {'candlestick':{}}

		if data['C'] > data['O']:
			new_data['candlestick']['upstick'] = {
					 'L': data['L'],
					 'H': data['H'],
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}
		elif data['C'] < data['O']:
			new_data['candlestick']['downstick'] = {
					 'L': data['L'],
					 'H': data['H'],
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}
		else:
			new_data['candlestick']['standstick'] = {
					 'L': data['L'],
					 'H': data['H'],
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}

		if data['D'] == True:
			new_data['candlestick']['buy_decision'] = {
					 'price': data['L'],
					 'T': data['T']
				}
		elif data['D'] == False:
			new_data['candlestick']['sell_decision'] = {
					 'price': data['H'],
					 'T': data['T']
				}

		self.BroadCast (new_data)


if __name__ == "__main__":

	trader = Trader (source = None, params = cfg.configuration, agent_params = cfg.strategy_agents) 

	plotting = chart.PlottingServer (title = 'Auto Crypto Trading System for market {mar}'.format (mar = cfg.configuration['market']), port = 8888, allow_websocket_origin = ['localhost:8888','enco.hopto.org:8888'])

	cvt = DataCvt()

	plotting.add_plot ('candlestick', get_figure)

	plotting.add_glyph ('candlestick', 'upstick', draw_up_candles, {'T':[],'H':[],'L':[],'O':[],'C':[]})
	plotting.add_glyph ('candlestick', 'downstick', draw_down_candles, {'T':[],'H':[],'L':[],'O':[],'C':[]})
	plotting.add_glyph ('candlestick', 'standstick', draw_stand_candles, {'T':[],'H':[],'L':[],'O':[],'C':[]})
	plotting.add_glyph ('candlestick', 'buy_decision', draw_buy, {'T':[],'price':[]})
	plotting.add_glyph ('candlestick', 'sell_decision', draw_sell, {'T':[],'price':[]})

	trader.predict_eva.BindTo (cvt.CallBack)
	cvt.BindTo (plotting.CallBack)

	clearscreen ()

	pprint ('Auto Crypto Trading System', pos = 'home')
	pprint ('\n' + 'Welcome. I can help you to monitor and trade crypto coins. But it would be better if under supervisor ...')
	sleep (1)

	if cfg.configuration ['simulation']:
		print ('It\'s attemping to run simulation. A bunch of history data will be fetched from exchange server ...')
		sleep (1)
		ans = input ('Data would be huge. Answer \'yes\' to start simulation: ')
		if ans == 'yes':
			print ('\n' + 'Running simulation for {mar} market.'.format (mar = cfg.configuration ['market']))  
		else:
			print ('Perhaps later.')
			quit ()
	else:
		print ('Please be kindly notice that I can simulate your trading based on your strategy ...')
		sleep (1)
		print ('Make sure that you are running on trial mode by enable it in trader_cfg.py file if you are unsure about what you are doing ...')
		sleep (1)
		print ('You can stop auto trading system whenever you decide by pressing Ctrl-C (or Ctrl-Break on Windows) ...')
		sleep (1)
		if cfg.configuration ['trial']:
			ans = input ('If you answer \'yes\', trial trading with updated market data will be performed so that your wallet will be safe. Do you want to run on trial mode? ')
			if ans == 'yes':
				print ('\n' + 'Running auto trader in trial mode for {mar} market.'.format (mar = cfg.configuration ['market']))
			else:
				print ('Perhaps later.')
				quit ()
		else:
			ans = input ('If you answer \'yes\', real trading with your real money will be performed so that your wallet would be affected. Do you really want to run on real mode? ')
			if ans == 'yes':
				print ('\n' + 'Running auto trader with real money for {mar} market.'.format (mar = cfg.configuration ['market']))
			else:
				print ('Smart choice right now.')
				quit ()

	trader.start ()
	plotting.idle ()

	clearscreen ()
	pprint ("Press Ctrl-C or Ctrl-Break (Windows) to stop ...\n", pos = 'home')

	trader.idle  ()
	pprint ('\n' + 'Finish.')

	profit_data = trader.profit_eva.archieve
	if len(profit_data) > 0:
		if len(profit_data [-1]) < 4:
			del profit_data [-1]
	
	if len(profit_data) > 0:
		profit     = sum([x[-1]['diff'] for x in profit_data])
		losses     = sum([1 if x[-1]['diff'] <  0 else 0 for x in profit_data])
		gains      = sum([1 if x[-1]['diff'] >  0 else 0 for x in profit_data])
		unchanges  = sum([1 if x[-1]['diff'] == 0 else 0 for x in profit_data])
	else:
		profit     = 0
		losses     = 0
		gains      = 0
		unchanges  = 0

	pprint ('\n' + 'Reports')
	pprint ('----------------------------------------------------')
	pprint ('Num of investment cycles     | {0:<20}'.format (len(profit_data)))
	pprint ('Gains                        | {0:<20}'.format(gains))
	pprint ('Losses                       | {0:<20}'.format(losses))
	pprint ('Unchanges                    | {0:<20}'.format(unchanges))
	pprint ('----------------------------------------------------')
	pprint ('Profit                       | {0:<20}'.format(profit))

	ans = ''
	while ans != 'quit':
		ans = input ("Type \'quit\' to exit: ")
	
	plotting.stop ()
