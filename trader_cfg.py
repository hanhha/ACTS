from argparse import ArgumentParser

import os
if os.path.isfile ('seeker_custom.py'):
	from seeker_custom   	  import Seeker
else:
	from Agents.seeker import BaseSeeker as Seeker

import user_cfg

seeker = Seeker  (None, {})
strategy_agents = {'seeker' : seeker}

configuration = {**user_cfg.debug_cfg, **user_cfg.gain_loss_rules, **user_cfg.market_attributes, **user_cfg.monitor_conf}
configuration ['trial'] = True if configuration ['simulation'] else configuration['trial']

parser = ArgumentParser()

parser.add_argument ('-v', '--verbose', type = int, default = 2, help = 'Select verbose level')
parser.add_argument ('-s', '--simple_ui', action = 'store_true', default = False, help = 'Not using curses to render UI')
parser.add_argument ('-a', '--archive', action = 'store_true', default = False, help = 'Save predictions and transactions to JSON files')
parser.add_argument ('-n', '--no_chart', action = 'store_true', default = False, help = 'Not creating charts')

cmd_args = parser.parse_args ()
