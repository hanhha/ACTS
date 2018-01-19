#!/usr/bin/env python3

from argparse import ArgumentParser

from time import time, sleep

from Agents           import misc_utils as misc
from Agents.monitor   import Monitor as Mon
from Agents.evaluator import PredictEvaluator 
from Agents.tanalyzer import TAnalyzer
from Agents           import user_interface as ui
from Agents.console_utils import *

import analyzer_visual_to_bokeh as vb
import trader_cfg as cfg

class Analyzer (misc.BPA):
	def __init__ (self, source, params, agent_params):
		misc.BPA.__init__ (self, source, params)

		self.monitor     = Mon      (params = params)
		self.analyzer    = TAnalyzer (source = self.monitor, agents = agent_params, params = params) 
		self.predict_eva = PredictEvaluator (source = self.analyzer)

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
			print ("\rInterrupt received. Stoping analyzer ...")

		self.monitor.stop ()	

		self.predict_eva.save ('predict_{mar}.json'.format(mar = cfg.configuration['market']))

parser = ArgumentParser()
parser.add_argument ('-n', '--no_curses', action = 'store_true', default = False, help = 'Not using curses to render UI')
args = parser.parse_args ()

analyzer = Analyzer (source = None, params = cfg.configuration, agent_params = cfg.strategy_agents) 

analyzer.predict_eva.BindTo (vb.cvt.CallBack)

trading_ui = ui.UserInterface ("Crypto Market Analyzer System")

analyzer.setShoutFunc          (trading_ui.printCur)
analyzer.monitor.setShoutFunc  (trading_ui.printCur)
analyzer.analyzer.setShoutFunc (trading_ui.printCur)

def main (stdscr):
	if not args.no_curses:
		trading_ui.start ()
	vb.chart.start ()

	trading_ui.printTip ("Showing time is GMT0 to match with returned data from exchange ...")
	trading_ui.printTip ("Charts shows at <hostname>:8888/analyzing ...")
	trading_ui.printTip ("Press Ctrl-C or Ctrl-Break (Windows) to stop ...")

	analyzer.start ()
	analyzer.idle  ()

	if not args.no_curses:
		trading_ui.end ()

if __name__ == "__main__":
	main (0)

	print ('\n' + 'Finish.')

	exit (0)
