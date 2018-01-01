#!/usr/bin/env python3

import bittrex as exchg

pAPIv1 = exchg.PublicAPI  (exchg.API_V1_1)
pAPIv2 = exchg.PublicAPI  (exchg.API_V2_0)

def moni (inpQ, outQ, params, Stop):
    market = params [0]
    interval = params [1]
    while not Stop.is_set():
        if not inpQ.empty():
            tmp = inpQ.get (block = False)
            res, tick = pAPIv2.get_ticks (market, interval, True)
            for q in outQ:
                if type(tick) is list:
                    q.put ((res, tick[0]), block = True)
                else:
                    q.put ((res, tick), block = True)
            if res is False:
                print ('Can not get data from exchange\'s server')
            inpQ.task_done ()
