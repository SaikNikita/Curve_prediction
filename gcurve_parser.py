import numpy as np
import pandas as pd
import requests
import apimoex
from tqdm import tqdm


def get_curve(startdate, enddate):
    # получение торговых дней бондового рынка через индекс RGBITR
    with requests.Session() as session:
        tradedays = apimoex.get_board_history(session, 'RGBITR', board='SNDX', engine='stock', market='index',
                                              start=startdate, end=enddate)
        tradedays = pd.DataFrame(tradedays)['TRADEDATE']

        # "2014-01-06" первый день публикации новой КБД
        tradedays = tradedays[tradedays >= "2014-01-06"]

    # получение кривой через API Мосбиржи
    i = 0
    t = ['0.25', '0.5', '0.75', '1', '2', '3', '5', '7', '10', '15', '20', '30']
    array = np.zeros([len(t), len(tradedays)])
    for d in tqdm(tradedays):

        try:
            data = requests.get(f'https://iss.moex.com/iss/engines/stock/zcyc.json?date={d}')
            curve = np.array(data.json()["yearyields"]['data'])[:, 3]
            array[:, i] = curve
            i += 1
        except:
            continue

    return pd.DataFrame(data=array.T, columns=t).set_index(pd.Index(pd.to_datetime(tradedays)))


def get_bonds(startdate, enddate):
    # получение торговых дней фондового рынка биржи через индекс RGBITR
    with requests.Session() as session:
        tradedays = apimoex.get_board_history(session, 'RGBITR', board='SNDX', engine='stock', market='index',
                                              start=startdate, end=enddate)
        tradedays = pd.DataFrame(tradedays)['TRADEDATE']

        # "2014-01-06" первый день публикации новой КБД
        tradedays = tradedays[tradedays >= "2014-01-06"]

    # получение кривой через API Мосбиржи
    data = pd.DataFrame()
    for d in tqdm(tradedays):

        try:
            req = requests.get(f'https://iss.moex.com/iss/engines/stock/zcyc.json?date={d}').json()
            data = pd.concat([data, pd.DataFrame(data=req["securities"]['data'], columns=req["securities"]['columns'])])
        except:
            continue

    return data


def nss_spot(b0, b1, b2, b3, tau1, tau2, t):
    Y = b0 + b1 * ((1 - np.exp(-t / tau1)) / (t / tau1)) + b2 * (
                ((1 - np.exp(-t / tau1)) / (t / tau1)) - np.exp(-t / tau1)) + b3 * (
                    ((1 - np.exp(-t / tau2)) / (t / tau2)) - np.exp(-t / tau2))
    return Y


def nss_forward(b0, b1, b2, b3, tau1, tau2, t):
    Y = b0 + b1 * np.exp(-t / tau1) + b2 * np.exp(-t / tau1) * t / tau1 + b3 * np.exp(-t / tau2) * t / tau2
    return Y