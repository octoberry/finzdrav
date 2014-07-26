# -*- coding: utf-8 -*-
from flask import jsonify
from pony.orm import db_session
from server import app


@app.route("/feed", methods=['GET', 'POST'])
@db_session
def feed():

    health = [{'id': 1,
               'type': 'health',
               'temperature': 0.5,
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
               'title': u'Тестовый заголовок',
               'description': u'Тестовый текст',
               'action_title': u'Согласен'}]

    items = health + articles + advices
    return jsonify(feed=items)
