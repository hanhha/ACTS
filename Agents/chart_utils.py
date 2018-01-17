from math import pi 

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label

from threading import Thread, Event
from collections import OrderedDict

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
	def __init__ (self, title = '', port = 8888, allow_websocket_origin=['localhost:8888','enco.hopto.org:8888']):
		self._execThread = None

		self.sources = dict()
		self.plots   = OrderedDict ()
		self.glyphs  = dict ()

		self.new_data = dict ()

		self.title = title
		self.port = port
		self.allow_websocket_origin = allow_websocket_origin

	def add_plot (self, plot_key, plot):
		self.sources [plot_key] = dict () 
		self.plots [plot_key] = plot
		self.new_data [plot_key] = dict ()

	def add_glyph (self, plot_key, glyph_key, glyph, column_dict):
		self.sources [plot_key][glyph_key] = ColumnDataSource(column_dict)
		self.glyphs[plot_key][glyph_key] = glyph
		self.new_data[plot_key][glyph_key] = dict ()

	def idle (self):
		self.app = {'/': Application(FunctionHandler(self.make_document))}
		self.server = Server(self.app, port = self.port, allow_websocket_origin = self.allow_websocket_origin)

		def monitor ():
			self.server.start ()
			self.server.io_loop.start ()

		self._execThread = Thread (target = monitor)
		self._execThread.daemon = True
		self._execThread.start () 

	def stop (self):
		self.server.io_loop.stop ()
		self._execThread.join ()

	def CallBack (self, data):
	#{plot:{glyph:{k:v}}}
		for k_plot, plot_data in data.items():
			for k_glyph, source in plot_data.items():
				if k_plot not in self.new_data.keys():
					self.new_data[k_plot] = {k_glyph:[]} 
				else:
					self.new_data[k_plot][k_glyph] = []
				for k, v in source.items():
					if k not in self.new_data[k_plot][k_glyph].keys():
						self.new_data[k_plot][k_glyph] = {k:[v]}
					else:
						self.new_data[k_plot][k_glyph][k].append(v)

	def make_document (self, doc):
		def update ():
			for kp, psource in self.sources.items():
				for kg, gsource in psource.items():
					if self.new_data[kp][kg]:
						gsource.stream (self.new_data[kp][kg].copy())
						self.new_data[kp][kg] = dict()

		for k, plot in self.plots.items():
			fig = plot 

			for gk, gv in self.glyphs.items():
				fig.add_glyph (self.sources[k][gk], gv)

			doc.add_root (fig)

		doc.add_periodic_callback (update, 1000)
		doc.title = self.title 
