# from app import data, render_cols, search_titles
from flask import current_app, render_template,\
    request, redirect, url_for, flash, get_flashed_messages, g, session,\
    jsonify
from sqlalchemy import func
from TheHunt.db import db
from TheHunt.resources import JobsApi, HitSearch
from TheHunt.models import Hit, SearchTerm, Location
from TheHunt.guest import guest
import utilities as utils
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')



@guest.before_app_first_request
def log():
    session['REFRESH_RATE'] = current_app.config['REFRESH_RATE']


@guest.route('/')
def home():
    API = HitSearch()
    return render_template(
        'search.html',
        search_terms=API.get_search_terms(),
        search_locations=API.get_locations())



@guest.route('/search', defaults={'page': 1})
@guest.route('/search/<int:page>')
def search(page=1):
    if request.args.get('search_term') is not None:
        # Update search args when a new search is performed
        session['search_args'] = request.args
    hits = HitSearch().get_hits()
    session['found_jobs'] = hits.count()
    hits = hits.paginate(page, per_page=current_app.config['PAGE_PER_REQUEST'], error_out=False)
    return render_template('results.html', hits=hits, locale=locale)


@guest.route('/applied')
def applied_to():
    return render_template(
        "applied.html",
        jobs=JobsApi().get_applied())


@guest.route('/interested')
def interested_in():
    return render_template(
        "interested.html",
        jobs=JobsApi().get_interested())


@guest.route('/ignored')
def ignored_jobs():
    return render_template(
        "ignored.html",
        jobs=JobsApi().get_ignored())


@guest.route('/interviewing')
def interview_jobs():
    return render_template(
        "interview.html",
        jobs=JobsApi().get_interviewing())


@guest.route('/offer')
def offer_jobs():
    return render_template(
        "offer.html",
        jobs=JobsApi().get_offers())
