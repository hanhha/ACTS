#!/usr/bin/env python3

from argparse import ArgumentParser

from time import time, sleep

from Agents           import misc_utils as misc
from Agents.monitor   import Monitor as Mon
from Agents.evaluator import (ProfitEvaluator, PredictEvaluator) 
from Agents.strategy  import Strategy
from Agents.performer import Performer as Perf
from Agents.risk_mgnt import RiskMgnt as Risk
from Agents           import user_interface as ui
from Agents.console_utils import *

import trader_visual_to_bokeh as vb
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
		self.shout ('Fetching history ...')

		if not self._params ['simulation']:
			self.monitor.start ()
		else:
			self.monitor.start_sim ()

		while self.monitor._Stop.is_set ():
			self.monitor._Stop.wait (1)

		self.shout ('History fetched ...')

	def idle (self):
		try:
			while not self.monitor._Stop.is_set():
				self.monitor._Stop.wait (1)
		except	(KeyboardInterrupt, SystemExit): 
			print ("\rInterrupt received. Stoping auto trading system ...")

		self.monitor.stop ()	

		self.predict_eva.save ('predict_{mar}.json'.format(mar = cfg.configuration['market']))
		self.profit_eva.save ('profit_{mar}.json'.format(mar = cfg.configuration['market']))

parser = ArgumentParser()
parser.add_argument ('-n', '--no_curses', action = 'store_true', default = False, help = 'Not using curses to render UI')
args = parser.parse_args ()

trader = Trader (source = None, params = cfg.configuration, agent_params = cfg.strategy_agents) 

trader.predict_eva.BindTo (vb.cvt.CallBack)

trading_ui = ui.UserInterface ("Auto Crypto Trading System")

trader.setShoutFunc            (trading_ui.printCur)
trader.profit_eva.setShoutFunc (trading_ui.printEva)
trader.monitor.setShoutFunc    (trading_ui.printCur)
trader.strategy.setShoutFunc   (trading_ui.printCur)

def main (stdscr):
	if not args.no_curses:
		trading_ui.start ()
	vb.chart.start ()

	trading_ui.printTip ("Showing time is GMT0 to match with returned data from exchange ...")
	trading_ui.printTip ("Charts shows at <hostname>:8888/analyzing ...")
	trading_ui.printTip ("Press Ctrl-C or Ctrl-Break (Windows) to stop ...")

	trader.start ()
	trader.idle  ()

	if not args.no_curses:
		trading_ui.end ()

if __name__ == "__main__":
	print ('Auto Crypto Trading System')
	print ('\n' + 'Welcome. I can help you to monitor and trade crypto coins. But it would be better if under supervisor ...')
	sleep (0.5)

	if cfg.configuration ['simulation']:
		print ('It\'s attemping to run simulation. A bunch of history data will be fetched from exchange server ...')
		sleep (0.5)
		ans = input ('Data would be huge. Answer \'yes\' to start simulation: ')
		if ans == 'yes':
			print ('\n' + 'Running simulation for {mar} market.'.format (mar = cfg.configuration ['market']))  
		else:
			print ('Perhaps later.')
			quit ()
	else:
		print ('Please be kindly notice that I can simulate your trading based on your strategy ...')
		sleep (0.5)
		print ('Make sure that you are running on trial mode by enable it in trader_cfg.py file if you are unsure about what you are doing ...')
		sleep (0.5)
		print ('You can stop auto trading system whenever you decide by pressing Ctrl-C (or Ctrl-Break on Windows) ...')
		sleep (0.5)
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

	main (0)

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

	ans = ''
	while ans != 'quit':
		ans = input ("Type \'quit\' to exit: ")
	
	exit (0)
