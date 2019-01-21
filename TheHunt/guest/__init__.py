"""Blueprint for Guests (i.e., anyone who wants to view the page)
Sends and retrieves data for querying database
"""

from flask import Blueprint


guest = Blueprint('guest', __name__, url_prefix='/guest')


from . import views
