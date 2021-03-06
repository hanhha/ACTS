#!/usr/bin/env python3

from time import time, sleep

from Agents.evaluator     import PredictEvaluator 
from Agents.tanalyzer     import TAnalyzer
from Agents.monitor       import Monitor        as Mon
from Agents		            import misc_utils     as misc
from Agents               import user_interface as ui

from Agents               import acts_config    as s_cfg
import trader_cfg                               as cfg

if s_cfg.bokeh_en:
	import trader_visual_to_bokeh             as vb

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
			self.shout ("Interrupt received. Stoping analyzer ...")

		self.monitor.stop ()	

		if cfg.cmd_args.archive:
			self.predict_eva.save ('predict_{mar}.json'.format(mar = cfg.configuration['market']))

analyzer = Analyzer (source = None, params = cfg.configuration, agent_params = cfg.strategy_agents) 

if s_cfg.bokeh_en:
	analyzer.predict_eva.BindTo (vb.cvt.CallBack)

trading_ui = ui
trading_ui.UI.verbose = cfg.cmd_args.verbose

analyzer.setShoutFunc          (trading_ui.printCur)
analyzer.monitor.setShoutFunc  (trading_ui.printCur)
analyzer.analyzer.setShoutFunc (trading_ui.printCur)

def main (stdscr):
	if not cfg.cmd_args.simple_ui:
		trading_ui.UI.start ()
		trading_ui.UI.print_on_window ('summary', 'Running on analyzing mode ...\n')

	trading_ui.printTip ("Showing time is GMT0 to match with returned data from exchange ...")
	trading_ui.printTip ("Charts shows at <hostname>:8888/analyzing ...")
	trading_ui.printTip ("Press Ctrl-C or Ctrl-Break (Windows) to stop ...")

	analyzer.start ()
	analyzer.idle  ()

	if not cfg.cmd_args.simple_ui:
		trading_ui.printCur ("Press any key to exit this UI ...")
		c = trading_ui.UI.getch (True)
		trading_ui.UI.end ()

if __name__ == "__main__":
	if s_cfg.bokeh_en:
		print (s_cfg.config.bokeh.allowed_origin)	
		list_origins = list(filter(lambda s: s != '', list(map (lambda x:x.strip(), [o for o in s_cfg.config.bokeh.allowed_origins.split (',')]))))

		vb.chart.allow_websocket_origin = list_origins
		vb.chart.port                   = int(s_cfg.config.bokeh.port)
		vb.chart.start ()

	main (0)

	print ('\n' + 'Finish.')

	exit (0)
