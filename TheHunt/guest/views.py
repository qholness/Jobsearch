# from app import data, render_cols, search_titles
from flask import current_app, render_template,\
    request, redirect, url_for, flash, get_flashed_messages, g, session,\
    jsonify
from sqlalchemy import func
from TheHunt.db import db
# from TheHunt.socket import socketio
from TheHunt.models import Hit, SearchTerm, Location
from TheHunt.guest import guest
from TheHunt.guest import api
import utilities as utils
import locale
locale.setlocale( locale.LC_ALL, '' )


@guest.before_app_first_request
def log():
    session['REFRESH_RATE'] = current_app.config['REFRESH_RATE']


@guest.route('/')
def home():
    search_titles = api.get_search_terms().all()
    search_locations = api.get_locations().all()
    top_words = api.get_top_words(100).all()
    return render_template(
        'search.html',
        search_terms=search_titles,
        search_locations=search_locations,
        top_words=top_words)



@guest.route('/search', defaults={'page': 1})
@guest.route('/search/<int:page>')
def search(page=1):
    if request.args.get('search_term') is not None:
        # Update search args when a new search is performed
        session['search_args'] = request.args
    hits = api.get_hits()
    session['found_jobs'] = hits.count()
    hits = hits.paginate(page, per_page=current_app.config['PAGE_PER_REQUEST'], error_out=False)


    return render_template('results.html', hits=hits, locale=locale)
