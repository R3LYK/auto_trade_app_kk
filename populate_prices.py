import psycopg2, asyncpg, config
import alpaca_trade_api as tradeapi
from psycopg2 import extensions
import psycopg2.extras

connection = psycopg2.connect(host=config.DB_LOCAL_HOST, 
                                database=config.DB_LOCAL_NAME, 
                                user=config.DB_LOCAL_USER, 
                                password=config.DB_LOCAL_PASSWORD)

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

symbols = []

stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

# looping through symbols 200 at a time(API-limit)
chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size] # moves to next iteration of chunk i.e. 1-200,201-400,401-600...

    barsets = api.get_barset(symbol_chunk, 'day')

    for symbol in barsets:
        print(f"processing symbol {symbol}")
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            cursor.execute("""
                INSERT INTO stock_price (stock_id, date_time, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))

connection.commit()