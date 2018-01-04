script = [
	# Monitor every 60s
	['tick', 60],
	# Low pass filter in 2 ticks
	['filter', 2],
	['generate', 1, 'clk'],
	
	# Monitor one minitue candle tick of BTC-ADA market
	# Supported: oneMin, fiveMin, thirtyMin, hour, day
	['monitor',    'clk',          'BTC-ADA',          'oneMin',   'btc_ada_tick'],

	# Compare closed price increasing 10% from my last order price 
	['compare',    'btc_ada_tick', 'cprice', 'ge',     '10%',      '10p_en'],
	# Check if closed price has just been down from maxima 
	['turnover',   'btc_ada_tick', 'maxima', 'cprice',             'peak_en'],
	# Check if closed price is above EMA with period 5
	['compare',    'btc_ada_tick', 'cprice', 'ge',     'ema', '5', 'above_ema_en'],

	# Enable to sell all ADA with last price when all above conditions are met
	['and',        '10p_en',             'peak_en', 'above_ema_en',                              'sell_ada_en']
	['confirm',    'sell_ada_en',        'Turnover, higher price, above EMA met, sell all ADA?', 'sell_ada_confirmed'],
	['sell',       'sell_ada_confirmed', 'BTC-ADA', 'price', 'all',                              'sell_success'],
	['notify',     'sell_ada_success',   'uuid',                                                  None],

	# Check if trend of closed price is fallsing 
	['trend',      'btc_ada_tick', 'cprice',  'fall',             'down_en'],
	# Check if closed price has just been up from minimum 
	['turnover',   'btc_ada_tick', 'minimum', 'cprice',           'canyon_en'],
	# Check if closed price is below EMA with period 5
	['compare',    'btc_ada_tick', 'cprice', 'le',    'ema', '5', 'below_ema_en'],

	# Enable to buy all ADA with last price when all above conditions are met
	['and',        'down_en',            'canyon_en', 'below_ema_en',                          'buy_ada_en']
	['confirm',    'buy_ada_en',         'Turnover, lower price, below EMA met, buy all ADA?', 'buy_ada_confirmed'],
	['buy',        'buy_ada_confirmed',  'BTC-ADA',   'price', 'all',                          'buy_success'],
	['notify',     'buy_ada_success',    'uuid',                                                None],

	#['notify','dat0', 'rem', 'Test output for monitor', None],
]

# cprice: closed price
# oprice: opened price
# hprice: highest price
# lprice: lowest price
# price : last price

#'BV': 99.44951468,
#'C': 5.223e-05,
#'H': 5.223e-05,
#'L': 5.067e-05,
#'O': 5.081e-05,
#'T': '2018-01-01T17:00:00',
#'V': 1933366.51921126}])
