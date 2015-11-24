# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from ..auth.commons import login_required
import time.localtime()


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
		board_num = cur.fetchone()

		#time set
		now = time.localtime()
		time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday
				, now.tm_hour, now.tm_min, now.tm_sec)

		print("enroll time: " + time)
		if request.form['isSignNeed'] == "true":
			isSignNeed = 1
			cur = g.db.execute('insert into notice values(?,?,?,?,?,?,?)'
				,[request.form['email'], board_num, request.form['title']
					,request.form['content'], time, isSignNeed, sign])
	
		else:
			isSignNeed = 0
			cur = g.db.execute('insert into notice values(?,?,?,?,?,?,?)'
					,[request.form['email'], board_num, request.form['title']
						,request.form['content'], time, isSignNeed, null])		
		g.db.commit()


		return "ok", 200

