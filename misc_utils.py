#/usr/bin/env python3

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
		