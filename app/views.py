# -*- coding: utf-8 -*-
from __future__ import division
import datetime
from dateutil.relativedelta import relativedelta
from flask import jsonify, request
from app import calculus
from app.elastic import get_bar_stats, get_mcdonalds_stats
from server import app


def get_temperature():
    start_date = app.config['START_DATE']
    end_date = datetime.date.today()
    equability = [calculus.costs_equability(date_from=datetime.datetime(start_date.year, m, 1),
                                        date_to=datetime.datetime(start_date.year, m + 1, 1)) for m in
              range(start_date.month,
                    end_date.month)]
    score1 = len(filter(lambda x: x > app.config['EQUABILITY_LIMIT'], equability)) / len(equability)

    balance = [calculus.balance(date_from=datetime.datetime(start_date.year, m, 1),
                                date_to=datetime.datetime(start_date.year, m + 1, 1)) for m in
               range(start_date.month,
                     end_date.month)]

    score2 = len(filter(lambda x: x < 0, balance)) / len(balance)

    score = (score1 + score2) / 2
    temperature = (app.config['TEMPERATURE_MAX'] - app.config['TEMPERATURE_NORMAL']) * score + \
                  app.config['TEMPERATURE_NORMAL']
    return temperature


@app.route("/health", methods=['GET', 'POST'])
def health():
    temp = get_temperature()
    if temp < 37:
        health = {'id': 1,
                  'type': 'health',
                  'temperature': temp,
                  'description': u'Все отлично',
                  'action_title': u'Ок'}
    else:
        health = {'id': 1,
                  'type': 'health',
                  'temperature': temp,
                  'description': u'Твои расходы неравномерны. В некоторых месяцах твои расходы привысили доходы.',
                  'action_title': u'Доктор, что мне делать?'}
    return jsonify(health=health)


@app.route("/action", methods=['GET', 'POST'])
def action():
    card_id = request.args.get('id')
    card_type = request.args.get('type')
    cards = {}

    if card_type == 'health' and card_id == '1':
        advice = [{
                      'id': 1,
                      'type': 'advice',
                      'img': 'heart',
                      'description': u'Давай добавим жену',
                      'cancel_title': u'Не хочу',
                      'action_title': u'Да, хочу!'},
                  {
                      'id': 2,
                      'type': 'advice',
                      'img': 'money',
                      'description': U'Давай закроем овердрафт по кредитной карте',
                      'cancel_title': u'Не хочу',
                      'action_title': u'Да, хочу!'
                  }]
        cards = advice
    elif card_type == 'advice' and card_id == '2':
        bar_stats = get_bar_stats(date_from=app.config['START_DATE'], date_to=datetime.datetime.today())
        bar_stats_weekly = get_bar_stats(date_from=datetime.datetime.today() - relativedelta(weeks=1),
                                         date_to=datetime.datetime.today())
        quests = [{
                      'id': 1,
                      'type': 'quest',
                      'total': 10,
                      'description': u'Лимит по кредитной карты будешь закрывать за 10 месяцев',
                      'action_title': u'OK!',
                      'hint_template': u'Отлично, теперь ты закроешь кредит за $MONTH_NUMBER$ месяцев',
                      'options': [{
                                      'id': 1,
                                      'type': 'option',
                                      'description': u'Ты тратишь на обеды %d рублей, давай уменьшаем средний чек на '
                                                     u'100 рублей' % int(bar_stats['avg']),
                                      'total': -2}, {
                                      'id': 2,
                                      'type': 'option',
                                      'description': u'Ты был в ресторанах %d раз в прошлом месяце, давай сходим в '
                                                     u'ресторан на 1 раз меньше' % int(bar_stats_weekly['count']),
                                      'total': -1}],
                  }]
        cards = quests
    elif card_type == 'ruler' and card_id == '1':
        articles = [{'id': 1,
                     'type': 'article',
                     'img': 'good_wife',
                     'title': u'Отлично!',
                     'description': u'Ты улучшил свое финансовое здоровье. Продолжай в том же духе!',
                     'action_title': u'ОК'}]
        cards = articles
    return jsonify(cards=cards)


@app.route("/ruler", methods=['GET', 'POST'])
def ruler():
    bar_stats = get_bar_stats(date_from=app.config['START_DATE'], date_to=datetime.datetime.today())

    articles = [{'id': 1,
                 'type': 'article',
                 'img': 'bad_news',
                 'title': u'Плохие новости',
                 'description': u'Ты же обещал тратить меньше. Мы же договаривались о среднем чеке на обеды $VAR1$, '
                                u'а получилось $VAR2$.',
                 'action_title': u'Ладно',
                 'replacement': {
                     '$VAR1$': u'%d рублей' % (int(bar_stats['avg']) - 100),
                     '$VAR2$': u'900 рублей'
                 }}, {
                    'id': 2,
                    'type': 'article',
                    'img': 'wife_bad',
                    'title': u'О оу',
                    'description': u'Кажется твоя вторая половинка недовольна',
                    'action_title': u'Ой-ой'}]

    mcdonalds_stats_monthly = get_mcdonalds_stats(date_from=datetime.datetime.today() - relativedelta(weeks=2),
                                                  date_to=datetime.datetime.today() - relativedelta(weeks=1))
    step = int(mcdonalds_stats_monthly['sum'] / 100)
    ruler = [{'id': 1,
              'action_title': 'Я справлюсь!',
              'type': 'ruler',
              'description': u'Давай тогда сделаем задание проще. Уменьши свои затраты в день на FRESH CAFE.',
              'minimum_value': int(mcdonalds_stats_monthly['sum']) - step * 20,
              'maximum_value': int(mcdonalds_stats_monthly['sum']),
              'step': step,
              'value': int(mcdonalds_stats_monthly['sum']) - step * 20}]
    return jsonify(cards=articles + ruler)
