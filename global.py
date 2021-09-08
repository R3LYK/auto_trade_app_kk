def pop_stock(connection, table=""):
    autocommit_orig = connection.autocommit_orig
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            
        )

