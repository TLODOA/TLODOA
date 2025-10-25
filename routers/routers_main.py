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
            userTokens = session_get(UserToken, hashed_ip=Token.crypt_sha256(user_addr))
            session_delete(userTokens)

            response = flask.make_response(flask.redirect('/'))
            cookie.delete(response, "user_name")
            cookie.delete(response, "user_token")

            return response

        user_name = cookie.get("user_name")


        if not cookie.valid("user_token"):
            hashed_userAddr, hashed_userName = Token.crypt_sha256(user_addr), Token.crypt_sha256(user_name)

            #
            userTokens = session_get(UserToken, hashed_ip=hashed_userAddr, hashed_userName=hashed_userName)
            session_delete(userTokens)

            response = flask.make_response(flask.redirect('/'))
            cookie.delete(response, "user_name")
            cookie.delete(response, "user_token")

            return response

        user_token = cookie.get("user_token")

        #
        hashed_userAddr, hashed_userName = Token.crypt_sha256(user_addr), Token.crypt_sha256(user_name)

        ipInfos = session_get(IpInfos, hashed_ip=hashed_userAddr)
        userToken = session_get(UserToken, hashed_ip=hashed_userAddr, hashed_userName=hashed_userName)

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
            cookie.delete(response=response, cookie_name=i)

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
