#!/usr/bin/env python3
from time import time
from Agents           import misc_utils as misc
from Agents.monitor   import Monitor as Mon
from Agents.evaluator import (ProfitEvaluator, PredictEvaluator) 
from Agents.strategy  import Strategy
from Agents.performer import Performer as Perf
from Agents.risk_mgnt import RiskMgnt as Risk

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
		if not self._params ['trial']:
			self.monitor.start ()
		else:
			self.monitor.start_sim ()

	def idle (self):
		if not self._params ['trial']:
			try:
				while True:
					time.sleep (1)
			except	(KeyboardInterrupt, SystemExit): 
				print ("Interrupt received. Stoping auto trading system ...")
			self.monitor.stop ()	

if __name__ == "__main__":
	trader = Trader (source = None, params = cfg.configuration, agent_params = cfg.strategy_agents) 
	print ('\n' + 'Welcome. I can help you to monitor and trade crypto coins. But it would be better if under supervisor...')
	if cfg.configuration ['trial']:
		print ('\n' + 'Running simulation for {mar} market.'.format (mar = cfg.configuration ['market']))  
	else:
		print ('Please be kindly notice that I can simulate your trading based on your strategy...')
		print ('Make sure that you are running on trial mode by enable it in trader_cfg.py file if you are unsure about what you are doing...')
		print ('You can stop auto trading system whenever you decide by pressing Ctrl-C (or Ctrl-Break on Windows) ...')
		ans = input ('If you answer \'yes\', real trading with your real money will be performed. Do you really want to run on real mode?')
		if ans == 'yes':
			print ('\n' + 'Running auto trader for {mar} market.'.format (mar = cfg.configuration ['market']))
		else:
			print ('Smart choice right now.')
			quit ()

	trader.start ()
	trader.idle  ()
	
	print ('\n' + 'Finish.')

	trader.predict_eva.print_all (0)
	trader.profit_eva.print_all ()

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
