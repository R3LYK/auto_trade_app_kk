# I've been using this to query the db rather than opening pgadmin or psql

import psycopg2, config
import psycopg2.extras

connection = psycopg2.connect(config.connection)


cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("""SELECT * FROM stock_price""")

stocks = cursor.fetchall()

for stock_price in stocks:
    print(stock_price['open'])

cursor.close()

connection.close()