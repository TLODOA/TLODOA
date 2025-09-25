from begin.xtensions import *
from database import *

def register_app(app:object)->None:

    @app.before_request
    def before_request():
        if "user_name" in flask.request.cookies:
            flask.session["user_name"] = flask.request.cookies["user_name"]
            return

        flask.session.pop("user_name", None)

    @app.route('/')
    def index()->object:
        if not "user_name" in flask.session:
            return flask.redirect('/sign/display')

        return flask.render_template('index.html')
