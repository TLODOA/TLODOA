from begin.globals import Messages, Cookie
from begin.xtensions import *

from database import *

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
                'message': Messages.Message(
                    content = Messages.Login.Request.Error.invalid_method,
                    type = error_js_class
                ).json
            })

        forms = flask.request.json
        user_addr = flask.request.remote_addr

        user_name = forms["user_name"].strip()
        user_email = forms["user_email"].strip()
        user_email_code = forms["user_email_code"].strip()

        user_password = forms["user_password"].strip()

        #
        ipInfos = session_query(IpInfos, ip=user_addr)
        user = session_query(UserCore, name=user_name)
        userEmail = session_query(UserEmailCode, ip=user_addr, email=user_email, field=UserEmailCode.FIELD_SIGN)

        error_js_class = Messages.Error.js_class

        ##
        if user is None or userEmail is None or ipInfos is None:
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Login.Error.internal,
                    type = error_js_class
                ).json
            })

        ipInfos[0].status_update()

        if not ipInfos[0].client_behavior_normal:
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Login.Request.Error.invalid_client_behavior(ipInfos[0].email_send_time_allow),
                    type = error_js_class
                ).json
            })

        session_update(ipInfos, auth_attempts=ipInfos[0].auth_attempts+1)
        #
        if not len(user):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Login.Error.user_not_found,
                    type = error_js_class
                ).json
            })

        if not user[0].hashed_email.strip() == Token.crypt_sha256(user_email):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Login.Error.incorrect_user_email,
                    type = error_js_class
                ).json
            })


        if not len(userEmail):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Login.EmailCode.Error.code_not_send,
                    type = error_js_class
                ).json
            })

        if not userEmail[0].token_auth(user_email_code):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Login.EmailCode.Error.incorrect_code,
                    type = error_js_class
                ).json
            })

        if not userEmail[0].token_valid():
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Login.EmailCode.Error.invalid_code_validity,
                    type = error_js_class
                ).json
            })
            

        if not user[0].password_auth(user_password):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Login.Error.incorrect_user_password,
                    type = error_js_class
                ).json
            })

        ##
        user_token = Token.user_generate()
        userToken = session_insert(UserToken, ip=user_addr, userName=user_name, token=user_token, field=UserToken.FIELD_AUTH)

        session_delete(userEmail)

        response = flask.make_response(
                flask.jsonify({
                    'href_link': "/"
                })
            )
        Cookie.define(response=response, cookie_name="user_token", cookie_value=user_token, max_age=UserToken.VALIDITY)
        Cookie.define(response=response, cookie_name="user_name", cookie_value=user_name, max_age=UserToken.VALIDITY)
        
        return response

    @app.route('/sign/auth', methods=["POST"])
    def sign_auth()->object:
        from begin.globals import Email, Auth

        ##
        if flask.request.method != "POST":
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Sign.Request.Error.invalid_method,
                    type = error_js_class
                ).json
            })

        forms = flask.request.json
        user_addr = flask.request.remote_addr

        user_name = forms["user_name"].strip()
        user_email = forms["user_email"].strip()
        user_email_code = forms["user_email_code"].strip()

        user_password = forms["user_password"].strip()
        user_password_check = forms["user_password_check"].strip()

        #
        user = session_query(UserCore, name=user_name)
        ipInfos = session_query(IpInfos, ip=user_addr)
        userEmail = session_query(UserEmailCode, ip=user_addr, email=user_email, field=UserEmailCode.FIELD_LOGIN)

        error_js_class = Messages.Error.js_class

        ##
        if user == None or ipInfos == None or userEmail == None:
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Sign.Request.Error.internal,
                    type = error_js_class
                ).json
            })

        ipInfos[0].status_update()
        session_update(ipInfos, auth_attempts=ipInfos[0].auth_attempts + 1)

        if not ipInfos[0].client_behavior_normal:
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Sign.Request.Error.invalid_client_behavior(ipInfos[0].email_send_time_allow),
                    type = error_js_class
                ).json
            })

        #
        if len(user):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Sign.Error.user_found,
                    type = error_js_class
                ).json
            })


        if not len(userEmail):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Sign.EmailCode.Error.code_not_send,
                    type = error_js_class
                ).json
            })

        if not userEmail[0].token_auth(user_email_code):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Sign.EmailCode.Error.incorrect_code,
                    type = error_js_class
                ).json
            })

        if not userEmail[0].token_valid():
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Sign.EmailCode.Error.invalid_code_validity,
                    type = error_js_class
                ).json
            })


        if user_password != user_password_check:
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.Sign.Error.password_not_match,
                    type = error_js_class
                ).json
            })
        
        ##
        session_insert(UserCore, name=user_name, email=user_email, password=user_password)
        session_insert(UserInfos, userName=user_name, nickname=user_name)

        session_delete(userEmail)

        return flask.jsonify({
            'href_link': "/login/display"
        })

    @app.route('/logout/auth')
    def logout_auth()->object:
        from begin.globals import Token

        ##
        if not Cookie.valid("user_name") or not Cookie.valid("user_token"):
            return flask.redirect('/')

        user_name = Cookie.get("user_name")
        user_token = Cookie.get("user_token")
        user_addr = flask.request.remote_addr

        if user_token is None or user_name is None:
            return flask.redirect('/')

        ##
        userToken = session_query(UserToken, ip=user_addr, userName=user_name)

        response = flask.make_response(flask.redirect('/'))
        Cookie.delete(response, "user_name")
        Cookie.delete(response, "user_token")

        for i in userToken:
            if not i.token_auth(user_token):
                continue

            session_delete((i, ))

        return response
