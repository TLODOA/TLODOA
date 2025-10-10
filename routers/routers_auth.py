from begin.xtensions import *
from begin import token

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
            return flask.jsonify({
                "message_error": "This user name is not defined"
            })

        if user[2] != user_password:
            return flask.jsonify({
                "message_error": "User password correct"
            })

        #
        # flask.session["message"]=""

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
            return flask.jsonify({
                "message_error": "User already defined"
            })


        # flask.session["message"]=""

        user_insert(user_name, user_email, user_password)

        response = flask.make_response(flask.redirect('/'))
        cookie_define(response, 'user_name', user_name)

        return response

    @app.route('/logout/auth')
    def logout_auth()->object:
        response = flask.make_response(flask.redirect('/'))
        cookie_define(response, 'user_name', '', max_age=0)

        return response

    ##
    @app.route('/email/token/generate', methods=['POST'])
    def email_token_generate()->object:
        if flask.request.method != 'POST':
            return flask.redirect(flask.request.referrer)
        
        #
        forms = flask.request.json
        user_email = forms["user_email"]

        #
        user_addr = flask.request.remote_addr
        userEmail = userEmailCode_get(ip=user_addr)

        if userEmail==None:
            return flask.jsonify({
                'message_error': "Something goes wrong"
            })

        if userEmail and len(userEmail):
            return flask.jsonify({
                "message_error": "You already receive the email code"
            })

        #
        code = token.token_email_generate()
        userEmail = userEmailCode_insert(token=code, user_name=None, ip=user_addr, email=user_email)
        userEmail.token_send()

        return '{}'
