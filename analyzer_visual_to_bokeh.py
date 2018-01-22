#!/usr/bin/env python3

from math import pi

from bokeh.plotting import figure
from bokeh.models.glyphs import VBar, Segment, Line
from bokeh.models.markers import Triangle 
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import Span

import pandas as pd

from Agents import misc_utils  as misc
from Agents import chart_utils as chart

def get_figure_0 ():
	p = figure(x_axis_type = 'datetime', sizing_mode = 'scale_width', plot_height = 200)
	p.add_tools(CrosshairTool())
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha = 0.6

	return p

def get_figure_pvt ():
	p = figure(x_axis_type = 'datetime', sizing_mode = 'scale_width', plot_height = 50)
	p.add_tools(CrosshairTool())
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha = 0.6

	return p

def get_figure_rsi ():
	p = figure(x_axis_type = 'datetime', sizing_mode = 'scale_width', plot_height = 50)
	p.add_tools(CrosshairTool())
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha = 0.6

	upper = Span (location = 30, dimension='width', line_color='black')
	lower = Span (location = -30, dimension='width', line_color='black')

	p.add_layout (upper)
	p.add_layout (lower)

	return p

def draw_highlow_segment ():
	g0 = Segment (x0 = 'T', y0 = 'H', x1 = 'T', y1 = 'L', line_color = 'black')
	return g0

def draw_up_candles ():
	g1 = VBar    (x = 'T', top = 'C', bottom = 'O', width = 250000, fill_color = 'green', line_color = 'black')

	return g1

def draw_down_candles ():
	g1 = VBar    (x = 'T', top = 'O', bottom = 'C', width = 250000, fill_color = 'red', line_color = 'black')

	return g1

def draw_stand_candles ():
	g1 = VBar    (x = 'T', top = 'O', bottom = 'C', width = 250000, fill_color = 'black', line_color = 'black')

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

def draw_ema ():
	g0 = Line (x = 'T', y = 'val', line_color = 'blue')
	return g0

class DataCvt(misc.BPA):
	def CallBack (self, data):
		new_data = {'candlestick':{}}

		if data['C'] > data['O']:
			new_data['candlestick']['upstick'] = {
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}
		elif data['C'] < data['O']:
			new_data['candlestick']['downstick'] = {
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}
		else:
			new_data['candlestick']['standstick'] = {
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}

		if data['profitable'] == True:
			new_data['candlestick']['buy_decision'] = {
					 'L': data['L'],
					 'T': data['T']
				}
		if data['harvestable'] == True:
			new_data['candlestick']['sell_decision'] = {
					 'H': data['H'],
					 'T': data['T']
				}

		new_data['candlestick']['highlow'] = {
				'T': data['T'],
				'H': data['H'],
				'C': data['C'],
				'O': data['O'],
				'L': data['L']
			}

		for k, v in data['calculations'].items ():
			v = 'NaN' if pd.isnull(v) else v
			if k == 'ema':
				new_data['candlestick']['ema'] = {'T': data['T'], 'val': v}
			else:
				new_data[k] = {k: {'T': data['T'], 'val': v}}

		self.BroadCast (new_data)

cvt = DataCvt()
cvt.BindTo (chart.CallBack)

chart.add_plot ('candlestick', get_figure_0)

chart.add_glyph ('candlestick', 'highlow',       draw_highlow_segment, {'T':[],'H':[],'C':[], 'O':[], 'L':[]})
chart.add_glyph ('candlestick', 'upstick',       draw_up_candles,    {'T':[],'O':[],'C':[]})
chart.add_glyph ('candlestick', 'downstick',     draw_down_candles,  {'T':[],'O':[],'C':[]})
chart.add_glyph ('candlestick', 'standstick',    draw_stand_candles, {'T':[],'O':[],'C':[]})
chart.add_glyph ('candlestick', 'buy_decision',  draw_buy,           {'T':[],'L':[]})
chart.add_glyph ('candlestick', 'sell_decision', draw_sell,          {'T':[],'H':[]})
chart.add_glyph ('candlestick', 'ema',          draw_ema,          {'T':[],'val':[]})

chart.add_plot ('rsi6', get_figure_rsi)
chart.add_plot ('pvt', get_figure_pvt)
chart.add_glyph ('rsi6', 'rsi6', draw_rsi6, {'T':[], 'val':[]})
chart.add_glyph ('pvt', 'pvt', draw_pvt, {'T':[], 'val':[]})
