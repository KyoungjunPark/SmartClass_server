# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from ..auth.commons import login_required
import json
import os

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

		cur = g.db.execute('select reg_type, name, sex_type, profile_image from user where email = ?'
		,[email])
		g.db.commit()
		result = cur.fetchone()
		name = result[1]
		reg_type = result[0]
		sex_type = result[2]
		filename = result[3]
		if not os.path.exists('profile_images/'):
			os.makedirs('profile_images/')

		fh = open(filename, "rb")
		image_data = fh.read()
		profile_image = image_data.encode("base64")
		
		data = []
		data.append({'email' : email, 'name' : name, 'reg_type' : reg_type, 'sex_type' : sex_type, 'profile_image' : profile_image})

		return json.dumps(data), 200
