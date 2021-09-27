import psycopg2, config
import alpaca_trade_api as tradeapi
from psycopg2 import extensions
import psycopg2.extras
import time


try:
    connection = psycopg2.connect(config.connection)

    print("Connected to database successfully.")
    
except:
    print("Could not connect to database.")

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("""SELECT symbol, name FROM stock""")

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)
assets = api.list_assets()

# playing around with testing/read-out's
# should count the number of stocks. Time starts time.
num_stocks = len(symbols) #not working
start = time.time()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("""INSERT INTO stock (symbol, name, exchange) VALUES (%s, %s, %s)""", (asset.symbol, asset.name, asset.exchange))
    except psycopg2.Error as e:
        pass
        print(asset.symbol)           #if error, will print symbol where error occured
        print (e.pgerror)
# ends time
end = time.time()

print(f"Populate_stocks took {end - start} to finish. {num_stocks} stocks were added.")

connection.commit()

cursor.close() 

connection.close()