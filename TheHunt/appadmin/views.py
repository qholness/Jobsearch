from flask import Blueprint, url_for, redirect, render_template, session, request, flash
from functools import wraps
from TheHunt.db import db
from TheHunt.appadmin import appadmin
from TheHunt.appadmin import api
from TheHunt.models import Hit, SearchTerm,\
    Location, Company,User
from sqlalchemy import func
from multiprocessing import Process
from werkzeug.security import check_password_hash


@appadmin.before_request
def setup():
    pass


def login_user():
    session['loggedin'] = True

@appadmin.route('/loginuser')
def loginuser():
    username = request.args['username']
    password = request.args['password']
    user = User.query.filter(User.username == username).first()
    if user is None:
        flash("Couldn't find a user by that name")
    if check_password_hash(user.password, password) is True:
        login_user()
    return redirect(url_for('appadmin.login'))


@appadmin.route("/login")
def login():
    return render_template('admin/login.html')


def loggedin(func):
    wraps(func)
    def _decorator(*args, **kwargs):
        if session.get('loggedin') is True:
            return func(*args, **kwargs)
        return redirect('/admin/login')
    return _decorator


@appadmin.route("/")
@loggedin
def index():
    return render_template('admin/index.html')


@appadmin.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('appadmin.login'))
