import psycopg2, config
import alpaca_trade_api as tradeapi
from psycopg2 import extensions
import psycopg2.extras

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

assets = api.list_assets()

for asset in assets:
    print(asset)
