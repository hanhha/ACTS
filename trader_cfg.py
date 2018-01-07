from seeker   	  import Seeker 

gain_loss_rules   = {'i_am_lucky':False, 'goal': 0.1, 'loss': 0.05, 'buy': 'all', 'sell': 'all'}
market_attributes = {'fee': 0.0025}
monitor_conf      = {'interval': 300, 'market': 'BTC-ADA'}

seeker = Seeker  (None, {})

debug_cfg       = {'trial'  : True, 'sim_period' : 100, 'initial_capital' : 100}
strategy_agents = {'seeker' : seeker} 

configuration = {**debug_cfg, **gain_loss_rules, **market_attributes, **monitor_conf}
