import sqlite3, config

connection = sqlite3.connect(config.DB_FILE)

cursor = connection.cursor()

#creates db for stocks/symbols
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL
    )
""")

#Creates db for stock price
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

# Creates strategy. Each strat has unique id, name
cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategy (
        id INTEGER PRIMARY KEY, 
        name NOT NULL
    )
""")

# references stock in strategy (will have row for each stock being used w/strat)
# Is foreign key telling the database to populate from relational db?
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_strategy (
        stock_id INTEGER NOT NULL,
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
        FOREIGN KEY (strategy_id) REFERENCES strategy (id)
    )
""")

# inserts name,value into strategies
strategies = ['opening_range_breakout','opening_range_breakdown']

for strategy in strategies:
    cursor.execute("""
        INSERT INTO strategy (name) VALUES (?)
    """,(strategy,))

connection.commit()