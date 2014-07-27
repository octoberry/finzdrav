# -*- coding: utf-8 -*-
__author__ = 'fuse'

import pandas as pd
import numpy as np
from scipy import integrate
from scipy.interpolate import interp1d
import os
from datetime import datetime

debit_trans_type = [585, 515, 670, 799, 736, 700, 703, 774, 777, 776, 677, 680, 508, 781, 689]
csv_path = os.path.dirname(os.path.abspath(__file__)) + '/../data/akulov.csv'
salary_csv_path = os.path.dirname(os.path.abspath(__file__)) + '/../data/salary_account.csv'

_data_cache = {}

def _load_data(path):
    if path not in _data_cache:
        _data_cache[path] = pd.read_csv(path)
    return _data_cache[path]

def _filter_costs(df):
    return df[df.trans_type.isin(debit_trans_type)]

def _filter_by_dates(df, date_from, date_to, date_column, to_ts):
    df = df[to_ts(date_to) >= df[date_column]]
    return df[df[date_column] >= to_ts(date_from)]

def _get_costs_by_dates(date_from, date_to):
    df = _load_data(csv_path)
    df = _filter_costs(df)
    return _filter_by_dates(df, date_from, date_to, 'creation_timestamp', lambda x: int(x.strftime('%s')))

def _calc_equability_by_sums(df):
    avg = np.mean(df.amount)
    cnt = len(df.amount)
    ideal = lambda x: x * avg
    intq_max = integrate.quad(ideal, 0, cnt)

    burn_up = [sum(df.amount[0:i]) for i in xrange(0, cnt+1)]
    real = interp1d(range(0, cnt+1), burn_up)
    diff = lambda x: abs(ideal(x) - real(x))
    intq = integrate.quad(diff, 0, cnt)
    return intq[0] / intq_max[0]

def costs_equability(date_from, date_to):
    """
    Вычисляет равномерность сумм расходов по дням в указанном диапозоне дат
    """
    df = _get_costs_by_dates(date_from, date_to)
    df.insert(len(df.columns), 'date', df.creation_timestamp.map(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d')))
    df = df.pivot_table(['amount'], ['date'], aggfunc='sum')
    return _calc_equability_by_sums(df)

def income_sum(date_from, date_to):
    df = _load_data(salary_csv_path)
    df = _filter_by_dates(df, date_from, date_to, 'Дата операции', lambda x: x.strftime('%Y-%m-%d'))
    return sum(df['Приход'])

def costs_sum(date_from, date_to):
    df = _get_costs_by_dates(date_from, date_to)
    return sum(df['amount'])

def balance(date_from, date_to):
    income = income_sum(date_from, date_to)
    costs = costs_sum(date_from, date_to)
    return income - costs


if __name__ == "__main__":
    date_from = datetime(2014, 5, 1)
    date_to = datetime(2014, 6, 1)
    print costs_equability(date_from, date_to)
    print balance(date_from, date_to)
