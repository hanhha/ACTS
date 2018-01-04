#!/usr/bin/env python3

import exchange as exch
import misc_utils as misc

def moni (inpQ, outQ, params, Stop):
    market = params [0]
    interval = params [1]
    while not Stop.is_set():
        if not inpQ.empty():
            tmp = inpQ.get (block = False)
            res, tick = exch.get_candle_ticks (market, interval, True)
		result = (res, tick[0]) if type(tick) is list else (res, tick)
		misc.fill_outQ (outQ, result)
            if res is False:
                print ('Can not get data from exchange\'s server')
            inpQ.task_done ()
