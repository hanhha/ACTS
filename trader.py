#!/usr/bin/env python3
from time import time, sleep

from Agents           import misc_utils as misc
from Agents.monitor   import Monitor as Mon
from Agents.evaluator import (ProfitEvaluator, PredictEvaluator) 
from Agents.strategy  import Strategy
from Agents.performer import Performer as Perf
from Agents.risk_mgnt import RiskMgnt as Risk

from Agents.console_utils import *

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

	def idle (self):
		try:
			while True:
				sleep (1)
		except	(KeyboardInterrupt, SystemExit): 
			print ("Interrupt received. Stoping auto trading system ...")

		self.monitor.stop ()	

		self.predict_eva.save ('predict_{mar}.json'.format(mar = cfg.configuration['market']))
		self.profit_eva.save ('profit_{mar}.json'.format(mar = cfg.configuration['market']))

if __name__ == "__main__":

	trader = Trader (source = None, params = cfg.configuration, agent_params = cfg.strategy_agents) 
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
	clearscreen ()
	pprint ("Press Ctrl-C or Ctrl-Break (Windows) to stop ...\n", pos = 'home')
	trader.idle  ()
	
	print ('\n' + 'Finish.')

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
	print ('\n' + 'Reports')
	print ('----------------------------------------------------')
	print ('Num of investment cycles     | {0:<20}'.format (len(profit_data)))
	print ('Gains                        | {0:<20}'.format(gains))
	print ('Losses                       | {0:<20}'.format(losses))
	print ('Unchanges                    | {0:<20}'.format(unchanges))
	print ('----------------------------------------------------')
	print ('Profit                       | {0:<20}'.format(profit))

	from bokeh.server.server import Server
	from bokeh.application import Application
	from bokeh.application.handlers.function import FunctionHandler

	def make_document (doc):
		fig = trader.predict_eva.visualize()
		doc.add_root(fig)
		doc.title = "Auto crypto trading system for {mar}".format(mar = cfg.configuration['market'])

	app = {'/': Application(FunctionHandler(make_document))}
	
	server = Server(app, port = 8888, allow_websocket_origin=['localhost:8888','enco.hopto.org:8888'])
	server.run_until_shutdown ()

