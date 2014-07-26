# -*- coding: utf-8 -*-
from flask import Flask
from pony.orm import Database

app = Flask(__name__)
app.config.from_pyfile('../default_config.py')
app.config.from_pyfile('../config.py')

db = Database('postgres', app.config['DATABASE'])

from app import views