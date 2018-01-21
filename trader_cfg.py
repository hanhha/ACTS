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

parser.add_argument ('-v', '--verbose', type = int, default = 2, help = 'Select verbose mode, there are 3 modes similar to Unix permissions')
parser.add_argument ('-n', '--no_curses', action = 'store_true', default = False, help = 'Not using curses to render UI')
parser.add_argument ('-s', '--save', action = 'store_true', default = False, help = 'Save predictions and transactions to JSON files')

cmd_args = parser.parse_args ()
