from begin.globals import Cookie, Messages
from begin.xtensions import *

from database import *

##
def register_app(app:object)->None:
    
    @app.route('/view/user/<user_name>/page')
    def view_user_infos(user_name)->object:
        import time

        try:
            userInfos_wrap = session_query(UserInfos, userName=user_name)[0]
            userInfos = model_unwrap(userInfos_wrap)

            time_viewed_last = time.localtime(userInfos["time_viewed_last"])
            time_arrival = time.localtime(userInfos["time_arrival"])

            user_data = {
                "userName": userInfos["userName"],
                "description": userInfos["description"],
                "photoPath": userInfos["photoPath"],

                "infos": {
                    "Last connection": f"{ time.strftime("%d/%m/%Y, %H:%M:%S", time_viewed_last) } ",
                    "Here since": f"{ time.strftime("%A, %B %d, %Y %H:%M:%S GMT%Z", time_arrival) }"
                }
            }

            return flask.render_template('user_page.html', user=user_data)

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
