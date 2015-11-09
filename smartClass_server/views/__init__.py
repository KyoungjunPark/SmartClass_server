#-*- encoding: utf-8 -*-

from test_view import test_blueprint

def register_views(app):
	app.register_blueprint(test_blueprint)
