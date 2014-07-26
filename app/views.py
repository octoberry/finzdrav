# -*- coding: utf-8 -*-
from flask import jsonify
from pony.orm import db_session
from server import app


@app.route("/cards", methods=['GET', 'POST'])
@db_session
def cards():
    article = {'title': u'Тестовый заголовок'}
    return jsonify(article=article)
