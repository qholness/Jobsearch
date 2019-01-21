"""Administrative Blueprint.

Used in database administration and update in conjunction with Celery
"""


from flask import Blueprint


appadmin = Blueprint('appadmin', __name__, url_prefix='/appadmin')


from . import views
