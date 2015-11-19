#-*- encoding: utf-8 -*-

from login_view import login_blueprint
#from join_view import join_blueprint

def register_views(app):
	app.register_blueprint(login_blueprint)
	#app.register_blueprint(join_blueprint)
