#!/usr/bin/env python3
import time 
from functools import reduce

def eand (inpQ, outQ, params, Stop):
    assert (type(inpQ) is list)
    while not Stop.is_set():
        if not reduce(lambda x, y: x.empty() or y.empty(), inpQ):
            ans = reduce (lambda x, y: x.get(block = False) and y.get(block = False))
            for q in outQ:
                q.put (ans, block = True)
            #print ('eand takes places ' + str(ans))
            inpQ.task_done()

def eor (inpQ, outQ, params, Stop):
    assert (type(inpQ) is list)
    while not Stop.is_set():
        if not reduce(lambda x, y: x.empty() or y.empty(), inpQ):
            ans = reduce (lambda x, y: x.get(block = False) or y.get(block = False))
            for q in outQ:
                q.put (ans, block = True)
            #print ('eor takes places ' + str(ans))
            inpQ.task_done()

def enot (inpQ, outQ, params, Stop):
    while not Stop.is_set():
        if not inpQ.empty():
            ans = not inpQ.get (block = False) 
            for q in outQ:
                q.put (ans, block = True)
            #print ('enot takes places ' + str(ans))
            inpQ.task_done()

def egen (inpQ, outQ, params, Stop):
    delay = params
    while not Stop.is_set():
        for q in outQ:
            q.put (True, block = True)
        Stop.wait (delay)
