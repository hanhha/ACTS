#!/usr/bin/env python3

import bittrex as exchg
import bittrex_trade_cfg as exchg_cfg

mAPI = exchg.MarketAPI  (exchg.API_VER_1_1, exchg_cfg.API_KEY, exchg_cfg.API_SECRET) 
aAPI = exchg.AccountAPI (exchg.API_VER_1_1, exchg_cfg.API_KEY, exchg_cfg.API_SECRET) 
