# -*- coding: utf-8 -*-
from flask import jsonify
from pony.orm import db_session
from server import app


@app.route("/feed", methods=['GET', 'POST'])
@db_session
def feed():
    articles = [{'id': 1,
                'type': 'article',
                'title': u'Тестовый заголовок',
                'action_title': u'Прочесть',
                'url': 'http://ya.ru'}]
    advices = [{'id': 1,
               'type': 'advice',
               'title': u'Тестовый заголовок',
               'text': u'Тестовый текст',
               'action_title': u'Согласен'}]

    items = articles + advices
    return jsonify(feed=items)
