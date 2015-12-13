# -*- encoding: utf-8 -*-

from flask import Flask, Blueprint, request, render_template, send_from_directory, redirect, url_for, session, g
from ..auth.commons import login_required
from time import strftime
from werkzeug import secure_filename
import base64
import os


SIGN_UPLOAD_FOLDER = 'sign_images/'
PROFILE_UPLOAD_FOLDER = 'profile_images/'
MEMORY_UPLOAD_FOLDER = 'memory_images/'

enroll_blueprint = Blueprint('enroll', __name__)

@enroll_blueprint.route('/enroll_notice', methods=['POST'])
@login_required
def enroll_notice():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email = result[0]

		cur = g.db.execute('select count(*) from notice where email = ?'
		,[email])
		g.db.commit()
		result = cur.fetchone()

	 	board_num = result[0]
		
		#time set
		now = strftime("%Y/%m/%d %H:%M")

		print("time :" + now)
		if request.form['isSignNeed'] == "true":
			isSignNeed = 1
		else:
			isSignNeed = 0
			
		if request.form['isImportant'] == "true":
			isImportant = 1
		else:
			isImportant = 0

		cur = g.db.execute('insert into notice values(?,?,?,?,?,?,?)'
				,[email, board_num, request.form['title']
					,request.form['content'], now, isSignNeed, isImportant])		
		g.db.commit()
		
		return "ok", 200
		#return redirect(url_for('gcm.send_gcm',board_type="notice"
		#	,email=email,title=request.form['title']))

@enroll_blueprint.route('/enroll_assignment', methods=['POST'])
@login_required
def enroll_assignment():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()

		email = result[0]

		cur = g.db.execute('select count(*) from assignment where email = ?'
		,[email])
		g.db.commit()
		result = cur.fetchone()

		board_num = result[0]
		
		#time set
		now = strftime("%Y/%m/%d %H:%M")

		print("time :" + now)
		if request.form['isImportant'] == "true":
			isImportant = 1
		else:
			isImportant = 0

		cur = g.db.execute('insert into assignment values(?,?,?,?,?,?,?,?)'
				,[email, board_num, request.form['title']
					,request.form['content'], now, request.form['start_date']
					,request.form['end_date'], isImportant])		
		g.db.commit()

		return "ok", 200
		#return redirect(url_for('gcm.send_gcm',board_type="assignment"
		#	,email=email,title=request.form['title']))

@enroll_blueprint.route('/enroll_sign', methods=['POST'])
@login_required
def enroll_sign():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email_parent = result[0]

		cur = g.db.execute('select code from user where email = ?'
				,[email_parent])
		g.db.commit()
		result = cur.fetchone()
		code = result[0]

		cur = g.db.execute('select email from teacherCode where parent_code = ?'
				,[code])
		g.db.commit()
		result = cur.fetchone()
		email_teacher = result[0]
		
		board_num = int(request.form['num'])

		#create sign image file
		filename = SIGN_UPLOAD_FOLDER + email_teacher + "_" + email_parent + "_" + str(board_num) + ".jpeg"
		
		if not os.path.exists(SIGN_UPLOAD_FOLDER):
			os.makedirs(SIGN_UPLOAD_FOLDER)

		fh = open(filename, "wb")
		fh.write(request.form['sign_image'].decode("base64"))
		fh.close()

		#insert info to sign table
		cur = g.db.execute('insert into sign values(?,?,?,?)'
				,[email_teacher, board_num, email_parent, filename])
		g.db.commit()
		
		return "ok", 200

@enroll_blueprint.route('/enroll_profile_image', methods=['POST'])
@login_required
def enroll_profile_image():
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email = result[0]

		#create profile image file
		filename = PROFILE_UPLOAD_FOLDER + email + ".png"
		if not os.path.exists(PROFILE_UPLOAD_FOLDER):
			os.makedirs(PROFILE_UPLOAD_FOLDER)


		fh = open(filename, "wb")
		fh.write(request.form['profile_image'].decode("base64"))
		fh.close()

		cur = g. db.execute('update user set profile_image =? where email = ?'
				,[filename, email])
		g.db.commit()

		return "ok", 200

@enroll_blueprint.route('/enroll_memory', methods=['POST'])
@login_required
def enroll_memory():
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email = result[0]
		
		#board number
		cur = g.db.execute('select count(*) from memory where email = ?'
		,[email])
		g.db.commit()
		result = cur.fetchone()
	 	board_num = result[0]
		
		#time set
		now = strftime("%Y/%m/%d %H:%M")
		print("time :" + now)

		if request.form['image'] != "":
			#create sign image file
			filename = MEMORY_UPLOAD_FOLDER + email + "_" + str(board_num) + ".png"
			
			if not os.path.exists(MEMORY_UPLOAD_FOLDER):
				os.makedirs(MEMORY_UPLOAD_FOLDER)

			fh = open(filename, "wb")
			fh.write(request.form['image'].decode("base64"))
			fh.close()
			#insert info to sign table
			cur = g.db.execute('insert into memory values(?,?,?,?,?)'
					,[email, board_num, request.form['content'], filename, now])
		else:
			filename = None
			#insert info to sign table
			cur = g.db.execute('insert into memory(email, num, content, time) values(?,?,?,?)', [email, board_num, request.form['content'], now])
		
		g.db.commit()

	return "ok", 200
	#return redirect(url_for('gcm.send_gcm',board_type="memory"
	#		,email=email,title=request.form['content']))


@enroll_blueprint.route('/enroll_screen', methods=['POST'])
@login_required
def enroll_screen():
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

		cur = g.db.execute('select count(*) from phone_status where email_teacher = ? and email_user = ?', [email_teacher, email])
		g.db.commit()
		result = cur.fetchone()
		isRecordExist = result[0]

		if request.form['screen_status'] == 'on':
			print("screen on")
			if isRecordExist == 0:
				cur = g.db.execute('insert into phone_status(email_teacher, email_user, screen_status) values(?, ?,?)',[email_teacher, email, 1])
			else:
				cur = g.db.execute('update phone_status set screen_status = ? and isSend = ? where email_teacher = ? and email_user = ?', [1, 0, email_teacher, email])
			
		else:
			print("screen off")
			if isRecordExist == 0:
				cur = g.db.execute('insert into phone_status(email_teacher, email_user, screen_status) values(?,?,?)'
						,[email_teacher, email, 0])
			else:
				cur = g.db.execute('update phone_status set screen_status = ?, isSend = ? where email_teacher = ? and email_user = ?', [0,0, email_teacher, email])
		
		g.db.commit()
		return "ok", 200
	

