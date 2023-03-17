import json
import pandas as pd
import config
from datetime import datetime
import time
import requests
import telegram
from decimal import Decimal
from typing import Union, Optional, Dict

from telegram.constants import ParseMode

def save_info_trade(data):
    with open('./assets/operations.json', 'w') as file:
        json.dump(data, file, indent=4)

def read_info_trade():
    with open('./assets/operations.json') as file:
        data = json.load(file)
    return data

def update_info_trade(field, new_data):
    old_data = read_info_trade()
    print(old_data)
    old_data['spot'][field].append(new_data)
    save_info_trade(old_data)

def get_klines_df(klines):
    df = pd.DataFrame(klines)
    df.closeTime = pd.to_datetime(df.closeTime, unit='ms').dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df.drop(['openTime','quoteAssetVolume', 'numTrades', 'takerBuyBaseAssetVolume','takerBuyQuoteAssetVolume', 'ignore'], axis=1)
    return df

def calculate_momentum(closes, periodo):
    if len(closes) < periodo:
        return None
    momentum = (float(closes[-1]) - float(closes[-periodo])) / float(closes[-periodo])
    return round(momentum,5)

def getTrendValues(klines_df, periodo_trend, periodo_momentum):
    df_trend = klines_df[-periodo_trend:]
    df_trend_first = df_trend["close"].astype(float).iloc[0]
    df_trend_end = df_trend["close"].astype(float).iloc[-1]
    diff = (df_trend_end - df_trend_first)
    _momentum = calculate_momentum(df_trend['close'].tolist(), periodo_momentum)
    return [diff, _momentum]

def calculate_sma_average(closes, periodos):
    sma_local = 0
    sum = 0
    for x in closes:
        sum = sum + float(x)
    sma_local = (sum / periodos)
    return float(sma_local)

def calculate_ema_average(closes, n=14):
    ema = []
    ema.append(calculate_sma_average(closes, n))
    #ema.append(closes[0])  # Usar el precio de cierre del período anterior como valor inicial
    k = 2 / (n + 1)
    #k = float('{:.2f}'.format(k))
    for i in range(1, len(closes)):
        ema.append((closes[i] * k) + (ema[i-1] * (1 - k)))
    ema_local = ema.pop()
    return ema_local


def calculate_ema_list(klines_df, emas, periodo_graph):
    for p in emas:
        k = 2 / (p + 1)
        ema = []
        closes = klines_df['close'].astype(float).tolist()
        first_ema = calculate_sma_average(closes, p)
        ema.append(first_ema)
        i = 1
        for price_close in klines_df.close:
            calc_ema = float((float(price_close) * k) + (ema[i-1] * (1 - k)))
            i = i + 1
            ema.append(float(calc_ema))
        col_name = f'ema_{p}'
        klines_df[col_name] = ema[:periodo_graph]
    return klines_df

def calculate_smas_list(klines_df, smas):
    for p in smas:
        sma_p = klines_df['close'].rolling(window=p).mean()
        col_name = f'sma_{p}'
        klines_df[col_name] = sma_p
    return klines_df


def GetBalanceAsset(_balance, trend):
    for data in _balance:
        if(data['asset'] == config.BASE_ASSET and trend == 'baja'):
            return float(data['free'])
        if(data['asset'] == config.QUOTE_ASSET and trend == 'alza'):
            return float(data['free'])


async def SendNotificationTelegram(msg):
    seconds = time.time() + 60
    date = datetime.fromtimestamp(seconds)
    bot = telegram.Bot(config.TELEGRAM_API)
    await bot.send_message(chat_id='@botsiachannel', text = msg,  parse_mode=ParseMode.HTML)

def round_step_size(quantity: Union[float, Decimal], step_size: Union[float, Decimal]) -> float:
    quantity = Decimal(str(quantity))
    valor_valido =float(quantity - quantity % Decimal(str(step_size)))
    return valor_valido