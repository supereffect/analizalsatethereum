import talib
import pandas as pd
import requests
import json
import time

# Binance API anahtarınızı yazın
api_key = "API_KEY"
secret_key = "SECRET_KEY"

# Ethereum fiyat verilerini indir
url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=90"
response = requests.get(url)
data = response.json()
prices = [x[1] for x in data["prices"]]

# veriyi pandas DataFrame olarak yükle
df = pd.DataFrame(prices)


# Exponential moving average hesapla
df['ema_fast'] = talib.EMA(df['prices'], timeperiod=8)
df['ema_slow'] = talib.EMA(df['prices'], timeperiod=21)

# tahminleri yap
df['position'] = None
df.loc[df['ema_fast'] > df['ema_slow'], 'position'] = 'long'
df.loc[df['ema_fast'] < df['ema_slow'], 'position'] = 'short'

# Binance üzerinden işlem yap
if df.iloc[-1]['position'] == 'long':
    # İşlem yapmak için gerekli parametreleri oluşturun
    params = {
        "symbol": "ETHUSDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": "1.0"
    }
    # İşlemi yap
    headers = {
        "X-MBX-APIKEY": api_key
    }
    endpoint = "https://api.binance.com/api/v3/order"
    res = requests.post(endpoint, headers=headers, json=params)
    print(json.loads(res.text))
elif df.iloc[-1]['position'] == 'short':
    # İşlem yapmak için gerekli parametreleri oluşturun
    params = {
        "symbol": "ETHUSDT",
        "side": "SELL",
        "type": "MARKET",
        "quantity": "1.0"
    }
    # İşlemi yap
    headers = {
        "X-MBX-APIKEY": api_key
    }
    endpoint = "https://api.binance.com/api/v3/order"
    res = requests.post(endpoint, headers=headers, json=params)
    print(json.loads(res.text))
else:
    print("Tahmin yapılamadı")