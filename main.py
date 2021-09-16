import psycopg2, config
import psycopg2.extras
from psycopg2 import extensions
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import datetime as datetime
from datetime import date


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    
    stock_filter = request.query_params.get('filter', False) #Fale - sets stock filter to stock
    connection = psycopg2.connect(host=config.DB_LOCAL_HOST, 
                                database=config.DB_LOCAL_NAME, 
                                user=config.DB_LOCAL_USER, 
                                password=config.DB_LOCAL_PASSWORD)

    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# NOW I THINK THERE IS AN ISSUE WITH THE TIME FORMATS WE'RE CALLING VS TIMVE FORMATS OF DATABASE

    if stock_filter == 'new_closing_highs':
        cursor.execute("""SELECT * FROM 
                    (
                    SELECT symbol, name, stock_id, MAX(close), date_time
                    FROM stock_price JOIN stock ON stock.id = stock_price.stock_id
                    WHERE date_time = '2021-9-7' 
                    GROUP BY stock.symbol, stock.name, stock_id, close, date_time
                    ORDER BY symbol
                    )
                    AS MyDerivedTable
                    WHERE date_time = %s
                    """), (date.today().isoformat(),) #calling date/time dynamically using imported datetime
    else:
        cursor.execute("""
            SELECT id, symbol, name FROM stock ORDER BY symbol
        """)

    rows = cursor.fetchall()
    
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})

@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol): #accepts a request and symbol
    connection = psycopg2.connect(host=config.DB_LOCAL_HOST, 
                            database=config.DB_LOCAL_NAME, 
                            user=config.DB_LOCAL_USER, 
                            password=config.DB_LOCAL_PASSWORD)

    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("""SELECT * FROM strategy
                """)
    strategies = cursor.fetchall()
    
    cursor.execute("""SELECT id, symbol, name FROM stock WHERE symbol = %s
                """, (symbol,))

    row = cursor.fetchone()
    
    cursor.execute("""SELECT * FROM stock_price WHERE stock_id = %s ORDER BY date_time DESC 
                """, (row['id'],))

    prices = cursor.fetchall()

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices, "strategies": strategies})

@app.post("/apply_strategy")
def apply_strategy(strategy_id: int=Form(...), stock_id: int = Form(...)):
    connection = psycopg2.connect(host=config.DB_LOCAL_HOST, 
                            database=config.DB_LOCAL_NAME, 
                            user=config.DB_LOCAL_USER, 
                            password=config.DB_LOCAL_PASSWORD)

    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("""
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (%s, %s)
    """, (stock_id, strategy_id))

    connection.commit()
    
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)

@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id):
    connection = psycopg2.connect(host=config.DB_LOCAL_HOST, 
                            database=config.DB_LOCAL_NAME, 
                            user=config.DB_LOCAL_USER, 
                            password=config.DB_LOCAL_PASSWORD)

    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("""
        SELECT id, name
        FROM strategy
        WHERE id = %s
    """,(strategy_id,))

    strategy = cursor.fetchone()

    cursor.execute("""
    SELECT symbol, name
    FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
    WHERE strategy_id = %s
    """,(strategy_id,))

    stocks = cursor.fetchall()

    return templates.TemplateResponse("strategy.html", {"request": request, "stocks": stocks, "strategy": strategy})