#!/usr/bin/env python3

import analysis_agent as ag
import exchange as exch

# Configuration
market = 'BTC-ADA'

stage_sell = False

AC = ag.Analysis (market, {'EMA':3, 'SMA':5, 'BOBA':{'period':5, 'avg':'SMA'})

try:
	while True:
		res, tick = exch.get_candle_ticks (market, 'oneMin', True)
		if not res:
			print ('Can not get data from exchange, please check')
		else:
			candle_data = exch.process_candle(tick, ['CP', 'DP',])
			AC.put (candle_data['CP'])
			ema3      = AC.get ('EMA')
			sma5      = AC.get ('SMA')
			bb5, sd5  = AC.get ('BOBA')
			dp           = candle_data ['DP']
			
			
			
			if not stage_sell:
				
				
			
		
except KeyboardInterrupt:
	print ('User interrupt.')
	