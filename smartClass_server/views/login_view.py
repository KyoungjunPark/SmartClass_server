# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
import os
import binascii

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
	error = None
	if request.method == 'POST':
		if valid_login(request.form['email'], request.form['password']):
			token = make_token()
			cur = g.db.execute('select count(*) from token where email = ?'
					,[request.form['email']])
			g.db.commit()
			result = cur.fetchone()
			if result[0] == 0:
				cur = g.db.execute('insert into token values(?,?)'
						, [request.form['email'],token])
			else:
				cur = g.db.execute('update token set token=? where email = ?'
				,[token, request.form['email']])
			g.db.commit()
			return token, 200
		else:
			return "This email or password is not correct!", 404

def valid_login(email, password):
	cur = g.db.execute('select count(*) from user where email= ? AND password= ?'
			,[email, password])
	g.db.commit()
	result = cur.fetchone()

	if result[0] == 0:
		return False
	else:
		return True

	
def make_token():
	return binascii.hexlify(os.urandom(12))
