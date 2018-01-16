#/usr/bin/env python3
import matplotlib.pyplot as plt
from datetime import datetime
from functools import singledispatch

@singledispatch
def to_serializable (val):
	return str(val)

@to_serializable.register(datetime)
def ts_datetime (val):
	return val.isoformat() 

def norm (param):
	if type(param) is str:
		return param.strip().lower()
	else:
		return param

def fill_outQ (outQ, qDat):
	for q in outQ:
		q.put (qDat, block = True)

class Archive ():
	def __init__ (self, length):
		self._length = length
		self._data = list ()
		
	def most_recent (self):
		return self._data [-1] if len(self._data) > 0 else None
		
	def data (self, b = None, e = None):
		if len (self._data) == 0:
			return None
		else:
			if b is None and e is None:
				return self._data.copy ()
			elif b is None:
				return self._data [:e]
			elif e is None:
				return self._data [b:]
			else:
				return self._data [b:e]
			
	def push (self, dat):
		self._data.append (dat)
		if len (self._data) > self._length:
			del self._data [0]
		

class BPA (object): # Base Processing Agent
	def __init__ (self, source = None, params = {}):
		self._source = None 
		self._params = {}
		if source is not None:
			self.Bind (source)
		if len(params) > 0:
			self.setParams (params)
		self._observer = list ()

	def Bind (self, source):
		self._source = source
		self._source.BindTo (self.CallBack)

	def setParams (self, params):
		self._params = params.copy ()

	def CallBack (self, data):
		print (data)

	def BroadCast (self, data):
		for cb in self._observer:
			cb (data)

	def BindTo (self, cb):
		self._observer.append (cb)
