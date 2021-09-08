'''import psycopg2, config

def
connection = psycopg2.connect(dbname=config.DB_NAME, 
                user=config.DB_USER, 
                password=config.DB_PASS, 
                host=config.DB_HOST)


cursor = connection.cursor()
cursor.execute(
connection.close()'''