import psycopg2, config
import psycopg2.extras
from psycopg2 import extensions

##CURRENTLY POINTED AT NON-EXISTING DATABASE INSTANCE (I deleted the old one)

def create_tables():
    """ create tables in database"""
    commands = (
        """ CREATE TABLE IF NOT EXISTS stock (
        id SERIAL PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL
        )
        """,
        """CREATE TABLE IF NOT EXISTS stock_price ( 
        stock_id INTEGER,
        date_time VARCHAR NOT NULL,
        open NUMERIC NOT NULL, 
        high NUMERIC NOT NULL, 
        low NUMERIC NOT NULL, 
        close NUMERIC NOT NULL, 
        volume NUMERIC NOT NULL,
        PRIMARY KEY (stock_id, date_time),
        CONSTRAINT fk_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
        )
        """,
        """CREATE TABLE IF NOT EXISTS strategy (
        id SERIAL PRIMARY KEY, 
        name TEXT NOT NULL
        )
        """,
        """CREATE TABLE IF NOT EXISTS stock_strategy (
        stock_id INTEGER NOT NULL,
        strategy_id INTEGER NOT NULL,
        CONSTRAINT fk_strategy FOREIGN KEY (stock_id) REFERENCES stock (id),
        CONSTRAINT fk_strategy_id FOREIGN KEY (strategy_id) REFERENCES strategy (id)
        )
        """,
        """CREATE INDEX ON stock_price (stock_id, date_time DESC)
        """)


    connection = psycopg2.connect(database=config.DB_NAME, 
                                host=config.DB_HOST, 
                                user=config.DB_USER, 
                                password=config.DB_PASS, 
                                port=config.DB_PORT)
    try:
        cursor = connection.cursor()

        for command in commands:
            cursor.execute(command)
            print("tables have been created")
        cursor.close()

        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        if connection is not None:
            connection.close()

if __name__ == '__main__':
    create_tables()