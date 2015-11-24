# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from ..auth.commons import login_required

code_blueprint = Blueprint('code', __name__)

@code_blueprint.route('/get_codes_teacher', methods=['POST'])
@login_required
def get_codes_teacher():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()

		email = result[0]

		cur = g.db.execute('select student_code, parent_code from teacherCode where email = ?'
		,[email])
		g.db.commit()
		result = cur.fetchone()

		codes = result[0] +"/"+ result[1]
		print(codes)
		return codes, 200

@code_blueprint.route('/get_codes', methods=['POST'])
@login_required
def get_codes():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()

		email = result[0]

		cur = g.db.execute('select code from user where email = ?'
				,[email])
		g.db.commit()
		result = cur.fetchone()

		code = result[0]
		print(code)

		return code, 200
