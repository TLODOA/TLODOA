from begin.xtensions import *
from database import *

from routers import cookie

##
def register_app(app:object)->None:

    @app.before_request
    def before_request()->object|None:
        from begin.globals import Token
        from itsdangerous import BadSignature

        ##
        if not flask.request.path.startswith('/view'):
            return 

        #
        user_addr = flask.request.remote_addr

        print('cookie: ', cookie.valid("user_name"), cookie.valid("user_token"))
        if not cookie.valid("user_name"):
            userTokens = session_get(UserToken, ip=user_addr)
            session_delete(userTokens)

            response = flask.make_response(flask.redirect('/'))
            cookie.delete(response, "user_name")
            cookie.delete(response, "user_token")

            return response

        user_name = cookie.get("user_name")


        if not cookie.valid("user_token"):
            userTokens = session_get(UserToken, ip=user_addr, user_name=user_name)
            session_delete(userTokens)

            response = flask.make_response(flask.redirect('/'))
            cookie.delete(response, "user_name")
            cookie.delete(response, "user_token")

            return response

        user_token = cookie.get("user_token")

        #
        ipInfos = session_get(IpInfos, ip=user_addr)
        userToken = session_get(UserToken, ip=user_addr, user_name=user_name)

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
            flask.session["user_name"] = userToken[0].user_name
            flask.session["user_card"] = 0

            return

        # print(flask.request.path, flask.session)

        #
        if "user_name" in flask.session:
            del flask.session["user_name"]

        return flask.redirect('/')

    #
    @app.route('/')
    def fork()->object:
        if not "user_name" in flask.request.cookies:
            return flask.redirect('/login/display')

        return flask.redirect('/view/index')

    @app.route('/view/index')
    def view_index()->object:
        return flask.render_template('index.html')
