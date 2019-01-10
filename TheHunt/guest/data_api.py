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


@guest.route('/api/jobcount')
def get_job_count():
    jobcount = Hit.query.with_entities(Hit.id).count()
    return jsonify(dict(jobs=jobcount))


@guest.route('/api/toplocations')
def get_top_locations():
    def cellify(x):
        return f"<tr><td>{x.city}</td>"\
            f"<td>{x.state}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"
    res = api.get_top_locations()
    if res.count() > 0:
        return "".join(list(map(cellify, res.all())))
    return"<p>No locations yet.</p>"


@guest.route('/api/topcompanies')
def get_top_companies():
    def cellify(x):
        return f"<tr><td>{x.name}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"
    res = api.get_top_companies_hiring(10)
    if res.count() > 0:
        return "".join(list(map(cellify, res.all())))
    return"<p>No companies yet.</p>"


@guest.route('/api/topsalaries')
def get_top_salaries():
    def cellify(x):
        return f"<tr><td>{x.text}</td>"\
            f"<td>${'{:,.0f}'.format(x.average_min_salary)}</td></tr>"
    res = api.get_top_salaries_by_search_term()
    if res.count() > 0:
        return "".join(list(map(cellify, res.all())))
    return"<p>No companies yet.</p>"


@guest.route('/api/searchtermcounts')
def get_top_search_terms():
    def cellify(x):
        return f"<tr><td>{x.search_term}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"
    res = api.get_results_by_search_term()
    if res.count() > 0:
        return "".join(list(map(cellify, res.all())))
    return"<p>No terms yet.</p>"


@guest.route('/api/topsearchcombinations')
def get_top_search_loc_combo():
    def cellify(x):
        return f"<tr><td>{x.searchterm}.{x.location}</td>"\
            f"<td>{'{:,.0f}'.format(x.total)}</td></tr>"
    res = api.get_top_search_combo()
    # if res is not None:
    #     res = list(get_results_combo_top_n(res))
    if res.count() > 0:
        return "".join(list(map(cellify, res.all())))
    return"<p>No terms yet.</p>"
