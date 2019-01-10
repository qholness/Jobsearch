from TheHunt.auth import basic_auth
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException, Response


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class AppModelViewer(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException("Not authenticated.")
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())
