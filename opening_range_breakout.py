import sqlite3
import config
import alpaca_trade_api as tradeapi
import datetime as datetime

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id FROM strategy WHERE name = 'opening_range_breakout'
""")

strategy_id = cursor.fetchone()['id']  #I need to figure out why this works.

cursor.execute("""SELECT symbol, name
                FROM stock
                JOIN stock_strategy on stock_strategy.stock_id = stock.id
                WHERE stock_strategy.strategy_id = %s
                """, (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks] #he called this "list comprehension", it's new to me.

print(symbols)

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)