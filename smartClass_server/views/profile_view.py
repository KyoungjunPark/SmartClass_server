# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from ..auth.commons import login_required

profile_blueprint = Blueprint('profile', __name__)

@profile_blueprint.route('/get_profile', methods=['POST'])
@login_required
def get_profile():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email = result[0]

		cur = g.db.execute('select reg_type, name, sex_type from user where email = ?'
		,[email])
		g.db.commit()
		result = cur.fetchone()

		codes = email + "/" + result[1] + "/" + str(result[0]) + "/" + str(result[2])
		print(codes)
		
		return codes, 200

