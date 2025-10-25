from begin.globals import Messages
from begin.xtensions import *

from database import *

from routers import cookie

##
def register_app(app:object)->None:

    @app.route('/login/display')
    def login_display()->object:
        return flask.render_template('login.html')

    @app.route('/sign/display')
    def sign_display()->object:
        return flask.render_template('sign.html')

    ##
    @app.route('/login/auth', methods=["POST"])
    def login_auth()->object:
        from begin.globals import Email, Token, Auth

        if flask.request.method != "POST":
            return flask.jsonify({
                'message': Messages.request_not_allow_because_method()
            })

        forms = flask.request.json
        user_addr = flask.request.remote_addr

        user_name = forms["user_name"].strip()
        user_email = forms["user_email"].strip()
        user_email_code = forms["user_email_code"].strip()

        user_password = forms["user_password"].strip()
        
        #
        hashed_userName = Token.crypt_hash256(user_name)
        hashed_userAddr = Token.crypt_hash256(user_addr)
        hashed_userEmail = Token.crypt_hash256(user_email)

        #
        user = session_get(User, hashed_name=hashed_userName)
        ipInfos = session_get(IpInfos, hashed_ip=hashed_userAddr)
        userEmail = session_get(UserEmailCode, hashed_ip=hashed_userAddr, hashed_email=hashed_userEmail, field=Email.FIELD_SIGN)

        ##
        if user == None or userEmail == None or ipInfos == None:
            return flask.jsonify({
                'message': Messages.server_internal_error()
            })

        ipInfos[0].status_update()

        if not ipInfos[0].client_behavior_normal:
            return flask.jsonify({
                'message': Messages.login_not_allow_because_client_behavior(ipInfos[0].email_send_time_allow)
            })

        session_update(ipInfos, auth_attempts=ipInfos[0].auth_attempts+1)
        #
        if not len(user):
            return flask.jsonify({
                'message': Messages.login_not_allow_because_user_not_found()
            })


        if not len(userEmail):
            return flask.jsonify({
                'message': Messages.login_not_allow_because_email_code_not_send()
            })

        if user[0].hashed_email != hashed_userEmail:
            return flask.jsonify({
                'message': Messages.login_not_allow_because_user_email_incorrect()
            })

        if not userEmail[0].token_auth(user_email_code):
            return flask.jsonify({
                'message': Messages.login_not_allow_because_email_code_incorrect()
            })

        if not userEmail[0].token_valid():
            return flask.jsonify({
                'message': Messages.login_not_allow_because_email_code_validity()
            })
            

        if not user[0].password_auth(user_password):
            return flask.jsonify({
                'message': Messages.login_not_allow_because_user_password_incorrect()
            })

        ##
        user_token = Token.user_generate()
        userToken = session_insert(UserToken, ip=user_addr, user_name=user_name, token=user_token)

        session_delete(userEmail)

        response = flask.make_response(
                flask.jsonify({
                    'href_link': "/"
                })
            )
        cookie.define(response=response, cookie_name="user_token", cookie_value=user_token, max_age=Token.VALIDITY_KEY_USER)
        cookie.define(response=response, cookie_name="user_name", cookie_value=user_name, max_age=Token.VALIDITY_KEY_USER)
        
        return response

    @app.route('/sign/auth', methods=["POST"])
    def sign_auth()->object:
        from begin.globals import Email, Status, Auth

        ##
        if flask.request.method != "POST":
            return flask.jsonify({
                'message': Messages.request_not_allow_because_method()
            })

        forms = flask.request.json
        user_addr = flask.request.remote_addr

        user_name = forms["user_name"].strip()
        user_email = forms["user_email"].strip()
        user_email_code = forms["user_email_code"].strip()

        user_password = forms["user_password"].strip()
        user_password_check = forms["user_password_check"].strip()

        #
        hashed_userAddr = Token.crypt_hash256(user_addr)
        hashed_userName = Token.crypt_hash256(user_name)
        hashed_userEmail = Token.crypt_hash256(user_email)

        #
        user = session_get(User, hashed_name=hashed_userName)
        ipInfos = session_get(IpInfos, hashed_ip=hashed_userAddr)
        userEmail = session_get(UserEmailCode, hashed_ip=hashed_userAddr, hashed_email=hashed_userEmail, field=Email.FIELD_LOGIN)

        ##
        if user == None or ipInfos == None or userEmail == None:
            return flask.jsonify({
                'message': Messages.server_internal_error()
            })

        ipInfos[0].status_update()
        session_update(ipInfos, auth_attempts=ipInfos[0].auth_attempts + 1)

        if not ipInfos[0].client_behavior_normal:
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_client_behavior(ipInfos[0].email_send_time_allow)
            })

        #
        if len(user):
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_user_found()
            })


        if not len(userEmail):
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_email_code_not_send()
            })

        if not userEmail[0].token_auth(user_email_code):
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_email_code_incorrect()
            })

        if not userEmail[0].token_valid():
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_email_code_validity()
            })


        if user_password != user_password_check:
            return flask.jsonify({
                'message': Messages.sign_not_allow_because_user_password_check_incorrect()
            })
        
        ##
        session_insert(User, name=user_name, email=user_email, password=user_password, status=Status.OFFLINE)
        session_delete(userEmail)

        return flask.jsonify({
            'href_link': "/login/display"
        })

    @app.route('/logout/auth')
    def logout_auth()->object:
        from begin.globals import Token

        ##
        if not cookie.valid("user_name") or not cookie.valid("user_token"):
            return flask.redirect('/')

        user_name = cookie.get("user_name")
        user_token = cookie.get("user_token")
        user_addr = flask.request.remote_addr

        if user_token == None or user_name == None:
            return flask.redirect('/')

        #
        hashed_userName = Token.crypt_hash256(user_name)
        hashed_userAddr = Token.crypt_hash256(user_addr)

        ##
        userToken = session_get(UserToken, hashed_ip=hashed_userAddr, hashed_userName=hashed_userName)

        response = flask.make_response(flask.redirect('/'))
        cookie.delete(response, "user_name")
        cookie.delete(response, "user_token")

        for i in userToken:
            if not i.token_auth(user_token):
                continue

            session_delete((i, ))

        return response
