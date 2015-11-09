# -*- encoding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for, session, g

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/test', methods=['GET'])
def test():
	return "Hello world"
