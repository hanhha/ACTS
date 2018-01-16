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

