from begin.xtensions import *

from database import *

##
def register_app(app:object)->None:

    @app.route('/view/user/<user_name>/infos')
    def view_user_infos(user_name)->object:
        from begin.globals import Token

        ##
        hashed_userName = Token.crypt_sha256(user_name)

        user = session_get(UserCore, hashed_name=hashed_userName)

        return flask.render_template('user_infos.html', user=user[0])

    @app.route('/view/user/<token>/card')
    def view_user_card(token:str)->object:

        return "Building..."
