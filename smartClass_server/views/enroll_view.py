# -*- encoding: utf-8 -*-

from flask import Flask, Blueprint, request, render_template, send_from_directory, redirect, url_for, session, g
from ..auth.commons import login_required
from time import strftime
from werkzeug import secure_filename
import base64

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

@enroll_blueprint.route('/enroll_sign', methods=['POST'])
@login_required
def enroll_sign():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()

		email = result[0]

		print(len(request.form['sign_image']))

		fh = open("test.jpeg", "wb")
		fh.write(request.form['sign-image'].decode('base64'))
		fh.close()
		if file:
			filename = secure_filename(file.filename)

			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			return redirect(url_for('enroll_sign_file', filename=filename))

@enroll_blueprint.route('/enroll_sign_file', methods=['POST'])
def enroll_sign_file():
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


