from begin.xtensions import *
from database import *

##
def register_app(app:object)->None:

    @app.before_request
    def before_request()->object|None:
        user_addr = flask.request.remote_addr

        ipInfos = session_get(IpInfos, ip=user_addr)

        if ipInfos[0].user_name != None:
            flask.session["user_name"] = ipInfos[0].user_name
            return

        print(flask.request.path, flask.session)
        if not flask.request.path.startswith('/view'):
            return 

        #
        print(flask.session)
        if "user_name" in flask.session:
            del flask.session["user_name"]

        return flask.redirect('/')

    #
    @app.route('/')
    def fork()->object:
        if not "user_name" in flask.session:
            return flask.redirect('/sign/display')

        return flask.redirect('/view/index')

    @app.route('/view/index')
    def index()->object:
        return flask.render_template('index.html')
