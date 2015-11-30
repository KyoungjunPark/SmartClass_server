# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from ..auth.commons import login_required
import demjson
import json

board_blueprint = Blueprint('board', __name__)

@board_blueprint.route('/board_notice', methods=['POST'])
@login_required
def board_notice():
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
				cur = g.db.execute('select email from teacherCode where parent_code = ?'
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

		cur = g.db.execute('select num, title, content, time, isSignNeed, isImportant from notice where email = ?', [email_teacher])
		g.db.commit()
		data = []
		for row in cur:
			cur = g.db.execute('select count(*) from sign where num = ? and email_teacher = ? and email_parent = ?', [row[0], email_teacher, email])
			g.db.commit()
			result = cur.fetchone()
			isSignFinished = result[0]
			data.append({ 'num' : row[0]
				, 'title' : row[1], 'content' : row[2]	
				, 'time' : row[3], 'isSignNeed' : row[4]
				, 'isImportant' : row[5], 'isSignFinished' : isSignFinished})
	
		print(json.dumps(data))

		return json.dumps(data), 200

@board_blueprint.route('/board_assignment', methods=['POST'])
@login_required
def board_assignment():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email = result[0]

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
				cur = g.db.execute('select email from teacherCode where parent_code = ?'
						,[code])
				g.db.commit()
				result = cur.fetchone()
				email = result[0]
			else:
				#case: student
				cur = g.db.execute('select email from teacherCode where student_code = ?'
						,[code])
				g.db.commit()
				result = cur.fetchone()
				email = result[0]

	
		cur = g.db.execute('select num, title, content, start_date, end_date, isImportant from assignment where email = ?', [email])
		g.db.commit()

		data = []
		for row in cur:
			data.append({ 'num' : row[0], 'title' : row[1]
				, 'content' : row[2], 'start_date' : row[3]
				, 'end_date' : row[4],  'isImportant' : row[5]})

		print(json.dumps(data))

		return json.dumps(data), 200

@board_blueprint.route('/board_sign', methods=['POST'])
@login_required
def board_sign():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email_teacher = result[0]

		num = request.headers.get('num')

		cur = g.db.execute('select email_parent, signImage from sign where email_teacher = ? and num = ?', [eamil_teacher, num])
		g.db.commit()

		data = []
		for row in cur:
			
			data.append({'email_parent': row[0], 'signImage' : image_url})


