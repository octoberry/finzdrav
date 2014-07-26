# -*- coding: utf-8 -*-
import json
import urllib2
from flask import jsonify, request
from server import app


@app.route("/feed", methods=['GET', 'POST'])
def feed():
    health = [{'id': 1,
               'type': 'health',
               'temperature': 36.6,
               'description': u"Отлично, молодец, красавчик, продолжай в том же духе!",
               'action_title': u"Да, продолжаю!"}]
    articles = [{'id': 1,
                 'type': 'article',
                 'title': u'Тестовый заголовок',
                 'description': u'Тестовый текст',
                 'action_title': u'Прочесть',
                 'url': 'http://ya.ru'}]
    advices = [{'id': 1,
                'type': 'advice',
                'img': 'heart',
                'description': u'Давай добавим жену',
                'cancel_title': u'Не хочу',
                'action_title': u'Да, хочу!'}]

    items = health + advices + articles
    return jsonify(feed=items)


@app.route("/health", methods=['GET', 'POST'])
def health():
    health = {'id': 1,
              'type': 'health',
              'temperature': 38.5,
              'description': u'Кажется у нас проблема',
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
        quests = [{
                      'id': 1,
                      'type': 'quest',
                      'total': 10,
                      'description': u'Лимит по кредитной карты будешь закрывать за 10 месяцев',
                      'action_title': u'OK!',
                      'options': [{
                          'id': 1,
                          'type': 'option',
                          'description': u'Уменьшаем средний чек на 100 руб',
                          'total': -2},{
                          'id': 2,
                          'type': 'option',
                          'description': u'Ты был в барах 8 раз в прошлом месяце, давай сходим в бар на 1 раз меньше',
                          'total': -1}],
                  }]
        cards = quests
    return jsonify(cards=cards)


@app.route("/spend", methods=['GET', 'POST'])
def spend():
    # amount = get_spend('address_name:bar') + get_spend('address_name:cafe') + get_spend('address_name:restoran')
    amount = get_spend('*')
    return jsonify(bars=amount)


def get_spend(query):
    var = urllib2.urlopen("http://95.143.124.220:9200/hack/_search?q=%s" % query).read()
    hits = json.loads(var)
    print hits['hits']
    return sum(item['_source']['amount'] for item in hits['hits']['hits'])

