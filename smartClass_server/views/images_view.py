# -*- encoding: utf-8 -*-

from flask import Flask, Blueprint, request, render_template, send_from_directory, redirect, url_for, session, g, send_file
from ..auth.commons import login_required
import json

images_blueprint = Blueprint('images', __name__)

@images_blueprint.route('/images/signs', methods=['POST'])
@login_required
def images_signs():
	if request.method == 'POST':
		cur = g.db.execute('select email from token where token = ?'
				,[request.headers.get('token')])
		g.db.commit()
		result = cur.fetchone()
		email_teacher = result[0]

		board_num = request.form['num']


		cur = g.db.execute('select email_parent, signImage from sign where email_teacher = ? and num = ?', [email_teacher, board_num])
		g.db.commit()
		data = []
		for row in cur:
			fh = open(row[1], "rb")
			image_data = fh.read()
			sign_image = image_data.encode("base64")
			
			data.append({'email_parent' : row[0], 'sign_image' : sign_image})

		return json.dumps(data), 200
