from begin.globals import Messages
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
            return flask.jsonify({
                'message': Messages.request_not_allow_because_method()
            })

        forms = flask.request.json

        user_name = forms["user_name"]

        user_email = forms["user_email"]
        user_email_code = forms["user_email_code"]

        user_password = forms["user_password"]

        user_addr = flask.request.remote_addr

        #
        user = session_get(User, name=user_name)
        ipInfos = session_get(IpInfos, ip=user_addr)
        userEmail = session_get(UserEmailCode, name=user_name)

        if user == None or userEmail == None or ipInfos == None:
            return flask.jsonify({
                'message': Messages.server_internal_error()
            })

        #
        if not len(user):
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_user_not_found
            })

        if not len(userEmail) or user[0].email != user_email:
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_user_email_incorrect
            })

        if user[0].password != user_password:
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_user_password_incorrect
            })

        if userEmail.token != user_email_code:
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_email_code_incorrect
            })
        #
        ipInfos[0].user_name = user_name
        
        return flask.jsonify({
            'href_link': '/'
        })

    @app.route('/login/auth', methods=["POST"])
    def login_auth()->object:
        if flask.request.method != "POST":
            return flask.jsonify({
                'message': Messages.request_not_allow_because_method()
            })

        forms = flask.request.json
        print(forms)

        user_name = forms["user_name"]

        user_email = forms["user_email"]
        user_email_code = forms["user_email_code"]

        user_password = forms["user_password"]
        user_password_check = forms["user_password_check"]

        user_addr = flask.request.remote_addr

        ##
        user = session_get(User, name=user_name)
        ipInfos = session_get(IpInfos, ip=user_addr)
        userEmail = session_get(UserEmailCode, ip=user_addr)

        return '{}'
