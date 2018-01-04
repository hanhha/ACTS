#/usr/bin/env python3

def norm (param):
	if type(param) is str:
		return param.strip().lower()
	else:
		return param

def fill_outQ (outQ, qDat):
	for q in outQ:
		q.put (qDat, block = True)


