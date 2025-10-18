from begin.xtensions import *

from database import *

##
def register_app(app:object)->None:

    @app.route('/view/user/<user_name>/infos')
    def user_view(user_name)->None:
        user = session_get(User, name=user_name)

        return flask.render_template('user_page.html', user=user[0])
