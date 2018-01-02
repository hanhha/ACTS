#!/usr/bin/env python3

import time 
from functools import reduce

def eand (inpQ, outQ, params, Stop):
	assert (type(inpQ) is list)
	while not Stop.is_set():
		nq = 0
		for iq in inpQ:
			if not iq.empty():
				nq += 1
		if nq == len(inpQ):
			for q in outQ:
				q.put (True, block = True)
			for iq in inpQ:
				tmp = inpQ.get (block = False)
				inpQ.task_done ()

def eor (inpQ, outQ, params, Stop):
	assert (type(inpQ) is list)
	while not Stop.is_set():
		nq = 0
		for iq in inpQ:
			if not iq.empty():
				nq += 1
		if nq > 0:
			for q in outQ:
				q.put (True, block = True)
			for iq in inpQ:
				tmp = inpQ.get (block = False)
				inpQ.task_done ()

def egen (inpQ, outQ, params, Stop):
	delay = params
	while not Stop.is_set():
		for q in outQ:
			q.put (True, block = True)
		Stop.wait (delay)
