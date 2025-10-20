from begin.xtensions import *
from database import *

##
def register_app(app:object)->None:

    @app.before_request
    def before_request()->object|None:
        user_addr = flask.request.remote_addr
        user_token = flask.request.cookies.get("user_token", None)

        ipInfos = session_get(IpInfos, ip=user_addr)
        userToken = session_get(UserToken, token=user_token)

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
        if not flask.request.path.startswith('/view'):
            return 

        #
        if "user_name" in flask.session:
            del flask.session["user_name"]

        return flask.redirect('/')

    #
    @app.route('/')
    def fork()->object:
        if not "user_name" in flask.session:
            return flask.redirect('/login/display')

        return flask.redirect('/view/index')

    @app.route('/view/index')
    def view_index()->object:
        return flask.render_template('index.html')
