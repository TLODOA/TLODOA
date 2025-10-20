from begin.globals import Messages
from begin.xtensions import *

from database import *

from routers import cookie

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
        from begin.globals import Email, Token

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
        userEmail = session_get(UserEmailCode, ip=user_addr, email=user_email, field=Email.FIELD_SIGN)

        ##
        if user == None or userEmail == None or ipInfos == None:
            return flask.jsonify({
                'message': Messages.server_internal_error()
            })

        session_update(ipInfos, "auth_attempts", ipInfos[0].auth_attempts+1)
        ipInfos[0].status_update()

        if not ipInfos[0].client_behavior_normal:
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_client_behavior(ipInfos[0].email_send_time_allow)
            })

        #
        if not len(user):
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_user_not_found()
            })


        if not len(userEmail):
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_email_code_not_send()
            })

        if user[0].email != user_email:
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_user_email_incorrect()
            })

        if not userEmail[0].token_auth(user_email_code):
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_email_code_incorrect()
            })

        if not userEmail[0].token_valid():
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_email_code_validity()
            })
            

        if user[0].password != user_password:
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_user_password_incorrect()
            })

        ##
        userToken = session_insert(UserToken, ip=user_addr, user_name=user_name)
        session_delete(userEmail)

        response = flask.make_response(
                flask.jsonify({
                    'href_link': "/"
                })
            )
        cookie.define(response=response, cookie_name="user_token", cookie_value=userToken.token, max_age=Token.VALIDITY_KEY_USER)
        
        return response

    @app.route('/login/auth', methods=["POST"])
    def login_auth()->object:
        from begin.globals import Email, Status

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

        #
        user = session_get(User, name=user_name)
        ipInfos = session_get(IpInfos, ip=user_addr)
        userEmail = session_get(UserEmailCode, ip=user_addr, email=user_email, field=Email.FIELD_LOGIN)

        ##
        if user == None or ipInfos == None or userEmail == None:
            return flask.jsonify({
                'message': Messages.server_internal_error()
            })

        ipInfos[0].status_update()
        session_update(ipInfos, "auth_attempts", ipInfos[0].auth_attempts + 1)

        if not ipInfos[0].client_behavior_normal:
            return flask.jsonify({
                'message': Messages.login_not_allow_because_client_behavior(ipInfos[0].email_send_time_allow)
            })

        #
        if len(user):
            return flask.jsonify({
                'message': Messages.login_not_allow_because_user_found()
            })


        if not len(userEmail):
            return flask.jsonify({
                'message': Messages.login_not_allow_because_email_code_not_send()
            })

        if not userEmail[0].token_auth(user_email_code):
            return flask.jsonify({
                'message': Messages.login_not_allow_because_email_code_incorrect()
            })

        if not userEmail[0].token_valid():
            return flask.jsonify({
                'message': Messages.login_not_allow_because_email_code_validity()
            })


        if user_password != user_password_check:
            return flask.jsonify({
                'message': Messages.login_not_allow_because_user_password_check_incorrect()
            })
        
        ##
        session_insert(User, name=user_name, email=user_email, password=user_password, status=Status.OFFLINE)
        session_delete(userEmail)

        return flask.jsonify({
            'href_link': "/sign/display"
        })

    @app.route('/logout/auth')
    def logout_auth()->object:
        user_token = flask.request.cookies["user_token"]

        userToken = session_get(UserToken, token=user_token)

        session_delete(userToken)

        return flask.redirect('/')
