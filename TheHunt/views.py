from flask import Blueprint, redirect, url_for, current_app


general = Blueprint('general', __name__, url_prefix='/')


@general.route('/')
def index():
    return redirect(url_for('guest.home'))
