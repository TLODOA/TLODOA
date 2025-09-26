from begin.xtensions import *
from database import *

from routers.cookies import *

##
def register_app(app:object)->None:

    @app.route('/sign/display')
    def sign_display()->object:
        return flask.render_template('sign.html')

    @app.route('/login/display')
    def login_display()->object:
        return flask.render_template('login.html')

    ##
    @app.route('/sign/auth', methods=["POST"])
    def sign_auth()->object:
        if flask.request.method != "POST":
            return flask.redirect('/sign/display')

        user_name = flask.request.form["user_name"]
        user_password = flask.request.form["user_password"]

        #
        user = user_get(user_name)
        print(user)
        if not user:
            flask.session["message"]="<b>User is not defined</b>"
            return flask.redirect('/sign/display')

        if user[2] != user_password:
            flask.session["message"]="<b>User password incorrect</b>"
            return flask.redite

        #
        flask.session["message"]=""

        response = flask.make_response(flask.redirect('/'))
        cookie_define(response, 'user_name', user_name)

        return response

    @app.route('/login/auth', methods=["POST"])
    def login_auth()->object:
        if flask.request.method != "POST":
            return flask.redirect('/login/display')

        user_name = flask.request.form["user_name"]
        user_email = flask.request.form["user_email"]
        user_password = flask.request.form["user_password"]

        #
        if user_get(user_name):
            flask.session["message"] = "<b>This user already exist</b>"

            return flask.redirect('/login/display')


        flask.session["message"]=""

        user_insert(user_name, user_email, user_password)

        response = flask.make_response(flask.redirect('/'))
        cookie_define(response, 'user_name', user_name)

        return response

    @app.route('/logout/auth')
    def logout_auth()->object:
        response = flask.make_response(flask.redirect('/'))
        cookie_define(response, 'user_name', '', max_age=0)

        return response
