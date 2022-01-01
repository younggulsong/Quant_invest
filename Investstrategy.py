import pyupbit
import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import time
import investpy


def stock_back_day(df, k):
    # df = pyupbit.get_daily_ohlcv_from_base(ticker,base=24)
    수수료율 = 0.0015
    df['매수기준가'] = df['open'] + k * (df['high'].shift(1) - df['low'].shift(1))
    status = 0  # 미보유는 0, 보유는 1

    df['당주수익률'] = 1.
    df['누적수익률'] = 1.
    df['기본수익률'] = df['close'] / df['close'][0]

    for i, date in enumerate(df.index):
        day_1 = df.index[i-1]
        if i < 1:  # 초기 1일은 전주가 없으므로 거래 제외
            continue
        if status == 0:
            if df.loc[date, 'high'] > df.loc[date, '매수기준가']:
                df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, '매수기준가']
                df.loc[date, '누적수익률'] = df.loc[day_1, '누적수익률'] * df.loc[date, '당주수익률']
                status = 1
                continue
            else:
                df.loc[date, '당주수익률'] = 1.
                df.loc[date, '누적수익률'] = df.loc[day_1, '누적수익률'] * df.loc[date, '당주수익률']
                continue

        if status == 1:
            if df.loc[date, 'high'] > df.loc[date, '매수기준가']:
                df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, '매수기준가']
                df.loc[date, '누적수익률'] = df.loc[day_1, '누적수익률'] * df.loc[date, '당주수익률']
                status = 0
                continue
            else:
                df.loc[date, '당주수익률'] = 1
                df.loc[date, '누적수익률'] = df.loc[day_1, '누적수익률'] * df.loc[date, '당주수익률']
                continue

    return df  # df, 매수비율, 승률, monthly cagr, mdd, 200일 변동률


def stock_back_day_long(df, k):
    # df = pyupbit.get_daily_ohlcv_from_base(ticker,base=24)
    수수료율 = 0.0015
    df['매수기준가'] = df['open'] + k * (df['high'].shift(1) - df['low'].shift(1))
    status = 0  # 미보유는 0, 보유는 1

    df['당주수익률'] = 1.
    df['누적수익률'] = 1.
    df['기본수익률'] = df['close'] / df['close'][0]

    for i, date in enumerate(df.index):
        week_1 = df.index[i-1]
        if i < 1:  # 초기 1일은 전주가 없으므로 거래 제외
            continue
        if status == 0:  # 보유 안했을 때 변동성 돌파에 따라 매수, 매수하고 이익을 보면 계속 보유
            if df.loc[date, 'high'] > df.loc[date, '매수기준가']:
                df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, '매수기준가']
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                if df.loc[date, '당주수익률'] > 1.:
                    print(df.loc[date, '당주수익률'])
                    status = 1
                continue
            else:
                df.loc[date, '당주수익률'] = 1.
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                continue

        if status == 1:  #
            df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, 'open']
            df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
            if df.loc[date, '당주수익률'] < 1:
                status = 0
                continue
            else:
                continue

    return df  # df, 매수비율, 승률, monthly cagr, mdd, 200일 변동률


def stock_back_day_long_ts(df, k):
    # df = pyupbit.get_daily_ohlcv_from_base(ticker,base=24)
    수수료율 = 0.0015
    df['매수기준가'] = df['open'] + k * (df['high'].shift(1) - df['low'].shift(1))
    status = 0  # 미보유는 0, 보유는 1

    df['당주수익률'] = 1.
    df['누적수익률'] = 1.
    df['기본수익률'] = df['close'] / df['close'][0]

    for i, date in enumerate(df.index):
        week_1 = df.index[i-1]
        if i < 1:  # 초기 1일은 전주가 없으므로 거래 제외
            continue
        if status == 0:  # 보유 안했을 때 변동성 돌파에 따라 매수, 매수하고 이익을 보면 계속 보유
            if df.loc[date, 'high'] > df.loc[date, '매수기준가']:
                df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, '매수기준가']
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                if df.loc[date, '당주수익률'] > 1.:
                    print(df.loc[date, '당주수익률'])
                    status = 1
                continue
            else:
                df.loc[date, '당주수익률'] = 1.
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                continue

        if status == 1:  #
            ts = df.loc[week_1, 'open']  # ts를 전 주 시가로 설정
            if df.loc[date, 'low'] < ts:
                df.loc[date, '당주수익률'] = ts / df.loc[date, 'open']
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                status = 0
                continue
            df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, 'open']
            df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
            if df.loc[date, '당주수익률'] < 1:
                status = 0
                continue
            else:
                continue

    return df  # df, 매수비율, 승률, monthly cagr, mdd, 200일 변동률


def stock_back_week(df, k):
    # df = pyupbit.get_daily_ohlcv_from_base(ticker,base=24)
    수수료율 = 0.0015
    df['매수기준가'] = df['open'] + k * (df['high'].shift(1) - df['low'].shift(1))
    status = 0  # 미보유는 0, 보유는 1

    df['당주수익률'] = 1.
    df['누적수익률'] = 1.
    df['기본수익률'] = df['close'] / df['close'][0]

    for i, date in enumerate(df.index):
        day_1 = df.index[i-1]
        if i < 1:  # 초기 1일은 전주가 없으므로 거래 제외
            continue
        if status == 0:
            if df.loc[date, 'high'] > df.loc[date, '매수기준가']:
                df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, '매수기준가']
                df.loc[date, '누적수익률'] = df.loc[day_1, '누적수익률'] * df.loc[date, '당주수익률']
                status = 1
                continue
            else:
                df.loc[date, '당주수익률'] = 1.
                df.loc[date, '누적수익률'] = df.loc[day_1, '누적수익률'] * df.loc[date, '당주수익률']
                continue

        if status == 1:
            if df.loc[date, 'high'] > df.loc[date, '매수기준가']:
                df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, '매수기준가']
                df.loc[date, '누적수익률'] = df.loc[day_1, '누적수익률'] * df.loc[date, '당주수익률']
                status = 0
                continue
            else:
                df.loc[date, '당주수익률'] = 1
                df.loc[date, '누적수익률'] = df.loc[day_1, '누적수익률'] * df.loc[date, '당주수익률']
                continue

    return df  # df, 매수비율, 승률, monthly cagr, mdd, 200일 변동률


def stock_back_week_long(df, k):
    # df = pyupbit.get_daily_ohlcv_from_base(ticker,base=24)
    수수료율 = 0.0015
    df['매수기준가'] = df['open'] + k * (df['high'].shift(1) - df['low'].shift(1))
    status = 0  # 미보유는 0, 보유는 1

    df['당주수익률'] = 1.
    df['누적수익률'] = 1.
    df['기본수익률'] = df['close'] / df['close'][0]

    for i, date in enumerate(df.index):
        week_1 = df.index[i-1]
        if i < 1:  # 초기 1일은 전주가 없으므로 거래 제외
            continue
        if status == 0:  # 보유 안했을 때 변동성 돌파에 따라 매수, 매수하고 이익을 보면 계속 보유 (status=1)
            if df.loc[date, 'high'] > df.loc[date, '매수기준가']:
                df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, '매수기준가']
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                if df.loc[date, '당주수익률'] > 1.:
                    print(df.loc[date, '당주수익률'])
                    status = 1
                continue
            else:
                df.loc[date, '당주수익률'] = 1.
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                continue

        if status == 1:  #
            df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, 'open']
            df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
            if df.loc[date, '당주수익률'] < 1:
                status = 0
                continue
            else:
                continue

    return df  # df, 매수비율, 승률, monthly cagr, mdd, 200일 변동률


def stock_back_week_long_ts(df, k):
    # df = pyupbit.get_daily_ohlcv_from_base(ticker,base=24)
    수수료율 = 0.0015
    df['매수기준가'] = df['open'] + k * (df['high'].shift(1) - df['low'].shift(1))
    status = 0  # 미보유는 0, 보유는 1

    df['당주수익률'] = 1.
    df['누적수익률'] = 1.
    df['기본수익률'] = df['close'] / df['close'][0]

    for i, date in enumerate(df.index):
        week_1 = df.index[i-1]
        if i < 1:  # 초기 1일은 전주가 없으므로 거래 제외
            continue
        if status == 0:  # 보유 안했을 때 변동성 돌파에 따라 매수, 매수하고 이익을 보면 계속 보유
            if df.loc[date, 'high'] > df.loc[date, '매수기준가']:
                df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, '매수기준가']
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                if df.loc[date, '당주수익률'] > 1.:
                    print(df.loc[date, '당주수익률'])
                    status = 1
                continue
            else:
                df.loc[date, '당주수익률'] = 1.
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                continue

        if status == 1:  #
            ts = df.loc[week_1, 'open']
            # ts = (df.loc[week_1, 'open']+df.loc[week_1, 'close'])/2.
            if df.loc[date, 'low'] < ts:
                df.loc[date, '당주수익률'] = ts / df.loc[date, 'open']
                df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
                status = 0
                continue
            df.loc[date, '당주수익률'] = df.loc[date, 'close'] / df.loc[date, 'open']
            df.loc[date, '누적수익률'] = df.loc[week_1, '누적수익률'] * df.loc[date, '당주수익률']
            if df.loc[date, '당주수익률'] < 1:
                status = 0
                continue
            else:
                continue

    return df  # df, 매수비율, 승률, monthly cagr, mdd, 200일 변동률


def weekly_변동성_stoploss(coinname, k, 손절비, from_date, to_date):
    # 손절비는 default 0
    price = investpy.crypto.get_crypto_historical_data(crypto=coinname, from_date=from_date, to_date=to_date)
    price.columns = ['open', 'high', 'low', 'close', 'volume', 'currency']

    max_week = price.rolling(window=7)['high'].max()
    min_week = price.rolling(window=7)['low'].min()
    주당변동성 = max_week - min_week
    status = 0
    price['일일수익률'] = 1.
    매수기준가격 = 10000.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['주당변동성'] = 주당변동성
    price['매수기준가격'] = 'NAN'
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['pc_upper'] = price.rolling(window=5)['high'].max().shift(1)
    price['pc_below'] = price.rolling(window=5)['low'].min().shift(1)

    for i, date in enumerate(price.index):

        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())
        if i % 7 == 0:  # 일주마다 한번씩 매수기준가격 update 하고 매도
            매수기준가격 = price.loc[date, 'open'] + k * 주당변동성[date - datetime.timedelta(days=1)]
            price.loc[date, '매수기준가격'] = 매수기준가격
            status = 0  # 매주 첫날 매도로 시작
        price.loc[date, '매수기준가격'] = 매수기준가격

        if status == 0:  # 안산 상태이면 매수기준에 사거나, 아예 안사고 하루를 보내면 됨.
            if price.loc[date, 'high'] > 매수기준가격:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / 매수기준가격
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                status = 1
                continue
            else:
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

        if status == 1:  # 매수 상태 시
            if price.loc[date, 'low'] < 매수기준가격 * 손절비:  # 저가보다 매수기준가격이 일정비율 낮으면 손절 손절비는 반드시 1보다 작게
                price.loc[date, '일일수익률'] = 매수기준가격 * 손절비 / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                status = 0  # 손절하여 매도 상태 근데 일주일안에 다시 매수할 수도 있는데 ..
                continue
            else:  # 매수유지
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

    return price


def weekly_변동성_stoploss_long(coinname, k, from_date, to_date):
    # 손절비는 default 0
    price = investpy.crypto.get_crypto_historical_data(crypto=coinname, from_date=from_date, to_date=to_date)
    price.columns = ['open', 'high', 'low', 'close', 'volume', 'currency']

    max_week = price.rolling(window=7)['high'].max()
    min_week = price.rolling(window=7)['low'].min()
    주당변동성 = max_week - min_week
    status = 0
    price['일일수익률'] = 1.
    매수기준가격 = 10000.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['주당변동성'] = 주당변동성
    price['매수기준가격'] = 'NAN'
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['pc_upper'] = price.rolling(window=5)['high'].max().shift(1)
    price['pc_below'] = price.rolling(window=5)['low'].min().shift(1)

    for i, date in enumerate(price.index):

        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())
        if i % 7 == 0:  # 일주마다 한번씩 매수기준가격 update 하고 매도
            매수기준가격 = price.loc[date, 'open'] + k * 주당변동성[date - datetime.timedelta(days=1)]
            price.loc[date, '매수기준가격'] = 매수기준가격
            status = 0  # 매주 첫날 매도로 시작
        price.loc[date, '매수기준가격'] = 매수기준가격

        if status == 0:  # 안산 상태이면 매수기준에 사거나, 아예 안사고 하루를 보내면 됨.
            if price.loc[date, 'high'] > 매수기준가격:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / 매수기준가격
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                status = 1
                continue
            else:
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

        if status == 1:  # 매수 상태 시
            if price.loc[date, 'low'] < 매수기준가격:  # 저가보다 매수기준가격이 일정비율 낮으면 손절 손절비는 반드시 1보다 작게
                price.loc[date, '일일수익률'] = 매수기준가격 / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                status = 0  # 손절하여 매도 상태
                continue
            else:  # 매수유지
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

    return price


def weekly_변동성_MACD(filename, k, 손절비):
    price = pd.read_excel(filename)
    price.index = price['Date']
    del price['Date']
    max_week = price.rolling(window=7)['high'].max()
    min_week = price.rolling(window=7)['low'].min()
    주당변동성 = max_week - min_week
    status = 0
    price['일일수익률'] = 1.
    매수기준가격 = 10000.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['주당변동성'] = 주당변동성
    price['매수기준가격'] = 'NAN'
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['MACD'] = price['close'].rolling(window=12).mean() - price['close'].rolling(window=26).mean()
    price['MACD_signal'] = price['MACD'].rolling(window=9).mean()

    for i, date in enumerate(price.index):

        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())
        if i % 7 == 0:  # 일주마다 한번씩 매수기준가격 update 하고 매도
            매수기준가격 = price.loc[date, 'open'] + k * 주당변동성[date - datetime.timedelta(days=1)]
            price.loc[date, '매수기준가격'] = 매수기준가격
            status = 0  # 매주 첫날 매도로 시작
            if price.loc[date, 'MACD'] < price.loc[date, 'MACD_signal']:
                매수기준가격 = 1000000000.  # 사지마라

        price.loc[date, '매수기준가격'] = 매수기준가격

        if status == 0:  # 안산 상태이면 매수기준에 사거나, 아예 안사고 하루를 보내면 됨.
            if price.loc[date, 'high'] > 매수기준가격:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / 매수기준가격
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                status = 1
                continue
            else:
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

        if status == 1:
            if price.loc[date, 'low'] < 매수기준가격 * (1 - 손절비):  # 저가보다 매수기준가격이 일정비율 낮으면 손절
                price.loc[date, '일일수익률'] = 1 - 손절비
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                status = 0  # 손절하여 매도 상태
                continue
            else:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

    return price


def weekly_변동성_pc(filename):  # price channel과 관련된 전략
    price = pd.read_excel(filename)
    price.index = price['Date']
    del price['Date']
    max_week = price.rolling(window=7)['high'].max()
    min_week = price.rolling(window=7)['low'].min()
    주당변동성 = max_week - min_week
    status = 0
    price['일일수익률'] = 1.
    매수기준가격 = 10000.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['주당변동성'] = 주당변동성
    price['매수기준가격'] = 'NAN'
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['MACD'] = price['close'].rolling(window=12).mean() - price['close'].rolling(window=26).mean()
    price['MACD_signal'] = price['MACD'].rolling(window=9).mean()
    price['pc_upper'] = price.rolling(window=5)['high'].max().shift(1)
    price['pc_lower'] = price.rolling(window=5)['low'].min().shift(1)

    for i, date in enumerate(price.index):

        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())

        if status == 0:  # 안산 상태이면 high 값이 upper channel 보다 높을 때 upper channel로 구매
            if price.loc[date, 'high'] > price.loc[date, 'pc_upper']:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'pc_upper']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                status = 1
                continue
            else:
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

        if status == 1:  # 산 상태이면 low 값이 below channel 보다 높을 때 lower channel로 구매
            if price.loc[date, 'low'] < price.loc[date, 'pc_lower']:  # 저가보다 매수기준가격이 일정비율 낮으면 손절
                price.loc[date, '일일수익률'] = price.loc[date, 'pc_lower'] / price.loc[date, 'open'] * ((1 - 수수료율) ** 2)
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                status = 0  # 손절하여 매도 상태
                continue
            else:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

    return price


def weekly_변동성_pc_investpy(coinname, from_date, to_date, pc_upper_day, pc_lower_day,
                           sell_ratio):  # price channel과 관련된 전략

    price = investpy.crypto.get_crypto_historical_data(crypto=coinname, from_date=from_date, to_date=to_date)
    price.columns = ['open', 'high', 'low', 'close', 'volume', 'currency']

    수수료율 = 0.0015
    status = 0
    price['일일수익률'] = 1.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['진입당수익률'] = 1.
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['MACD'] = price['close'].rolling(window=12).mean() - price['close'].rolling(window=26).mean()
    price['MACD_signal'] = price['MACD'].rolling(window=9).mean()
    price['pc_upper'] = price.rolling(window=pc_upper_day)['high'].max().shift(1)
    price['pc_lower'] = price.rolling(window=pc_lower_day)['low'].min().shift(1)

    for i, date in enumerate(price.index):

        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())

        if status == 0:  # 안산 상태이면 high 값이 upper channel 보다 높을 때 upper channel로 구매
            if price.loc[date, 'high'] > price.loc[date, 'pc_upper']:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'pc_upper']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                진입가격 = price.loc[date, 'pc_upper']
                status = 1
                continue
            else:
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

        if status == 1:  # 산 상태이면 low 값이 below channel 보다 높을 때 lower channel로 판매
            sellprice = sell_ratio * price.loc[date, 'pc_lower'] + (1 - sell_ratio) * price.loc[
                date, 'pc_upper']  # upper와 lower의 중간값
            if price.loc[date, 'low'] < sellprice:
                price.loc[date, '일일수익률'] = sellprice / price.loc[date, 'open'] * ((1 - 수수료율) ** 2)
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '진입당수익률'] = sellprice / 진입가격 * ((1 - 수수료율) ** 2)
                status = 0  # 손절하여 매도 상태
                continue
            else:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

    return price


def weekly_변동성_pc_investpy_middlesell(coinname, from_date, to_date, pc_upper_day,
                                      pc_lower_day):  # price channel과 관련된 전략

    price = investpy.crypto.get_crypto_historical_data(crypto=coinname, from_date=from_date, to_date=to_date)
    price.columns = ['open', 'high', 'low', 'close', 'volume', 'currency']

    수수료율 = 0.0015
    status = 0
    price['일일수익률'] = 1.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['진입당수익률'] = 1.
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['MACD'] = price['close'].rolling(window=12).mean() - price['close'].rolling(window=26).mean()
    price['MACD_signal'] = price['MACD'].rolling(window=9).mean()
    price['pc_upper'] = price.rolling(window=pc_upper_day)['high'].max().shift(1)
    price['pc_lower'] = price.rolling(window=pc_lower_day)['low'].min().shift(1)

    for i, date in enumerate(price.index):

        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())

        if status == 0:  # 안산 상태이면 high 값이 upper channel 보다 높을 때 upper channel로 구매
            if price.loc[date, 'high'] > price.loc[date, 'pc_upper']:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'pc_upper']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                진입가격 = price.loc[date, 'pc_upper']
                status = 1
                continue
            else:
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

        if status == 1:  # 산 상태이면 low 값이 below channel 보다 높을 때 lower channel로 판매
            sellprice = 0.5 * price.loc[date, 'pc_lower'] + 0.5 * price.loc[date, 'pc_upper']  # upper와 lower의 중간값
            if price.loc[date, 'low'] < sellprice:
                price.loc[date, '일일수익률'] = sellprice / price.loc[date, 'open'] * ((1 - 수수료율) ** 2)
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '진입당수익률'] = sellprice / 진입가격 * ((1 - 수수료율) ** 2)
                status = 0  # 손절하여 매도 상태
                continue
            else:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

    return price


def pc_investpy_addup(coinname, from_date, to_date, pc_upper_day, pc_lower_day, sell_ratio=1):  # price channel과 관련된 전략

    price = investpy.crypto.get_crypto_historical_data(crypto=coinname, from_date=from_date, to_date=to_date)
    price.columns = ['open', 'high', 'low', 'close', 'volume', 'currency']

    수수료율 = 0.0015
    status = 0  # 0면 매도 상태 1이면 절반매수상태 2 이면 풀매수 상태
    price['일일수익률'] = 1.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['진입당수익률'] = 1.
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['MACD'] = price['close'].rolling(window=12).mean() - price['close'].rolling(window=26).mean()
    price['MACD_signal'] = price['MACD'].rolling(window=9).mean()
    price['pc_upper'] = price.rolling(window=pc_upper_day)['high'].max().shift(1)
    price['pc_lower'] = price.rolling(window=pc_lower_day)['low'].min().shift(1)
    price['투자계좌'] = 0.5
    price['현금계좌'] = 0.5
    price['총자산'] = 1.
    price['총자산max대비손실'] = 0.
    추가진입가격 = 1.

    for i, date in enumerate(price.index):

        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())
        price.loc[day_1, '총자산max대비손실'] = -100 * (1 - price.loc[day_1, '총자산'] / price.loc[:day_1, '총자산'].max())

        if status == 0:  # 안산 상태이면 high 값이 upper channel 보다 높을 때 upper channel로 구매 반만큼 구매한다.
            if price.loc[date, 'high'] > price.loc[date, 'pc_upper']:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'pc_upper']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                진입가격 = price.loc[date, 'pc_upper']
                price.loc[date, '투자계좌'] = price.loc[date, '일일수익률'] * price.loc[day_1, '투자계좌']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                status = 1
                continue
            else:  # 매수기준 아니므로 수익없음, 일일수익률 = 1
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue

        if status == 1:  # 절반만 산 상태  몇퍼센트 이상 오르면 나머지 절반 add-up, 아니면 가지고 있거나 아니면 손절
            sellprice = sell_ratio * price.loc[date, 'pc_lower'] + (1 - sell_ratio) * price.loc[
                date, 'pc_upper']  # 손절가격 설정 일단은 pc_lower로 설정(sell_ratio=1)

            if price.loc[date, 'low'] < sellprice:  # sell price이하가 되면 자산을 팔고 총자산을 나누어 투자계좌와 현금계좌에 나누어 넣는다.
                price.loc[date, '일일수익률'] = sellprice / price.loc[date, 'open'] * ((1 - 수수료율) ** 2)
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '진입당수익률'] = sellprice / 진입가격 * ((1 - 수수료율) ** 2)
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, '일일수익률']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                price.loc[date, '투자계좌'] = 0.5 * price.loc[date, '총자산']
                price.loc[date, '현금계좌'] = 0.5 * price.loc[date, '총자산']
                status = 0  # 손절하여 매도 상태
                continue
            if price.loc[date, 'high'] > 1.1 * 진입가격 and price.loc[
                date, '현금계좌'] != 0.:  # 10% 상승시 add-up하여 나머지 현금 재산을 집어넣는다.
                추가진입가격 = 1.1 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + price.loc[day_1, '현금계좌'] * price.loc[
                                              date, 'close'] / 추가진입가격  # 현금계좌 추가 투입분에 일일 수익률추가
                price.loc[date, '현금계좌'] = 0.
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue
            else:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, '일일수익률']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue

    return price


def pc_investpy_addup_fine(coinname, from_date, to_date, pc_upper_day, pc_lower_day,
                           sell_ratio=1):  # price channel과 관련된 전략

    price = investpy.crypto.get_crypto_historical_data(crypto=coinname, from_date=from_date, to_date=to_date)
    price.columns = ['open', 'high', 'low', 'close', 'volume', 'currency']

    수수료율 = 0.0015
    status = 0  # 0면 매도 상태 1이면 절반매수상태 2 이면 풀매수 상태
    price['일일수익률'] = 1.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['진입당수익률'] = 1.
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['MACD'] = price['close'].rolling(window=12).mean() - price['close'].rolling(window=26).mean()
    price['MACD_signal'] = price['MACD'].rolling(window=9).mean()
    price['pc_upper'] = price.rolling(window=pc_upper_day)['high'].max().shift(1)
    price['pc_lower'] = price.rolling(window=pc_lower_day)['low'].min().shift(1)
    price['투자계좌'] = 0.2
    price['현금계좌'] = 0.8
    price['총자산'] = 1.
    price['총자산max대비손실'] = 0.
    최초투자금 = 1.
    add_count = 0

    for i, date in enumerate(price.index):
        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())
        price.loc[day_1, '총자산max대비손실'] = -100 * (1 - price.loc[day_1, '총자산'] / price.loc[:day_1, '총자산'].max())

        if status == 0:  # 안산 상태이면 high 값이 upper channel 보다 높을 때 upper channel로 구매 반만큼 구매한다.
            if price.loc[date, 'high'] > price.loc[date, 'pc_upper']:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'pc_upper']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                진입가격 = price.loc[date, 'pc_upper']
                price.loc[date, '투자계좌'] = price.loc[date, '일일수익률'] * price.loc[day_1, '투자계좌']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                status = 1
                add_count = 1
                continue
            else:  # 매수기준 아니므로 수익없음, 일일수익률 = 1
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue

        if status == 1:  # 절반만 산 상태  몇퍼센트 이상 오르면 나머지 절반 add-up, 아니면 가지고 있거나 아니면 손절
            sellprice = sell_ratio * price.loc[date, 'pc_lower'] + (1 - sell_ratio) * price.loc[
                date, 'pc_upper']  # 손절가격 설정 일단은 pc_lower로 설정(sell_ratio=1)

            if price.loc[date, 'low'] < sellprice:  # sell price이하가 되면 자산을 팔고 총자산을 나누어 투자계좌와 현금계좌에 나누어 넣는다.
                price.loc[date, '일일수익률'] = sellprice / price.loc[date, 'open'] * ((1 - 수수료율) ** 2)
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '진입당수익률'] = sellprice / 진입가격 * ((1 - 수수료율) ** 2)
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, '일일수익률']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                price.loc[date, '투자계좌'] = 0.2 * price.loc[date, '총자산']
                price.loc[date, '현금계좌'] = 0.8 * price.loc[date, '총자산']
                최초투자금 = price.loc[date, '투자계좌']
                status = 0  # 손절하여 매도 상태
                add_count = 0
                continue
            if price.loc[date, '현금계좌'] - 최초투자금 < 0:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, '일일수익률']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue
            if price.loc[date, 'high'] > 1.05 * 진입가격 and add_count == 1:  # 10% 상승시 20% add-up하여 넣는다.
                추가진입가격 = 1.05 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + 최초투자금 * price.loc[date, 'close'] / 추가진입가격
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌'] - 최초투자금
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                add_count = 2
                continue
            if price.loc[date, 'high'] > 1.1 * 진입가격 and add_count == 2:  # 20% 상승시 add-up하여 나머지 현금 재산을 집어넣는다.
                추가진입가격 = 1.1 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + 최초투자금 * price.loc[date, 'close'] / 추가진입가격
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌'] - 최초투자금
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                add_count = 3
                continue
            if price.loc[date, 'high'] > 1.15 * 진입가격 and add_count == 3:  # 30% 상승시 add-up하여 나머지 현금 재산을 집어넣는다.
                추가진입가격 = 1.15 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + 최초투자금 * price.loc[date, 'close'] / 추가진입가격
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌'] - 최초투자금
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                add_count = 4
                continue
            if price.loc[date, 'high'] > 1.2 * 진입가격 and add_count == 4:  # 40% 상승시 add-up하여 나머지 현금 재산을 집어넣는다.
                추가진입가격 = 1.2 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + 최초투자금 * price.loc[date, 'close'] / 추가진입가격
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌'] - 최초투자금
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                add_count = 5
                continue
            else:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, '일일수익률']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue

    return price


def yg_investpy_addup_fine(coinname, from_date, to_date, pc_upper_day, pc_lower_day,
                           sell_ratio=1):  # 진입은 변동성 돌파로, 나오는 것은 TS 지정으로 나오도록 하는 방법

    price = investpy.crypto.get_crypto_historical_data(crypto=coinname, from_date=from_date, to_date=to_date)
    price.columns = ['open', 'high', 'low', 'close', 'volume', 'currency']

    수수료율 = 0.0015
    status = 0  # 0면 매도 상태 1이면 절반매수상태 2 이면 풀매수 상태
    price['일일수익률'] = 1.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['진입당수익률'] = 1.
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    # price['MACD'] = price['close'].rolling(window=12).mean() - price['close'].rolling(window=26).mean()
    # price['MACD_signal'] = price['MACD'].rolling(window=9).mean()
    price['pc_upper'] = price.rolling(window=pc_upper_day)['high'].max().shift(1)
    price['pc_lower'] = price.rolling(window=pc_lower_day)['low'].min().shift(1)
    price['투자계좌'] = 0.2
    price['현금계좌'] = 0.8
    price['총자산'] = 1.
    price['총자산max대비손실'] = 0.
    최초투자금 = 1.
    add_count = 0
    손절비율 = 0.

    for i, date in enumerate(price.index):
        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = date - datetime.timedelta(days=1)

        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())
        price.loc[day_1, '총자산max대비손실'] = -100 * (1 - price.loc[day_1, '총자산'] / price.loc[:day_1, '총자산'].max())

        if status == 0:  # 안산 상태이면 pc_upper 돌파 시 구매
            # 변동성돌파가격 = price.loc[date,'open']+0.5*(price.loc[day_1,'high']-price.loc[day_1,'low'])
            if price.loc[date, 'high'] > price.loc[date, 'pc_upper']:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'pc_upper']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                진입가격 = price.loc[date, 'pc_upper']  # 진입한 기준가격을 기록
                진입일자 = date  # 진입한 기준 날짜를 기록
                price.loc[date, '투자계좌'] = price.loc[date, '일일수익률'] * price.loc[day_1, '투자계좌']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                status = 1
                add_count = 1
                continue
            else:  # 매수기준 아니므로 수익없음, 일일수익률 = 1
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue

        if status == 1:  # 절반만 산 상태  몇퍼센트 이상 오르면 나머지 절반 add-up, 아니면 가지고 있거나 아니면 손절
            if add_count == 1:
                sellprice = sell_ratio * price.loc[date, 'pc_lower'] + (1 - sell_ratio) * price.loc[
                    date, 'pc_upper']  # add up을 하지 않았으면 pc_lower로 손절
            else:
                sellprice = 진입가격 + 손절비율 * (
                            price.loc[진입일자:date, 'high'].max() - 진입가격)  # 손절가격 설정 진입가격 + 손절비율 * (최고가-진입가격)

            if price.loc[date, 'low'] < sellprice:  # sell price이하가 되면 자산을 팔고 총자산을 나누어 투자계좌와 현금계좌에 나누어 넣는다.
                price.loc[date, '일일수익률'] = sellprice / price.loc[date, 'open'] * ((1 - 수수료율) ** 2)
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '진입당수익률'] = sellprice / 진입가격 * ((1 - 수수료율) ** 2)
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, '일일수익률']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                price.loc[date, '투자계좌'] = 0.2 * price.loc[date, '총자산']
                price.loc[date, '현금계좌'] = 0.8 * price.loc[date, '총자산']
                최초투자금 = price.loc[date, '투자계좌']
                status = 0  # 손절하여 매도 상태
                add_count = 0
                continue
            if price.loc[date, '현금계좌'] - 최초투자금 < 0:  # 현금계좌 잔고가 부족하면 매매하지 않음.
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, '일일수익률']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue
            if price.loc[date, 'high'] > 1.1 * 진입가격 and add_count == 1:  # 10% 상승시 20% add-up하여 넣는다.
                추가진입가격 = 1.1 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + 최초투자금 * price.loc[date, 'close'] / 추가진입가격
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌'] - 최초투자금
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                add_count = 2
                손절비율 = 0.5
                continue
            if price.loc[date, 'high'] > 1.2 * 진입가격 and add_count == 2:  # 20% 상승시 add-up하여 나머지 현금 재산을 집어넣는다.
                추가진입가격 = 1.2 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + 최초투자금 * price.loc[date, 'close'] / 추가진입가격
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌'] - 최초투자금
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                add_count = 3
                손절비율 = 0.4
                continue
            if price.loc[date, 'high'] > 1.3 * 진입가격 and add_count == 3:  # 30% 상승시 add-up하여 나머지 현금 재산을 집어넣는다.
                추가진입가격 = 1.3 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + 최초투자금 * price.loc[date, 'close'] / 추가진입가격
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌'] - 최초투자금
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                add_count = 4
                손절비율 = 0.3
                continue
            if price.loc[date, 'high'] > 1.4 * 진입가격 and add_count == 4:  # 40% 상승시 add-up하여 나머지 현금 재산을 집어넣는다.
                추가진입가격 = 1.4 * 진입가격
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, 'close'] / price.loc[
                    date, 'open'] + 최초투자금 * price.loc[date, 'close'] / 추가진입가격
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌'] - 최초투자금
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                add_count = 5
                손절비율 = 0.2
                continue
            else:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '투자계좌'] = price.loc[day_1, '투자계좌'] * price.loc[date, '일일수익률']
                price.loc[date, '현금계좌'] = price.loc[day_1, '현금계좌']
                price.loc[date, '총자산'] = price.loc[date, '투자계좌'] + price.loc[date, '현금계좌']
                continue

    return price  # #


def turtle_trade(filename, k, 손절비):
    # 어떤 내용이 들어가야 하느냐?
    '''
    1. 매수타이밍 잡기
    2. 손절가 지정
    3. add-up 전략
    4. TS 전략
    이 포함되어야 함.

    2. 무슨
    :return:
    '''