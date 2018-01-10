from seeker_custom   	  import Seeker 

gain_loss_rules   = {'i_am_lucky':False, 'goal': 0.07, 'loss': 0.03, 'buy': 'all', 'sell': 'all', 'price':'last'}
market_attributes = {'fee': 0.0025}
monitor_conf      = {'interval': 300, 'market': 'BTC-ETH'}
#monitor_conf      = {'interval': 300, 'market': 'USDT-BTC'}

seeker = Seeker  (None, {})

debug_cfg       = {'trial'  : True, 'sim_period' : 288, 'initial_capital' : 100}
strategy_agents = {'seeker' : seeker} 

configuration = {**debug_cfg, **gain_loss_rules, **market_attributes, **monitor_conf}

