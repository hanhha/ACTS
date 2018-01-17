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

TOOLS = "pan, wheel_zoom, box_zoom, reset, save"

def draw_candlesticks (data, hprice = 'H', cprice = 'C', oprice = 'O', lprice = 'L', timestamp = 'T', width = 300, name = 'Candles', ref_fig = None, ref_axes = None, decision = None):
	bar_width = (width-50) * 1000
	plot_height = 200
	line_color = 'black'
	inc_color = 'green'
	dec_color = 'red'
	buy_color = 'green'
	sale_color = 'red'

	if ref_axes == 'x':
		p = figure(title = name, x_axis_type = 'datetime', tools = TOOLS, sizing_mode = 'scale_width', plot_height = plot_height, x_range = ref_fig.x_range)
	elif ref_axes == 'y':
		p = figure(title = name, x_axis_type = 'datetime', tools = TOOLS, sizing_mode = 'scale_width', plot_height = plot_height, y_range = ref_fig.y_range)
	elif ref_axes == 'both':
		p = figure(title = name, x_axis_type = 'datetime', tools = TOOLS, sizing_mode = 'scale_width', plot_height = plot_height, x_range = ref_fig.x_range, y_range = ref_fig.y_range)
	else:
		p = figure(title = name, x_axis_type = 'datetime', tools = TOOLS, sizing_mode = 'scale_width', plot_height = plot_height)

	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha = 0.6

	inc  = data[cprice] >  data[oprice]
	dec  = data[cprice] <  data[oprice]
	keep = data[cprice] == data[oprice]

	p.segment(data[timestamp].values, data[hprice].values, data[timestamp].values, data[lprice].values, color = line_color)
	p.vbar (data[timestamp][inc], bar_width, data[oprice][inc], data[cprice][inc], fill_color=inc_color, line_color = line_color)
	p.vbar (data[timestamp][dec], bar_width, data[oprice][dec], data[cprice][dec], fill_color=dec_color, line_color = line_color)
	p.vbar (data[timestamp][keep], bar_width, data[oprice][keep], data[cprice][keep], fill_color=line_color, line_color = line_color)

	if decision is not None:
		buy = data[decision] == True
		sale = data[decision] == False
		p.triangle (data[timestamp][buy], data[lprice][buy], size = 10, color = buy_color, angle = 0.0, fill_alpha = 0.8)
		p.triangle (data[timestamp][sale], data[hprice][sale], size = 10, color = sale_color, angle = pi, fill_alpha = 0.8)

	return p

def draw_lines (data, interest = 'C', timestamp = 'T', name = 'Line', color = 'red', ref_fig = None, ref_axes = None):
	plot_height = 200
	line_color = color
	if ref_axes == 'x':
		fig = figure (title = name, x_axis_type = "datetime", sizing_mode = 'scale_width', plot_height = plot_height, x_range = ref_fig.x_range)
	elif ref_axes == 'y':
		fig = figure (title = name, x_axis_type = "datetime", sizing_mode = 'scale_width', plot_height = plot_height, y_range = ref_fig.y_range)
	elif ref_axes == 'both':
		fig = figure (title = name, x_axis_type = "datetime", sizing_mode = 'scale_width', plot_height = plot_height, y_range = ref_fig.y_range, x_range = ref_fig.x_range)
	else:
		fig = figure (title = name, x_axis_type = "datetime", sizing_mode = 'scale_width', plot_height = plot_height)

	fig.grid.grid_line_alpha = 0.6
	fig.xaxis.major_label_orientation = pi/4

	fig.line (color = color, x = data[timestamp].values, y = data[interest].values)
	
	return fig

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

	@gen.coroutine
	def DataCB (self):
		if not self.server_in_cb_process:
			self.server_in_cb_process = True
			self.new_plot_data = self.new_data.copy()
			self.new_data = dict ()

			for kp, vp in self.new_plot_data.items():
				for kg, vg in vp.items():
					self.sources[kp][kg].stream (vg)
			
			self.server_in_cb_process = False
	
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
