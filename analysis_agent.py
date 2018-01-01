#!/usr/bin/env python3

#TODO: analysis_agent

def pcmp (inpQ, outQ, params, Stop):
    while not Stop.is_set():
        if not inpQ.empty():
            #TODO: moni
            tmp = inpQ.get (block = False)
            for q in outQ:
                q.put (market, block = True)
            print ('moni takes place')
            inpQ.task_done ()





