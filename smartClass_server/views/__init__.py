#-*- encoding: utf-8 -*-

from login_view import login_blueprint
from join_view import join_blueprint
from code_view import code_blueprint
from profile_view import profile_blueprint
from enroll_view import enroll_blueprint
from board_view import board_blueprint
from images_view import images_blueprint
from gcm_view import gcm_blueprint
from status_view import status_blueprint

def register_views(app):
	app.register_blueprint(login_blueprint)
	app.register_blueprint(join_blueprint)
	app.register_blueprint(code_blueprint)
	app.register_blueprint(profile_blueprint)
	app.register_blueprint(enroll_blueprint)
	app.register_blueprint(board_blueprint)
	app.register_blueprint(images_blueprint)
	app.register_blueprint(gcm_blueprint)
	app.register_blueprint(status_blueprint)
