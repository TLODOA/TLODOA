from begin.xtensions import *

from database import *

##
def register_app(app:object)->None:

    @app.route('/view/user/<user_name>/infos')
    def view_user_infos(user_name)->object:
        user = session_get(User, name=user_name)

        return flask.render_template('user_infos.html', user=user[0])

    @app.route('/view/user/<token>/card')
    def view_user_card(token:str)->object:

        return "Building..."
