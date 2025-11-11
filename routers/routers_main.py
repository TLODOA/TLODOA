from begin.globals import Cookie, Token, Router
from begin.xtensions import *

from database import *

##
def register_app(app:object)->None:

    @app.before_request
    def before_request()->object|None:
        import time

        ##
        if flask.request.path.startswith('/static'):
            return

        if not Router.exists(app, flask.request.path):
            flask.abort(404)

        if not flask.request.path.startswith('/view'):
            return 

        print('request_path: ', flask.request.path)
        #
        user_addr = flask.request.remote_addr

        print('cookie: ', Cookie.valid("user_name"), Cookie.valid("user_token"))
        if not Cookie.valid("user_name"):
            userTokens = session_query(UserToken, ip=user_addr)
            session_delete(userTokens)

            response = flask.make_response(flask.redirect('/'))
            Cookie.delete(response, "user_name")
            Cookie.delete(response, "user_token")

            return response

        user_name = Cookie.get("user_name")


        if not Cookie.valid("user_token"):
            userTokens = session_query(UserToken, ip=user_addr, userName=user_name)
            session_delete(userTokens)

            response = flask.make_response(flask.redirect('/'))
            Cookie.delete(response, "user_name")
            Cookie.delete(response, "user_token")

            return response

        user_token = Cookie.get("user_token")

        #
        ipInfos = session_query(IpInfos, ip=user_addr)
        userToken = session_query(UserToken, ip=user_addr, userName=user_name, validity__gt=time.time(), field=UserToken.FIELD_AUTH)

        #
        valid = False

        for i in userToken:
            valid = i.token_auth(user_token)

            if valid:
                break

        if not valid:
            userToken = ()

        #
        if len(userToken) and userToken[0].validity < time.time():
            session_delete(userToken)
            userToken = ()

        if len(userToken) and not len(ipInfos):
            ipInfos = session_insert(IpInfos, ip=user_addr)

        if len(userToken) and len(ipInfos) and ipInfos[0].validity < time.time():
            ipInfos[0].validity = time.time() + Token.VALIDITY_IPINFOS

        #
        if len(userToken):

            return

        # print(flask.request.path, flask.session)
        response = flask.make_response(flask.redirect('/'))
        cookies = flask.request.cookies

        for i in cookies.keys():
            Cookie.delete(response=response, cookie_name=i)

        return response

    #
    @app.route('/')
    def fork()->object:
        if not "user_name" in flask.request.cookies:
            return flask.redirect('/login/display')

        return flask.redirect('/view/index')

    @app.route('/view/index')
    def view_index()->object:
        return flask.render_template('index.html')
