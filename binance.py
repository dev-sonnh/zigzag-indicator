import requests
from datetime import datetime
import numpy as np

def get_time(t):
    return str(datetime.fromtimestamp(int(t) / 1000))

# market = 'BTCUSDT'
# tick_interval = '1m'
#
# url = 'https://api.binance.com/api/v3/klines?symbol='+market+'&interval='+tick_interval+'&limit=' + '1000'
# data = np.array(requests.get(url).json())

def get_data(market='BTCUSDT', tick_interval='1m'):
    url = 'https://api.binance.com/api/v3/klines?symbol=' + market + '&interval=' + tick_interval + '&limit=' + '1000'
    data = np.array(requests.get(url).json())
    date = np.array([get_time(row[0]) for row in data])
    open = np.array(data[:, 1])
    high = np.array(data[:, 2])
    low = np.array(data[:, 3])
    close = np.array(data[:, 4])

    return date, open.astype(float), high.astype(float), low.astype(float), close.astype(float)
