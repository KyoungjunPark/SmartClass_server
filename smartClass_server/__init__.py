import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
		abort, render_template, flash, jsonify
import json
from contextlib import closing
import smartClass_server.views

app = Flask(__name__)

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'smartClass.db'),
    DEBUG = True,
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
))

app.config.from_object(__name__)
views.register_views(app)
