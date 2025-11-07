from begin.globals import Cookie, Messages
from begin.xtensions import *

from database import *

##
def register_app(app:object)->None:
    
    @app.route('/view/user/<user_name>/page')
    def view_user_infos(user_name)->object:
        try:
            userInfos_wrap = session_query(UserInfos, userName=user_name)[0]
            userInfos = model_unwrap(userInfos_wrap)
            print('userInfos: ', userInfos)

            return flask.render_template('user_page.html', user=userInfos)

        ## Where needs a dedicate error page
        except IndexError as e:
            return flask.abort(404)

    @app.route('/view/user/self')
    def view_user_infos_self()->object:
        user_name = Cookie.get("user_name")

        return flask.redirect(flask.url_for("view_user_infos", user_name=user_name))


    @app.route('/view/user/<token>/card')
    def view_user_card(token:str)->object:

        return "Building..."
