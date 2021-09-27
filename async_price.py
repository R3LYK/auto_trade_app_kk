import json
import requests
import aiohttp, asyncpg, asyncio
import datetime, time

async def write_to_db(connection, params):
    await connection.copy_to_table('stock_price', records=params)
    #await connection.executemultiple("""INSERT INTO stock_price (stock_id, date_time, open, high, low, close, volume, price)
    #                                  VALUES (%s, %s, %s, %s, %s, %s, %s)
    # 
    # """

async def get_price(pool, stock_id, url):
    try:
        async with pool.acquire() as connection:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    resp = await response.read()
                    response = json.loads(resp)
                    params = [(stock_id, datetime.datetime.fromtimestamp(bar['t'] / 1000.0, bar['o'], bar['h'], bar['l'], bar['c'], bar['v']))]
                    await write_to_db(connection, params)