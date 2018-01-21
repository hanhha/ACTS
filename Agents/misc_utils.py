#/usr/bin/env python3
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
		self._bkdr_observer = list ()
		self._print_func = None

	def Bind (self, source):
		self._source = source
		self._source.BindTo (self.CallBack)
		self._source.BkdrBindTo (self.BkdrCallBack)

	def setParams (self, params):
		self._params = params.copy ()
		if 'shout_func' in self._params.keys():
			self._print_func = self._params['shout_func']
	
	def setShoutFunc (self, func):
		self._print_func = func

	def shout (self, text, **kwargs):
		if self._print_func is not None:
			_text = repr(text) if type(text) is not str else text
			try:
				_kwargs = {**kwargs, **{'verbose':2}} if 'verbose' not in kwargs.keys() else kwargs
				self._print_func (_text, **_kwargs)
			except (AttributeError, TypeError):
				print (_text)
		else:
			print (text)

	def BkdrCallBack (self, data):
		pass

	def CallBack (self, data):
		self.shout (data)

	def BroadCast (self, data):
		for cb in self._observer:
			cb (data)

	def BroadCastPush (self, data):
		for cb in self._bkdr_observer:
			cb (data)

	def BindTo (self, cb):
		self._observer.append (cb)

	def BkdrBindTo (self, cb):
		self._bkdr_observer.append (cb)

	def setFeedback (self, fb):
		self._feedback = fb

	def Feedback (self, data):
		if self._feedback is not None:
			self._feedback (data)
		else:
			raise ValueError ("No feedback was set!")
