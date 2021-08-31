import sqlite3, config
import psycopg2
import alpaca_trade_api as tradeapi

conn = psycopg2.connect(database=config.db_name, user=config.user_name, password=config.db_pass, host=config.db_host, port=5432)

cursor = conn.cursor()
cursor.execute("""
    SELECT symbol, name FROM stock
""")
rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)
assets = api.list_assets()
for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, name, exchange) VALUES (?,?, ?)", (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)
conn.commit() 