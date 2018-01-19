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

sources = dict()
plots   = OrderedDict ()
glyphs  = dict ()

new_data = dict ()

title = ''

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
	global plots, glyphs, sources, in_cb_process

	for k, plot in plots.items():
		fig = plot () 

		for gk, gv in glyphs[k].items():
			tmp_dict = sources[k][gk].to_df().to_dict(orient='list')
			sources[k][gk] = ColumnDataSource(tmp_dict)

			glyph = gv ()
			if type(glyph) is tuple:
				for g in glyph:
					fig.add_glyph (sources[k][gk], g)
			else:
				fig.add_glyph (sources[k][gk], glyph)

		doc.add_root (fig)

	doc.title = title 
	doc.add_periodic_callback (update_data, 1000)

	in_cb_process = False

port = 8888
allow_websocket_origin = ['localhost:8888']

app = {'/analyzing': Application(FunctionHandler(modify_document))}

io_loop = ioloop.IOLoop.instance ()
autoreload.start (io_loop)

server = Server (app, port = port, io_loop = io_loop, allow_websocket_origin = allow_websocket_origin)
server.start ()

def start ():
	pass

def io_start (io_loop):
	io_loop.start ()

def stop ():
	global io_loop
	io_loop.stop ()

t = Thread (target = io_start, args = (io_loop,))
t.start ()

#def start ():
#	from bokeh.client import push_session
#
#	doc = curdoc ()
#	modify_document (doc)
#	session = push_session (document = doc)
#	session.show ()
#	t = Thread (target = session.loop_until_closed)
#	t.daemon = True
#	t.start ()
#
#def stop ():
#	pass
