#!/usr/bin/env python3

from bokeh.plotting import figure
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.document import without_document_lock
from bokeh.models import ColumnDataSource 
from bokeh.layouts import  column 
from bokeh.server.server import Server

from tornado import gen, ioloop, autoreload
from collections import OrderedDict
from pandas import DataFrame

from threading import Thread, Lock

from . import misc_utils as misc

class Chart(misc.BPA):
	def __init__ (self, title = 'Noname', source = None, params = {}, port = 8888, allowed_origins = ['localhost:8888',]):
		misc.BPA.__init__ (self, source, params)

		self.title            = title

		self.sources          = dict()
		self.plots            = OrderedDict ()
		self.glyphs           = OrderedDict ()
		self.additional_tools = dict ()
		self.renderers        = dict ()
		self.plots_list       = list ()

		self.port                   = port 
		self.allow_websocket_origin = allowed_origins 
		self.server                 = None
		self.app                    = None

		self.new_data      = dict ()
		self.cb_lock       = Lock () 
		self.new_data_lock = Lock ()
		self.exec_t        = None

	def add_plot (self, plot_key, plot):
		self.sources [plot_key] = dict () 
		self.plots   [plot_key] = plot
		self.glyphs  [plot_key] = dict()
	
	def add_glyph (self, plot_key, glyph_key, glyph, column_dict):
		self.sources  [plot_key][glyph_key] = ColumnDataSource(column_dict)
		self.glyphs   [plot_key][glyph_key] = glyph
	
	def add_tool (self, plot_key, glyph_key, tool):
		if plot_key not in self.additional_tools.keys():
			self.additional_tools[plot_key] = {glyph_key : tool}
		else:
			if glyph_key in self.additional_tools[plot_key].keys():
				self.additional_tools[plot_key][glyph_key].append (tool)
			else:
				self.additional_tools[plot_key][glyph_key] = [tool]
	
	def CallBack (self, data):
		self.new_data_lock.acquire ()
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

		self.new_data_lock.release ()
	
	def start (self):
		def modify_document (doc):
			self.cb_lock.acquire ()
			self.doc = doc
			self.plots_list = list ()
			
			for k, plot in self.plots.items():
				fig = plot ()
				self.renderers [k] = dict ()
		
				for gk, gv in self.glyphs[k].items():
					tmp_dict = self.sources[k][gk].to_df().to_dict(orient='list')
					self.sources[k][gk] = ColumnDataSource(tmp_dict)
		
					glyph = gv ()
		
					if type(glyph) is tuple:
						tmp = None
						for g in glyph:
							tmp = fig.add_glyph (self.sources[k][gk], g)
		
						self.renderers [k][gk] = tmp # last ride of the day
		
					else:
						tmp = fig.add_glyph (self.sources[k][gk], glyph)
						self.renderers [k][gk] = tmp 
		
					if k in self.additional_tools.keys():
						if gk in self.additional_tools[k].keys():
							tool = self.additional_tools[k][gk]
		
							if type(tool) is not list:
								tool.renderers = [self.renderers [k][gk]]
								fig.add_tools (tool)
		
							else:
								for t in tool:
									t.renderers = [self.renderers [k][gk]]
									fig.add_tools (t)
				if len(self.plots_list) > 0:
					fig.x_range = self.plots_list[-1].x_range	
		
				self.plots_list.append (fig)

			@gen.coroutine
			def real_update_data ():
				self.new_data_lock.acquire ()
				self.new_plot_data = new_data.copy()
				self.new_data = dict ()
				self.new_data_lock.release ()
			
				for kp, vp in self.new_plot_data.items():
					for kg, vg in vp.items():
						if kp in self.sources.keys():
							if kg in self.sources[kp].keys():
								self.sources[kp][kg].stream (vg)#, rollover = 288)
				self.cb_lock.release ()
			
			@gen.coroutine
			@without_document_lock
			def update_data ():
				if self.cb_lock.acquire (False):
					self.doc.add_next_tick_callback (real_update_data)
			
				self.doc.title = self.title 
				self.doc.add_root (column(*self.plots_list, sizing_mode = 'scale_width'))
			
				self.doc.add_periodic_callback (update_data, 1000)
				self.cb_lock.release ()
			
				return self.doc
	
		app = {'/analyzing': Application(FunctionHandler(modify_document))}
	
		self.server = Server (app, port = self.port, allow_websocket_origin = self.allow_websocket_origin)
		self.server.start ()
		self.exec_t        = Thread (name = "bokeh_chart", target = self.server.io_loop.start)
		self.exec_t.daemon = True
		self.exec_t.start ()
	
	def stop ():
		self.server.io_loop.stop ()
