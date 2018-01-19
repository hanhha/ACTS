#!/usr/bin/env python3

from bokeh.plotting import figure, curdoc
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.document import without_document_lock
from bokeh.models import ColumnDataSource 
from bokeh.server.server import Server

from tornado import gen, ioloop, autoreload
from collections import OrderedDict
from pandas import DataFrame

from threading import Thread

sources          = dict()
plots            = OrderedDict ()
glyphs           = dict ()
additional_tools = dict ()
renderers        = dict ()

new_data         = dict ()

title         = ''

in_cb_process = False

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

@gen.coroutine
def update_data ():
	global new_data, sources, in_cb_process

	if not in_cb_process:
		in_cb_process = True

		new_plot_data = new_data.copy()
		new_data = dict ()

		for kp, vp in new_plot_data.items():
			for kg, vg in vp.items():
				sources[kp][kg].stream (vg)

		in_cb_process = False

def CallBack ( data):
	global new_data

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

def modify_document (doc):
	global plots, glyphs, sources, in_cb_process, additional_tools, renderers

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
				renderers [k][gk] = tmp # last ride of the day

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
				
		doc.add_root (fig)

	doc.title = title 
	doc.add_periodic_callback (update_data, 1000)

	in_cb_process = False

port = 8888
allow_websocket_origin = ['localhost:8888', 'enco.hopto.org:8888']

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
