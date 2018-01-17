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

class BPA (object): # Base Processing Agent
	def __init__ (self, source = None, params = {}):
		self._source = None 
		self._params = {}
		if source is not None:
			self.Bind (source)
		if len(params) > 0:
			self.setParams (params)
		self._observer = list ()
		self._print_func = None

	def Bind (self, source):
		self._source = source
		self._source.BindTo (self.CallBack)

	def setParams (self, params):
		self._params = params.copy ()
		if 'print_func' in self._params.keys():
			self._print_func = self._params['print_func']

	def shout (self, text):
		if self._print_func is not None:
			_text = repr(text) if type(text) is not str else text
			self._print_func (_text)
		else:
			print (text)

	def CallBack (self, data):
		self.shout (data)

	def BroadCast (self, data):
		for cb in self._observer:
			cb (data)

	def BindTo (self, cb):
		self._observer.append (cb)
