#!/usr/bin/env python3
import time 

def eand (inpQ, outQ, params, Stop):
    assert (type(inpQ) is list)
    while not Stop.is_set():
        if not reduce(lambda x, y: x.empty() or y.empty(), inpQ):
            ans = reduce (lambda x, y: x.get(block = False) and y.get(block = False))
            for q in outQ:
                q.put (ans, block = True)
            #TODO: eand
            print ('eand takes places ' + str(ans))
            inpQ.task_done()

def eor (inpQ, outQ, params, Stop):
    assert (type(inpQ) is list)
    while not Stop.is_set():
        if not reduce(lambda x, y: x.empty() or y.empty(), inpQ):
            ans = reduce (lambda x, y: x.get(block = False) or y.get(block = False))
            for q in outQ:
                q.put (ans, block = True)
            #TODO: eor
            print ('eor takes places ' + str(ans))
            inpQ.task_done()

def enot (inpQ, outQ, params, Stop):
    while not Stop.is_set():
        if not inpQ.empty():
            ans = not inpQ.get (block = False) 
            for q in outQ:
                q.put (ans, block = True)
            #TODO: enot
            print ('enot takes places ' + str(ans))
            inpQ.task_done()

def egen (inpQ, outQ, params, Stop):
    delay = params
    while not Stop.is_set():
        for q in outQ:
            q.put (True, block = True)
        #TODO: egen
        print ('egen takes place')
        time.sleep (delay)
