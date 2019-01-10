from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from TheHunt.views import general
from TheHunt.guest import guest
from TheHunt.appadmin import appadmin
from TheHunt.auth import basic_auth
from flask_admin import Admin
from TheHunt.db import db
# from TheHunt.socket import socketio
from TheHunt.appadmin import api
# from TheHunt.dbadmin import dbadmin
from TheHunt.models import User, Location, SearchTerm
from TheHunt.ModelView import AppModelViewer
from werkzeug.security import generate_password_hash


def create_auth_user():
    if User.query.filter(User.username=='admin').first() is None:
        db.session.commit()
        pwd = 'fa0la99la28la3zlaa2wr'
        u = User(username='admin', password=generate_password_hash(pwd))
        db.session.add(u)
        db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object('TheHunt.config.Config')
    db.init_app(app)
    basic_auth.init_app(app)
    admin = Admin(app, 'admin', template_mode='bootstrap3')
    admin.add_view(AppModelViewer(Location, db.session))
    admin.add_view(AppModelViewer(SearchTerm, db.session))
    # socketio.init_app(app)
    app.register_blueprint(general)
    app.register_blueprint(guest)
    app.register_blueprint(appadmin)
    # socket = SocketIO(app)
    with app.app_context():
        try:
            create_auth_user()
        except:
            pass
    return app


# app.logger.info("Updating search term number")
# api.count_results_by_search_term()
# app.logger.info("Updating location number")
# api.count_results_by_location()
# app.logger.info("Updating company number")
# api.count_results_by_company()
# app.logger.info("Pruning old hits")
# api.prune_hits(app.config['PRUNE_HIT_DAYS'])
#

# server_name = "localhost.localhost:5000"
# server_name = "castironcofee.com:8080"
