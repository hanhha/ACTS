from seeker_custom   	  import Seeker 

# Customize values to fit each market
gain_loss_rules   = {'i_am_lucky':False, 'goal': 0.1, 'loss': 0.03, 'buy': 'all', 'sell': 'all', 'price':'last'}
market_attributes = {'fee': 0.0025}
monitor_conf      = {'interval': 300, 'market': 'BTC-XRP'}

seeker = Seeker  (None, {})

debug_cfg       = {'trial'  : True, 'initial_capital' : 100}
strategy_agents = {'seeker' : seeker} 
# End of customization

configuration = {**debug_cfg, **gain_loss_rules, **market_attributes, **monitor_conf}

