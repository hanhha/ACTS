from math import pi 
from copy import deepcopy

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, curdoc
from bokeh.document import without_document_lock
from bokeh.models import ColumnDataSource 

from tornado import gen, ioloop

from threading import Thread, Event
from collections import OrderedDict

from pandas import DataFrame

class PlottingServer(object):
	def __init__ (self, title = '', port = 8888, allow_websocket_origin=['localhost:8888']):
		self._execThread = None

		self.sources = dict()
		self.plots   = OrderedDict ()
		self.glyphs  = dict ()

		self.new_data = dict ()
		self.new_plot_data = dict ()

		self.title = title
		self.port = port
		self.allow_websocket_origin = allow_websocket_origin

		self.server_in_cb_process = False
		self.server_is_running    = False

		self.app = {'/analyzing': Application(FunctionHandler(self.make_document))}

	def add_plot (self, plot_key, plot):
		self.sources [plot_key] = dict () 
		self.plots [plot_key] = plot
		self.new_data [plot_key] = dict ()
		self.glyphs [plot_key] = dict()

	def add_glyph (self, plot_key, glyph_key, glyph, column_dict):
		self.sources  [plot_key][glyph_key] = ColumnDataSource(column_dict)
		self.glyphs   [plot_key][glyph_key] = glyph
		self.new_data [plot_key][glyph_key] = dict ()

	def server_start (self):
		self.server.start ()
		self.server.io_loop.start ()

	def server_stop (self):
		self.server.stop ()
		self.server.io_loop.stop ()

	def idle (self):
		self.server = Server(self.app, port = self.port, allow_websocket_origin = self.allow_websocket_origin)
		t = Thread(target=self.server_start)
		t.start ()

	def stop (self):
		self.server_stop ()
		self.server_is_running = False

	#@gen.coroutine
	def update (self):
		self.new_plot_data = self.new_data.copy()
		self.new_data = dict ()

		for kp, vp in self.new_plot_data.items():
			for kg, vg in vp.items():
				self.sources[kp][kg].stream (vg)
		
		self.server_in_cb_process = False

	#@gen.coroutine
	@without_document_lock
	def DataCB (self):
		if not self.server_in_cb_process:
			self.server_in_cb_process = True
			curdoc().add_next_tick_callback (self.update)
	
	def CallBack (self, data):
		for kp, vp in data.items():
			for kg, vg in vp.items():
				if kp not in self.new_data.keys():
					self.new_data[kp] = {kg : {}}
				if kg not in self.new_data[kp].keys():
					self.new_data[kp][kg] = {}
				for k, v in vg.items():
					if k not in self.new_data[kp][kg].keys():
						self.new_data[kp][kg][k] = [v]
					else:
						self.new_data[kp][kg][k].append(v)

	def make_document (self, doc):
		for k, plot in self.plots.items():
			fig = plot () 

			for gk, gv in self.glyphs[k].items():
				tmp_dict = self.sources[k][gk].to_df().to_dict(orient='list')
				#del self.sources[k][gk]
				self.sources[k][gk] = ColumnDataSource(tmp_dict)

				glyph = gv ()
				if type(glyph) is tuple:
					for g in glyph:
						fig.add_glyph (self.sources[k][gk], g)
				else:
					fig.add_glyph (self.sources[k][gk], glyph)

			doc.add_root (fig)

		doc.title = self.title 
		doc.add_periodic_callback (self.DataCB, 1000)

		self.server_is_running = True
		self.server_in_cb_process = False

		return doc 
