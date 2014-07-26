# -*- coding: utf-8 -*-
from flask import jsonify
from pony.orm import db_session
from server import app


@app.route("/cards", methods=['GET', 'POST'])
@db_session
def cards():
    feed = [
            {
                'type': 'article',
                'id': 1,
                'title': u'Тестовый заголовок',
                'action_title': u'Прочесть',
                'url': 'http://ya.ru'
            },
            {
                'type': 'advice',
                'id': 1,
                'title': u'Тестовый заголовок',
                'action_title': u'ОК',
            },
            ]
    return jsonify(feed=feed)
