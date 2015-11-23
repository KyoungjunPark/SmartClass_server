import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
		abort, render_template, flash, jsonify, send_file
import json
from contextlib import closing
import views

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

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

#GET communication test
@app.route('/db_test', methods=['GET'])
def test_GET():
	g.db.execute('insert into user values(?, ?, ?, ?, ?)'
			, [request.args.get('email'), request.args.get('password')
				, request.args.get('reg_type'), request.args.get('name')
				, request.args.get('sex_type')])
	g.db.commit()
	return "good"
@app.route('/pic_test', methods=['GET'])
def pic_test():
	return send_file('static/hyojoo.jpeg', mimetype='image/jpeg')
