#!/usr/bin/env python3

from functools import reduce
import misc_utils as misc
from monitor      import Monitor     as Mon
from evaluator    import ProfitEvaluator, PredictEvaluator 
from strategy     import Strategy
from performer    import Performer   as Perf
from risk_mgnt    import RiskMgnt    as Risk

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
		if not cfg.debug_cfg ['trial']:
			self.monitor.start ()
		else:
			self.monitor.start_sim ()

	def idle (self):
		if not cfg.debug_cfg ['trial']:
			try:
				while True:
					sleep (1)
			except KeyboardInterrupt:
				print ('User interrupted.')

			self.monitor.stop ()	

if __name__ == "__main__":
	trader = Trader (source = None, params = cfg.configuration, agent_params = cfg.strategy_agents) 
	trader.start ()
	trader.idle  ()
	
	profit = sum([x[-1]['diff'] for x in trader.profit_eva.archieve])
	print ('Profit: {p}'.format(p=profit))
