import psycopg2, asyncpg, config
import alpaca_trade_api as tradeapi
from psycopg2 import extensions
import psycopg2.extras
import time
import logging

connection = psycopg2.connect(config.connection)

# commented-out code below will auto-commit every insert. Good for debugging purposes
# bad practice other-wise. Google commit and rollback for more information

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows]

stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol) 
    stock_dict[symbol] = row['id']

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

# starting timer for debugging purposes
start = time.time()
# looping through symbols 200 at a time(API-limit)

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size] # moves to next iteration of chunk i.e. 1-200,201-400,401-600...

    barsets = api.get_barset(symbol_chunk, 'day')

    for symbol in barsets:
        print(f"processing symbol {symbol}")
    for bar in barsets[symbol]:
        stock_id = stock_dict[symbol]
        cursor.execute("""INSERT INTO stock_price
                    (stock_id, date_time, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) 
                    ON CONFLICT ON CONSTRAINT fk_stock DO NOTHING
                    """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
    
    # ends timer for debugging purposes
    end = time.time()
    print(f"Process ran for {end - start}.") # prints out time from start to end.


connection.commit()