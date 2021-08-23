"""import config
import alpaca_trade_api as tradeapi

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

hourly_bars = api.polygon.historic_agg_v2('Z', 1, 'hour', _from='2020-10-02', to='2020-10-22')
five_minute_bars = api.polygon.historic_agg_v2('Z', 5, 'minute', _from='2020-10-02', to='2020-10-22')
minute_bars = api.polygon.historic_agg_v2('Z', 1, 'minute', _from='2020-10-02', to='2020-10-22')

for bar in hourly_bars:
    print(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)

for bar in five_minute_bars:
    print(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)

for bar in minute_bars:
    print(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)"""