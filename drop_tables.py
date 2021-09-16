import psycopg2, config
import psycopg2.extras
from psycopg2 import extensions
   

def drop_tables():
    """ drop tables in database"""
    commands = (
        """DROP TABLE IF EXISTS strategy CASCADE""",
        """DROP TABLE IF EXISTS stock_price CASCADE""",
        """DROP TABLE IF EXISTS stock_strategy CASCADE""",
        """DROP TABLE IF EXISTS tickers CASCADE""",
        """DROP TABLE IF EXISTS stock CASCADE""",
        )

    connection = psycopg2.connect(database=config.DB_NAME, 
                            host=config.DB_HOST, 
                            user=config.DB_USER, 
                            password=config.DB_PASS, 
                            port=config.DB_PORT)

    try:
        cursor = connection.cursor()

        for command in commands:
            cursor.execute(command)
            print("tables have been dropped")
        cursor.close()

        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        if connection is not None:
            connection.close()

if __name__ == '__main__':
    drop_tables()
    