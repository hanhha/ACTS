#!/usr/bin/env python3

from math import pi

from bokeh.plotting import figure
from bokeh.models.glyphs import VBar, Segment, Line
from bokeh.models.markers import Triangle 
from bokeh.models import HoverTool, CrosshairTool

import pandas as pd

from Agents import misc_utils  as misc
from Agents import chart_utils as chart

timeframe = 100

def get_figure_0 ():
	p = figure(x_axis_type = 'datetime', sizing_mode = 'scale_width', plot_height = 200)
	p.add_tools(CrosshairTool())
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha = 0.6

	return p

def get_figure_1 ():
	p = figure(x_axis_type = 'datetime', sizing_mode = 'scale_width', plot_height = 50)
	p.add_tools(CrosshairTool())
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha = 0.6

	return p

def get_candlestick_hover ():
	hover = HoverTool (renderers = [],
			tooltips = [
				("T", "@T{%F}"),
				("O", "@O"),
				("C", "@C"),
				("H", "@H"),
				("L", "@L"),
			],

			formatters = {
				'T': 'datetime'
			},
			
			mode = 'vline'
	)

	return hover

def draw_highlow_segment ():
	g0 = Segment (x0 = 'T', y0 = 'H', x1 = 'T', y1 = 'L', line_color = 'black')
	return g0

def draw_up_candles ():
	global timeframe
	g1 = VBar    (x = 'T', top = 'C', bottom = 'O', width = timeframe * 1000 - 2, fill_color = 'green', line_color = 'black')

	return g1

def draw_down_candles ():
	global timeframe
	g1 = VBar    (x = 'T', top = 'O', bottom = 'C', width = timeframe * 1000 - 2, fill_color = 'red', line_color = 'black')

	return g1

def draw_stand_candles ():
	global timeframe
	g1 = VBar    (x = 'T', top = 'O', bottom = 'C', width = timeframe * 1000 - 2, fill_color = 'black', line_color = 'black')

	return g1 

def draw_sell ():
	g0 = Triangle (x = 'T', y = 'H', size = 10, fill_color = 'red', angle = pi, fill_alpha = 0.8)

	return g0 

def draw_buy ():
	g0 = Triangle (x = 'T', y = 'L', size = 10, fill_color = 'green', angle = 0.0, fill_alpha = 0.8)

	return g0 

def draw_rsi6 ():
	g0 = Line (x = 'T', y = 'val', line_color = 'blue')
	return g0

def draw_pvt ():
	g0 = Line (x = 'T', y = 'val', line_color = 'blue')
	return g0

class DataCvt(misc.BPA):
	def CallBack (self, data):
		new_data = {'candlestick':{}}

		if data['C'] > data['O']:
			new_data['candlestick']['upstick'] = {
					 'C': data['C'],
					 'O': data['O'],
					 'H': data['H'],
					 'L': data['L'],
					 'T': data['T']
				}
		elif data['C'] < data['O']:
			new_data['candlestick']['downstick'] = {
					 'C': data['C'],
					 'O': data['O'],
					 'H': data['H'],
					 'L': data['L'],
					 'T': data['T']
				}
		else:
			new_data['candlestick']['standstick'] = {
					 'C': data['C'],
					 'O': data['O'],
					 'H': data['H'],
					 'L': data['L'],
					 'T': data['T']
				}

		if data['act'][0] == 'buy':
			new_data['candlestick']['buy_decision'] = {
					 'L': data['L'],
					 'T': data['T']
				}
		elif data['act'][0] == 'sell':
			new_data['candlestick']['sell_decision'] = {
					 'H': data['H'],
					 'T': data['T']
				}

		new_data['candlestick']['highlow'] = {
				'T': data['T'],
				'H': data['H'],
				'L': data['L']
			}

		for k, v in data['calculations'].items ():
			v = 'NaN' if pd.isnull(v) else v
			new_data[k] = {k: {'T': data['T'], 'val': v}}

		self.BroadCast (new_data)

cvt = DataCvt()
cvt.BindTo (chart.CallBack)

chart.add_plot ('candlestick', get_figure_0)

chart.add_glyph ('candlestick', 'highlow',       draw_highlow_segment, {'T':[],'H':[], 'L':[]})
chart.add_glyph ('candlestick', 'upstick',       draw_up_candles,    {'T':[],'O':[],'C':[], 'H':[], 'L':[]})
chart.add_glyph ('candlestick', 'downstick',     draw_down_candles,  {'T':[],'O':[],'C':[], 'H':[], 'L':[]})
chart.add_glyph ('candlestick', 'standstick',    draw_stand_candles, {'T':[],'O':[],'C':[], 'H':[], 'L':[]})
chart.add_glyph ('candlestick', 'buy_decision',  draw_buy,           {'T':[],'L':[]})
chart.add_glyph ('candlestick', 'sell_decision', draw_sell,          {'T':[],'H':[]})
chart.add_tool ('candlestick', 'upstick',   get_candlestick_hover())
chart.add_tool ('candlestick', 'downstick',   get_candlestick_hover())
chart.add_tool ('candlestick', 'standstick',   get_candlestick_hover())

chart.add_plot ('rsi6', get_figure_1)
chart.add_plot ('pvt', get_figure_1)
chart.add_glyph ('rsi6', 'rsi6', draw_rsi6, {'T':[], 'val':[]})
chart.add_glyph ('pvt', 'pvt', draw_pvt, {'T':[], 'val':[]})

