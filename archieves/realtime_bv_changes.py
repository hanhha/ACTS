#!/usr/bin/env python3

import pygame
from pygame.locals import *

from time import sleep

import bittrex as bt
import analysis_agent as ag
import line_visual as lv

pAPIv1 = bt.PublicAPI (bt.API_V1_1)
pAPIv2 = bt.PublicAPI (bt.API_V2_0)

timeframe = 'oneMin'

dataset = {'BTC': list(), 'ETH': list(), 'USDT': list()}

WHITE = pygame.Color (255,255,255)
RED = pygame.Color(255,0,0)
GREEN   = pygame.Color(0,255,0)
BLACK = pygame.Color(0,0,0)
YELLOW = pygame.Color(255,255,0)
BLUE = pygame.Color(0,0,255)

pygame.init ()
pygame.font.init ()
infoObject = pygame.display.Info ()

chartw = infoObject.current_w - 330
charth = int((infoObject.current_h - 30)/3)
screen = pygame.display.set_mode ((infoObject.current_w - 300, infoObject.current_h - 30))

eth_chart  = lv.LineVisual (chartw, charth)
btc_chart  = lv.LineVisual (chartw, charth)
usdt_chart = lv.LineVisual (chartw, charth)

idx = 0
#res, m24h = pAPIv1.get_24h_sum ()
res, all_markets = pAPIv1.get_markets () 

def get_base_volumes ():
    all_bv_hist = dict () 
    for market in all_markets:
        mar = market ['MarketName']
        base = market ['BaseCurrency']
        print (mar)
        res, tick = pAPIv2.get_ticks (mar, timeframe, only_lastest = True)
        all_bv_hist [base] = tick [0] ['BV']
    return all_bv_hist

pre_base_vols = get_base_volumes () 

try:
	while True:
		#base_vol = ag.get_base_volumes (m24h)
		base_vol = get_base_volumes ()
		if len (dataset['BTC']) == 100:
			del dataset ['BTC'][0]
			del dataset ['ETH'][0]
			del dataset ['USDT'][0]
		
		dbv = dict()
		
		dbv ['BTC'] = (base_vol ['BTC'] - pre_base_vols ['BTC'])/pre_base_vols['BTC']
		dbv ['ETH'] = (base_vol ['ETH'] - pre_base_vols ['ETH'])/pre_base_vols['ETH']
		dbv ['USDT'] = (base_vol ['USDT'] - pre_base_vols ['USDT'])/pre_base_vols ['USDT']
		#print (dbv)
		pre_base_vols = base_vol.copy()
		
		dataset ['BTC'].append (dbv['BTC'])
		dataset ['ETH'].append (dbv['ETH'])
		dataset ['USDT'].append (dbv['USDT'])
		
		eth_chart.set_dataset  ([ [idx, val] for idx, val in enumerate (dataset['ETH'])])
		btc_chart.set_dataset  ([ [idx, val] for idx, val in enumerate (dataset['BTC'])])
		usdt_chart.set_dataset ([ [idx, val] for idx, val in enumerate (dataset['USDT'])])
			
		if len (dataset ['BTC']) > 1:
			screen.fill (BLACK)
			eth_chart.draw (screen, YELLOW, (0, charth * 2))
			btc_chart.draw (screen, WHITE, (0, charth))
			usdt_chart.draw (screen, GREEN, (0, 0))
		
		pygame.display.flip ()
		
		for evt in pygame.event.get():
			pass
			
		sleep (1)

except KeyboardInterrupt:
	pass
	
pygame.quit ()
			
			
			
