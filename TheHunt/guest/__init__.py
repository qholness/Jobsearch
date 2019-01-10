from flask import Blueprint


guest = Blueprint('guest', __name__, url_prefix='/guest')


from . import views
from . import data_api
