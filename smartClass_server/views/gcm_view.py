# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from ..auth.commons import login_required
import os
from gcm import *
import json

API_KEY = "AIzaSyC8y5omsB8cuWPdJW44-fNnVd-ziuME_Bk"

gcm_blueprint = Blueprint('gcm', __name__)

@gcm_blueprint.route('/gcm', methods=['POST'])
@login_required
def gcm():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email = result[0]
		email_teacher = result[0]

		#check user type
		cur = g.db.execute('select reg_type, code from user where email = ?'
				,[email])
		g.db.commit()
		result = cur.fetchone()
		reg_type = result[0]
		code = result[1]

		if reg_type != 1:
			if code[0] == 'P':
				#case: parent
				cur = g.db.execute('select email from teacherCode where parent_code =?'
						,[code])
				g.db.commit()
				result = cur.fetchone()
				email_teacher = result[0]
			else:
				#case: student
				cur = g.db.execute('select email from teacherCode where student_code = ?'
						,[code])
				g.db.commit()
				result = cur.fetchone()
				email_teacher = result[0]
		
		if email != email_teacher:
			cur = g.db.execute('select count(*) from gcm_id where email_teacher = ? and email_user = ?' ,[email_teacher, email])
			g.db.commit()
			result = cur.fetchone()
			if result[0] == 0:
				cur = g.db.execute('insert into gcm_id values(?,?,?)'
						,[email_teacher, email,request.form['register_id']])
			else:
				cur = g.db.execute('update gcm_id set register_id = ? where email_teacher =? and email_user = ?' ,[request.form['register_id'], email_teacher,email])
			g.db.commit()

		return "ok", 200

@gcm_blueprint.route('/send_gcm', methods=['GET','POST'])
def send_gcm():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email = result[0]
	
		cur = g.db.execute('select register_id from gcm_id where email_teacher = ?'
				,[email])
		g.db.commit()

		gcm = GCM(API_KEY)
		data = {'board_type': request.form['board_type'], 'title': request.form['title']}
	
		reg_ids = []
		for row in cur:
			reg_ids.append(row[0])

		gcm.json_request(registration_ids=reg_ids, data=data)
		
	
	return "ok", 200
	
