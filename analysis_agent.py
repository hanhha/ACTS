#!/usr/bin/env python3

import misc_utils as misc
import re
import math
#TODO: analysis_agent

def get_base_volumes (all_24hsum):
	base_volumes = dict()
	for mar in all_24hsum:
		base = mar ['MarketName'].split ('-')[0]
		if base in base_volumes.keys():
			base_volumes [base] += mar ['BaseVolume']
		else:
			base_volumes [base] = mar ['BaseVolume']
	return base_volumes

def price_compare (price, cmp_cond, pivot):
	assert (type(cmp_cond) is str)
	_cmp_cond = misc.norm (cmp_cond)
	_pivot = misc.norm (pivot)
	if type(_pivot) is str:
		percent = re.compile ('(\d+)%')
		_pivot = price * int(percent.match (_pivot)[1]) / 100.0 if percent.match (_pivot) else None
	if _pivot == None:
		print ('Invalid parameter {p}'.format (p = pivot))
	else:
		if cmp_cond == 'ge':
			return price >= _pivot
		elif cmp_cond == 'g':
			return price > _pivot
		elif cmp_cond == 'e':
			return price == _pivot
		elif cmp_cond == 'l':
			return price < _pivot
		elif cmp_cond == 'le':
			return price <= _pivot
		else:
			print ('Invalid comparison {c}'.format(c = cmp_cond))
			return False

class MA ():
    def __init__ (self, period):
        self._period = period
        self._data = list ()
    def get (self):
        assert "Not implemented yet", 0

    def put (self, data):
        assert "Not implemented yet", 0

class SMA (MA):
    def __init__ (self, period):
        MA.__init__ (self, period)

    def get (self):
        if len(self._data) < self._period:
            return None
        else:
            return sum(self._data)/self._period

    def put (self, data):
        self._data.append (data)
        if len(self._data) > self._period:
            del self._data [0]

class EMA (MA):
    def __init__ (self, period):
        SMA.__init__ (self, period)
        self._mul = 2 / (self._period + 1)
        self._pEMA = None
        self._EMA = None

    def get (self):
        return self._EMA

    def put (self, data):
        self._pEMA = self._EMA if self._pEMA is not None else data
        self._EMA = data * self._mul + self._pEMA * (1 - self._mul) 

class BoBa (SMA):
    def __init__ (self, period, avg):
        MA.__init__ (self, period)
        if avg == 'SMA':
            self._avg = SMA (period)
        elif avg == 'EMA':
            self._avg = EMA (period)
        else:
            print ('{avg} is not supported'.format (avg = avg))

    def put (self, data):
        self._avg.put (data)
        SMA.put (self, data)

    def get (self):
        avg = self._avg.get ()
        sd = self.std_deviation ()
        return avg, (sd * 2)

    def std_deviation (self):
        avg = SMA.get (self)
        variance = sum (list (map (lambda x: (x - avg)**2, self._data))) / (self._period - 1)
        return math.sqrt (variance) 

def process_market_data (mdata):
	pass

def pcmp (inpQ, outQ, params, Stop):
	while not Stop.is_set():
		if not inpQ.empty ():
			pass
			inpQ.task_done ()


