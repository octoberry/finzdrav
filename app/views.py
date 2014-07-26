# -*- coding: utf-8 -*-
from flask import jsonify
from pony.orm import db_session
from server import app


@app.route("/feed", methods=['GET', 'POST'])
@db_session
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

    items = advices + health + articles
    return jsonify(feed=items)


@app.route("/health", methods=['GET', 'POST'])
@db_session
def health():
    health = {'id': 1,
               'type': 'health',
               'temperature': 38.5,
               'description': u'Кажется у нас проблема',
               'action_title': u'Доктор, что мне делать?'}
    return jsonify(health=health)


@app.route("/action", methods=['GET', 'POST'])
@db_session
def action():
    advice = [{'id': 1,
               'type': 'advice',
               'img': 'heart',
               'description': u'Давай добавим жену',
               'cancel_title': u'Не хочу',
               'action_title': u'Да, хочу!'}]
    cards = advice
    return jsonify(cards=cards)