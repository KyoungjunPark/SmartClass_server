# -*- encoding utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
import random

join_blueprint = Blueprint('join', __name__)

@join_blueprint.route('/join_teacher', methods=['POST'])
def join_teacher():
	error_code = 200
	error_message = "Default"

	if request.method == 'POST':
		if valid_email(request.form['email']):
			cur = g.db.execute('insert into user(email, password, reg_type, name, sex_type) values(?,?,?,?,?)'
					,[request.form['email'],request.form['password']
						,1 ,request.form['name']
							, request.form.get('sex_type', type=int)])
			g.db.commit()
		else:
			error_code = 404
			error_message = "Already email is exist"
	else:
		error_code = 404
		error_message = "Wrong request type"

	if error_code == 200:
		create_codes(request.form['email'])
		return "ok"
	else:
		return error_message, error_code

@join_blueprint.route('/join_student', methods=['POST'])
def join_student():
	error_code = 200
	error_message = "Default"

	if request.method == 'POST':
		if valid_code(request.form['code']):
			if valid_email(request.form['email']):
				cur = g.db.execute('insert into user(email, password, reg_type, name, sex_type, code) values(?,?,?,?,?,?)'
						,[request.form['email'],request.form['password']
							,2 ,request.form['name']
								,int(request.form['sex_type']),request.form['code']])
				g.db.commit()
			else:
				error_code = 404
				error_message = "Already email is exist"
		else:
			error_code = 404
			error_message = "This code is incorrect"
	else:
		error_code = 404
		error_message = "Wrong request type"

	if error_code == 200:
		return "ok"
	else:
		return error_message, error_code

@join_blueprint.route('/join_parent', methods=['POST'])
def join_parent():
	error_code = 200
	error_message = "Default"

	if request.method == 'POST':
		if valid_code(request.form['code']):
			if valid_email(request.form['email']):
				cur = g.db.execute('insert into user(email, password, reg_type, name, sex_type, code) values(?,?,?,?,?,?)'
						,[request.form['email'],request.form['password']
							,3 ,request.form['name']
								,int(request.form['sex_type']),request.form['code']])
				g.db.commit()
			else:
				error_code = 404
				error_message = "Already email is exist"
		else:
			error_code = 404
			error_message = "This code is incorrect"
	else:
		error_code = 404
		error_message = "Wrong request type"

	if error_code == 200:
		return "ok"
	else:
		return error_message, error_code

def valid_code(code):
	if code[0] == 'P':
		cur = g.db.execute('select count(*) from teacherCode where parent_code = ?'
			,[code])
	elif code[0] == 'S':
		cur = g.db.execute('select count(*) from teacherCode where student_code = ?'
			,[code])
	else:
		return False

	g.db.commit()
	result = cur.fetchone()

	if result[0] == 0:
		return False
	else:
		return True


def valid_email(email):
	cur = g.db.execute('select count(*) from user where email = ?', [email])
	g.db.commit()
	result = cur.fetchone()

	if result[0] == 0:
		return True
	else:
		return False
def create_codes(email):

	student_code = "S"
	parent_code = "P"

	isCorrectCode = False
	while isCorrectCode == False:
		student_code += str(random.randrange(0, 10))
		student_code += str(random.randrange(0, 10))
		student_code += str(random.randrange(0, 10))
		student_code += str(random.randrange(0, 10))
		student_code += str(random.randrange(0, 10))

		parent_code += str(random.randrange(0, 10))
		parent_code += str(random.randrange(0, 10))
		parent_code += str(random.randrange(0, 10))
		parent_code += str(random.randrange(0, 10))
		parent_code += str(random.randrange(0, 10))

		cur = g.db.execute('select count(*) from teacherCode where student_code = ?'
				,[student_code])
		g.db.commit()
		student_result = cur.fetchone()
		cur = g.db.execute('select count(*) from teacherCode where parent_code = ?'
				,[parent_code])
		g.db.commit()
		parent_result = cur.fetchone()

		if student_result[0] == 0 and parent_result[0] == 0:
			isCorrectCode = True

	cur = g.db.execute('insert into teacherCode values(?, ?, ?)'
			,[email, student_code, parent_code])
	g.db.commit()

	return "ok"
