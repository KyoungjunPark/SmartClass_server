# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from ..auth.commons import login_required
import demjson

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

		cur = g.db.execute('select email_user from phone_status where email_teacher = ? and screen_status = 1', [email])
		g.db.commit()

		data = []
		for row in cur:
			eamil_user = row[0]
			
			result = cur.fetchone()
			data.append({'email':email_user, 'status' : 'on'})


		return json.dumps(data), 200


