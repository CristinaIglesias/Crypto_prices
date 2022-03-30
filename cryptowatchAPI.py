import cryptowatch as cw
from datetime import datetime, timedelta
import pandas as pd 
import matplotlib.pyplot as plt
import logging
from sktime.utils.plotting import plot_series



# Connecting Api rest 

bitcoin = cw.assets.get('btc')
print(bitcoin._http_response)
cw.api_key = "GRVV3GWWQ17XM8MGC37D"


# Get all Kraken markets
kraken = cw.markets.list("kraken")
# instruments 
coin = cw.instruments.get("XTZUSD")
# Returns market summary (last, high, low, change, volume)
prices_kraken = cw.markets.get("KRAKEN:XTZUSD", ohlc=True) # > Tezos-USD Ticket 

# Returns market last trades
cw.markets.get("KRAKEN:XTZUSD", trades=True)
# Return market candlestick info (open, high, low, close, volume) on some timeframes
#cw.markets.get("KRAKEN:XTZUSD", ohlc=True, periods=["4h", "1h", "1d"])

# For each Kraken market...
for market in kraken.markets:

    # Forge current market ticker, like KRAKEN:BTCUSD
    ticker = "{}:{}".format(market.exchange, market.pair).upper()
    # Request weekly candles for that market
    candles = cw.markets.get(ticker, ohlc=True, periods=["1w"])

    # Each candle is a list of [close_timestamp, open, high, low, close, volume, volume_quote]
    # Get close_timestamp, open and close from the most recent weekly candle
    close_ts, wkly_open, wkly_close = (
        candles.of_1w[-1][0],
        candles.of_1w[-1][1],
        candles.of_1w[-1][4],
    )

    # Compute market performance, skip if open was 0
    if wkly_open == 0:
        continue
    perf = (wkly_open - wkly_close) * 100 / wkly_open

    # If the market performance was 5% or more, print it
    if perf >= 5:
        open_ts = datetime.utcfromtimestamp(close_ts) - timedelta(days=7)
        print("{} gained {:.2f}% since {}".format(ticker, perf, open_ts))

TICKET = "XTZ"
TABLE = "candles_1h_"+TICKET
candles = cw.markets.get("KRANEN:XTZUSD"+TICKET, ohlc=True)

rows_list = []

for x in candles.of_1h:
  close_ts = datetime.utcfromtimestamp(x[0])
  open_value = x[1]
  high_value = x[2]
  low_value = x[3]
  close_value = x[4]
  volume_base = x[5]
  volume_quote = x[6]
  rows_list.append([TICKET, close_ts, open_value, high_value,
                   low_value, close_value, volume_base, volume_quote])
df = pd.Dataframe(rows_list, columns=["ticket", "close_ts", "open_value",
                  "high_value", "low_value", "close_value", "volume_value", "volume_quote"])
print(df)








