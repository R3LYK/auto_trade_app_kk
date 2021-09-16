import psycopg2, config
import alpaca_trade_api as tradeapi
from psycopg2 import extensions
import psycopg2.extras
import datetime as datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

barsets = api.get_barset(['MSFT, NFLX, AAPL, XOM'], 'minute')

for symbol in barsets:
    print(f"PROCESSING TICKER {symbol}")

    for bar in barsets[symbol]:
        print(bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v)
