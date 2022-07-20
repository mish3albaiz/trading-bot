# trading_bot.py - Python program to trade stocks using Alpaca API
# 4/4/2022
# Meshal Albaiz

import alpaca_trade_api as tradeapi # trading API
import time # time functions
from symbols import symbol_list # python file with list of stock market tickers
from dictionary_symbols import * # python dictionary of symbols and order information
import math # math functions
from datetime import datetime # time and date functions
import pytz # python timezone library

SEC_KEY = 'XXXX' # secret and public keys for the Alpaca API
PUB_KEY = 'XXXX'
BASE_URL = 'https://paper-api.alpaca.markets' # URL to access API
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL) # API object

now = pytz.utc.localize(datetime.utcnow()) # current time UTC
tz = pytz.timezone("America/New_York") # New York timezone
ny_time = now.astimezone(tz) # convert time to NY timezone
hour = ny_time.hour # hour in NY
minute = ny_time.minute # minute in NY
day = ny_time.weekday() # day in NY

# time and day checks to only trade Mon-Fri 9:35AM to 3:55PM
time_check = (hour == 9 and minute >= 35) or (hour == 15 and minute < 56) or (15 > hour > 9)
day_check = 0 <= day < 5

def selling(): # function to sell held position
    for symbol in symbol_list: # for every ticker in list
        position = get_pos(symbol) # get position of company
        if position != False: # if position exists
            if(get_position_csv(symbol)['held'] == "True"): # if sell order was not placed then order sell
                cost = float(position.avg_entry_price) # get cost of position
                price = str(truncate(cost*1.01, 2)) # set selling price at 1% more
                sell(symbol, "1", price) # sell 1 stock

def buying(): # function to buy unheld position
    for symbol in symbol_list: # for every ticker in list
        position = get_pos(symbol) # get position of company
        if position == False: # if position doesn't exist
            if(get_position_csv(symbol)['held'] == "False"): # if buy  order was not placed then order buy
                buy(symbol, "1") # buy 1 stock at market price

def get_pos(symbol): # function to get held positions through API
    try:
        pos = api.get_position(symbol) # get position of symbol
        return pos # retrun position
    except:
        return False # return False if position does not exist

def sell(symbol, qty, price): # function to place sell order
    try: # try to submit sell order
        api.submit_order(
            symbol=symbol,
            qty=qty,
            limit_price=price,
            side='sell',
            type='limit',
            time_in_force='gtc'
        )
        update_position(symbol, "False") # update position in CSV file to indicate sell order was placed
    except:
        return False

def buy(symbol, qty): # function to place buy order
    try: # try to submit buy order
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='day'
        )
        update_position(symbol, "True") # update position in CSV file to indicate buy order was placed
    except:
        return False

def get_price(symbol): # function to get price of specific stock
    price_data = api.get_bars(symbol, tradeapi.TimeFrame.Minute, limit=1)
    return price_data

def truncate(number, digits) -> float: # function to truncate float decimal value
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


if(time_check and day_check): # if market is open
    selling() # place sell orders for all held positions
    buying() # place buy orders for all unheld positions
