#!/usr/bin/env python3

import bittrex as exchg
import bittrex_trade_cfg as exchg_cfg

mAPI = exchg.MarketAPI  (exchg.API_V1_1, exchg_cfg.API_KEY, exchg_cfg.API_SECRET) 
aAPI = exchg.AccountAPI (exchg.API_V1_1, exchg_cfg.API_KEY, exchg_cfg.API_SECRET) 
pAPIv2 = exchg.PublicAPI  (exchg.API_V2_0)
pAPIv1 = exchg.PublicAPI  (exchg.API_V1_1)

def sell (inpQ, outQ, params, Stop):
    market, price, qty = params
    assert (type(price) is str or type(price) is int or type(price) is float)
    assert (type(qty) is str or type(qty) is int or type(qty) is float)
    price = float(price) if type(price) is int or type(price) is float else price
    qty = float(qty) if type(qty) is int or type(qty) is float else qty

    while not Stop.is_set():
        if not inpQ.empty ():
            tmp = inpQ.get (block = False)
            balance_avail, balance = aAPI.get_balance (market.split('-')[1])
            price_avail, ticker = pAPIv1.get_ticker (market)

            if price is 'last':
                price = ticker ['Last'] if price_avail else None
            if qty is 'all':
                qty = balance ['Available'] if balance_avail else None

            if price is not None and qty is not None:
                order_res, msg = mAPI.sell_limit (market, qty, price)
                if order_res:
                    outQ.put ((True, msg['uuid']), block = True)
                else:
                    outQ.put ((False, msg), block = True)

            else:
                outQ.put ((False, 'Can not get last price or avaiable coins'), block = True)

            inpQ.task_done ()

def buy (inpQ, outQ, params, Stop):
    market, price, qty = params
    assert (type(price) is str or type(price) is int or type(price) is float)
    assert (type(qty) is str or type(qty) is int or type(qty) is float)
    price = float(price) if type(price) is int or type(price) is float else price
    qty = float(qty) if type(qty) is int or type(qty) is float else qty

    while not Stop.is_set():
        if not inpQ.empty ():
            tmp = inpQ.get (block = False)
            balance_avail, balance = aAPI.get_balance (market.split('-')[1])
            price_avail, ticker = pAPIv1.get_ticker (market)

            if price is 'last':
                price = ticker ['Last'] if price_avail else None
            if qty is 'all':
                qty = balance ['Available'] if balance_avail else None

            if price is not None and qty is not None:
                order_res, msg = mAPI.buy_limit (market, qty, price)
                if order_res:
                    outQ.put ((True, msg['uuid']), block = True)
                else:
                    outQ.put ((False, msg), block = True)

            else:
                outQ.put ((False, 'Can not get last price or avaiable coins'), block = True)

            inpQ.task_done ()

def cancel (inpQ, outQ, params, Stop):
    #TODO: cancel
    pass
