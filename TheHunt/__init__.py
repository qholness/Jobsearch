from flask import Flask, redirect
from TheHunt.resources import api as rapi
from flask_sqlalchemy import SQLAlchemy
from TheHunt.views import general
from TheHunt.guest import guest
from TheHunt.appadmin import appadmin
from TheHunt.auth import basic_auth
from flask_admin import Admin
from TheHunt.db import db
from TheHunt.appadmin import api
from TheHunt.models import User, Location, SearchTerm
from TheHunt.ModelView import LocationViewer, SearchTermViewer
from werkzeug.security import generate_password_hash
from TheHunt.cel import celery
from TheHunt.config import Config


def create_auth_user():
    if User.query.filter(User.username=='admin').first() is None:
        db.session.commit()
        pwd = 'fa0la99la28la3zlaa2wr'
        u = User(username='admin', password=generate_password_hash(pwd))
        db.session.add(u)
        db.session.commit()


def create_app(config_name=None):
    app = Flask(__name__)
    if config_name:
        app.config.from_object(config_name)
    else:
        app.config.from_object('TheHunt.config.Config')
    db.init_app(app)
    basic_auth.init_app(app)
    rapi.init_app(app)
    celery.conf.update(app.config)
    admin = Admin(app, 'admin', template_mode='bootstrap3')
    admin.add_view(LocationViewer(Location, db.session))
    admin.add_view(SearchTermViewer(SearchTerm, db.session))
    app.register_blueprint(general)
    app.register_blueprint(guest)
    app.register_blueprint(appadmin)

    # Create auth_user
    with app.app_context():
        try: create_auth_user()
        except: pass
    return app

app = create_app()
