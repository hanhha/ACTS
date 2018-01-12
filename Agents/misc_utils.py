#/usr/bin/env python3
import matplotlib.pyplot as plt

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

class MouseLine(object):
    def __init__(self, ax, direction = 'V', color = 'red'):
        self.ax = ax
        self.direction = direction
        self.lines = list()
        for a in self.ax:
            if direction == 'V':
                self.lines.append(a.axvline (x = 0, ymin = 0, ymax = 1, c = color, linewidth=0.5, zorder = 5))
            elif direction == 'H':
                self.lines.append(a.axhline (y = 0, xmin = 0, xmax = 1, c = color, linewidth=0.5, zorder = 5))

    def show_line(self, event):
        if event.inaxes in self.ax:
            for l in self.lines:
                x, y = l.get_data(True)
                if self.direction == 'V':
                    x = [event.xdata for i in x]
                elif self.direction == 'H':
                    y = [event.ydata for i in y]
                l.set_data(x, y)
                l.set_visible(True)
        #else:
        #    self.line.set_visible(False)
        plt.draw()

def draw_hthresholds (ax, base = 0, upper = 30, lower = -30, color = 'red', show_base = True):
    ax.axhline (y = base + upper, xmin = 0, xmax = 1,c=color, linewidth=0.5, zorder = 0)
    if show_base:
        ax.axhline (y = base , xmin = 0, xmax = 1,c=color, linewidth=0.5, zorder = 0)
    ax.axhline (y = base + lower, xmin = 0, xmax = 1,c=color, linewidth=0.5, zorder = 0)