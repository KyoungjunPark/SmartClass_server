# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from ..auth.commons import login_required
import demjson
import json

status_blueprint = Blueprint('status', __name__)

@status_blueprint.route('/screen_status', methods=['POST'])
@login_required
def screen_status():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email = result[0]

		cur = g.db.execute('select email_user from phone_status where email_teacher = ? and screen_status = 1 and isSend = 0', [email])
		g.db.commit()

		data = []
		for row in cur:
			email_user = row[0]
			cur = g.db.execute('update phone_status set isSend = 1 where email_user = ?'
					,[email_user])
			g.db.commit()

			result = cur.fetchone()
			data.append({'email': email_user, 'status' : 'on'})


		return json.dumps(data), 200


