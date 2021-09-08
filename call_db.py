import psycopg2, config
import psycopg2.extras

connection = psycopg2.connect(host=config.DB_LOCAL_HOST, 
                            database=config.DB_LOCAL_NAME, 
                            user=config.DB_LOCAL_USER, 
                            password=config.DB_LOCAL_PASSWORD)


cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("""SELECT * FROM stock""")

stocks = cursor.fetchall()

for stock in stocks:
    print(stock['symbol'])

cursor.close()

connection.close()