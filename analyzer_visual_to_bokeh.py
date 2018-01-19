#!/usr/bin/env python3

from math import pi

from bokeh.plotting import figure
from bokeh.models.glyphs import VBar, Segment
from bokeh.models.markers import Triangle 
from bokeh.models import HoverTool, CrosshairTool

from Agents import misc_utils  as misc
from Agents import chart_utils as chart

def get_figure ():
	p = figure(x_axis_type = 'datetime', sizing_mode = 'scale_width', plot_height = 200)
	p.add_tools(CrosshairTool())
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha = 0.6

	return p

def get_hover ():
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

def draw_up_candles ():
	g0 = Segment (x0 = 'T', y0 = 'H', x1 = 'T', y1 = 'L', line_color = 'black')
	g1 = VBar    (x = 'T', top = 'C', bottom = 'O', width = 250000, fill_color = 'green', line_color = 'black')

	return (g0, g1)

def draw_down_candles ():
	g0 = Segment (x0 = 'T', y0 = 'H', x1 = 'T', y1 = 'L', line_color = 'black')
	g1 = VBar    (x = 'T', top = 'O', bottom = 'C', width = 250000, fill_color = 'red', line_color = 'black')

	return (g0, g1)

def draw_stand_candles ():
	g0 = Segment (x0 = 'T', y0 = 'H', x1 = 'T', y1 = 'L', line_color = 'black')
	g1 = VBar    (x = 'T', top = 'O', bottom = 'C', width = 250000, fill_color = 'black', line_color = 'black')

	return (g0, g1) 

def draw_sell ():
	g0 = Triangle (x = 'T', y = 'price', size = 10, fill_color = 'red', angle = pi, fill_alpha = 0.8)

	return g0 

def draw_buy ():
	g0 = Triangle (x = 'T', y = 'price', size = 10, fill_color = 'green', angle = 0.0, fill_alpha = 0.8)

	return g0 

class DataCvt(misc.BPA):
	def CallBack (self, data):
		new_data = {'candlestick':{}}

		if data['C'] > data['O']:
			new_data['candlestick']['upstick'] = {
					 'L': data['L'],
					 'H': data['H'],
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}
		elif data['C'] < data['O']:
			new_data['candlestick']['downstick'] = {
					 'L': data['L'],
					 'H': data['H'],
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}
		else:
			new_data['candlestick']['standstick'] = {
					 'L': data['L'],
					 'H': data['H'],
					 'C': data['C'],
					 'O': data['O'],
					 'T': data['T']
				}

		if data['profitable'] == True:
			new_data['candlestick']['buy_decision'] = {
					 'price': data['L'],
					 'T': data['T']
				}
		if data['harvestable'] == True:
			new_data['candlestick']['sell_decision'] = {
					 'price': data['H'],
					 'T': data['T']
				}

		self.BroadCast (new_data)

cvt = DataCvt()
cvt.BindTo (chart.CallBack)

chart.add_plot ('candlestick', get_figure)

chart.add_glyph ('candlestick', 'upstick',       draw_up_candles,    {'T':[],'H':[],'L':[],'O':[],'C':[]})
chart.add_glyph ('candlestick', 'downstick',     draw_down_candles,  {'T':[],'H':[],'L':[],'O':[],'C':[]})
chart.add_glyph ('candlestick', 'standstick',    draw_stand_candles, {'T':[],'H':[],'L':[],'O':[],'C':[]})
chart.add_glyph ('candlestick', 'buy_decision',  draw_buy,           {'T':[],'price':[]})
chart.add_glyph ('candlestick', 'sell_decision', draw_sell,          {'T':[],'price':[]})

chart.add_tool ('candlestick', 'upstick',   get_hover())
chart.add_tool ('candlestick', 'downstick', get_hover())
chart.add_tool ('candlestick', 'downstick', get_hover())

