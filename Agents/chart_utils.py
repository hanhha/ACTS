#!/usr/bin/env python3

from bokeh.plotting import figure, curdoc
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

sources          = dict()
plots            = OrderedDict ()
glyphs           = OrderedDict ()
additional_tools = dict ()
renderers        = dict ()

new_data         = dict ()

title            = ''

cb_lock    = Lock () 

plots_list = list ()

port = 8886 
allow_websocket_origin = ['localhost:8886']


def add_plot ( plot_key, plot):
	global sources, plots, glyphs

	sources [plot_key] = dict () 
	plots [plot_key] = plot
	glyphs [plot_key] = dict()

def add_glyph ( plot_key, glyph_key, glyph, column_dict):
	global sources, glyphs

	sources  [plot_key][glyph_key] = ColumnDataSource(column_dict)
	glyphs   [plot_key][glyph_key] = glyph

def add_tool ( plot_key, glyph_key, tool):
	global additional_tools
	if plot_key not in additional_tools.keys():
		additional_tools[plot_key] = {glyph_key : tool}
	else:
		if glyph_key in additional_tools[plot_key].keys():
			additional_tools[plot_key][glyph_key].append (tool)
		else:
			additional_tools[plot_key][glyph_key] = [tool]

new_data_lock = Lock ()

@gen.coroutine
def real_update_data ():
	global new_data, sources, cb_lock
	global new_data_lock

	new_data_lock.acquire ()
	new_plot_data = new_data.copy()
	new_data = dict ()
	new_data_lock.release ()

	for kp, vp in new_plot_data.items():
		for kg, vg in vp.items():
			if kp in sources.keys():
				if kg in sources[kp].keys():
					sources[kp][kg].stream (vg)#, rollover = 288)
	cb_lock.release ()

@gen.coroutine
@without_document_lock
def update_data ():
	global cb_lock

	if cb_lock.acquire (False):
		curdoc().add_next_tick_callback (real_update_data)

def CallBack ( data):
	global new_data, new_data_lock

	new_data_lock.acquire ()
	for kp, vp in data.items():
		for kg, vg in vp.items():
			if kp not in new_data.keys():
				new_data[kp] = {kg : {}}
			if kg not in new_data[kp].keys():
				new_data[kp][kg] = {}
			for k, v in vg.items():
				if k not in new_data[kp][kg].keys():
					new_data[kp][kg][k] = [v]
				else:
					new_data[kp][kg][k].append(v)
	new_data_lock.release ()

def modify_document (doc):
	global plots, glyphs, sources, cb_lock, additional_tools, renderers
	global plots_list

	cb_lock.acquire ()

	plots_list = list ()
	
	for k, plot in plots.items():
		fig = plot ()
		renderers [k] = dict ()

		for gk, gv in glyphs[k].items():
			tmp_dict = sources[k][gk].to_df().to_dict(orient='list')
			sources[k][gk] = ColumnDataSource(tmp_dict)

			glyph = gv ()

			if type(glyph) is tuple:
				tmp = None
				for g in glyph:
					tmp = fig.add_glyph (sources[k][gk], g)

				renderers [k][gk] = tmp # last ride of the day

			else:
				tmp = fig.add_glyph (sources[k][gk], glyph)
				renderers [k][gk] = tmp 

			if k in additional_tools.keys():
				if gk in additional_tools[k].keys():
					tool = additional_tools[k][gk]

					if type(tool) is not list:
						tool.renderers = [renderers [k][gk]]
						fig.add_tools (tool)

					else:
						for t in tool:
							t.renderers = [renderers [k][gk]]
							fig.add_tools (t)
		if len(plots_list) > 0:
			fig.x_range = plots_list[-1].x_range	

		plots_list.append (fig)

	doc.add_root (column(*plots_list, sizing_mode = 'scale_width'))

	doc.title = title 
	doc.add_periodic_callback (update_data, 1000)

	cb_lock.release ()

	return doc

app = {'/analyzing': Application(FunctionHandler(modify_document))}

server = None

def start ():
	global server, io_loop, allow_websocket_origin, port, app

	server = Server (app, port = port, allow_websocket_origin = allow_websocket_origin)
	server.start ()
	t = Thread (name = "bokeh_chart", target = server.io_loop.start)
	t.daemon = True
	t.start ()

def stop ():
	global server
	server.io_loop.stop ()
