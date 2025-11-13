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
            
            icon_wrap = session_query(Icon, hashed_name=userInfos["hashed_iconProfileName"])[0]
            icon = model_unwrap(icon_wrap)

            icons_profile = session_query(Icon, type=Icon.TYPE_PROFILE)

            ##
            time_viewed_last = time.localtime(userInfos["time_viewed_last"])
            time_arrival = time.localtime(userInfos["time_arrival"])

            user_data = {
                "userName": userInfos["userName"],
                "nickname": userInfos["nickname"],
                "description": userInfos["description"],

                "iconName": icon["name"],
                "iconPath": icon["pathIcon"],

                "infos": {
                    "Last connection": f"{ time.strftime("%d/%m/%Y, %H:%M:%S", time_viewed_last) } ",
                    "Here since": f"{ time.strftime("%A, %B %d, %Y %H:%M:%S GMT%Z", time_arrival) }"
                },

                "activity": [],

                "is_same": Cookie.get("user_name") == userInfos["userName"]
            }

            system_data = {
                "icons": {model_get(i, "cipher_name")[0]: model_get(i, "cipher_pathIcon")[0] for i in icons_profile }
            }

            return flask.render_template('user_page.html', user=user_data, system=system_data)

        except IndexError as e:
            return flask.abort(404)

    @app.route('/view/user/self')
    def view_user_infos_self()->object:
        user_name = Cookie.get("user_name")

        return flask.redirect(flask.url_for("view_user_infos", user_name=user_name))

    ##
    @app.route('/view/user/card')
    def view_user_card()->object:

        return "Building..."

    @app.route('/view/user/objects')
    def view_user_objects()->object:
        return flask.render_template('user_objects.html')

    ##
    @app.route('/user/profile/edit', methods=['POST'])
    def user_profile_edit()->object:
        if flask.request.method != 'POST':
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.ProfileEdit.Request.Error.invalid_method,
                    type = Messages.ProfileEdit.Error.js_class
                ).json
            })

        form_json = flask.request.json
        user_name = Cookie.get("user_name")

        error_class = Messages.Error.js_class
        success_class = Messages.Success.js_class

        #
        user_nickname = form_json["user_nickname"].strip()
        user_description = form_json["user_about"].strip()

        user_iconProfile = form_json["user_photo_selection"]
        user_iconProfile = user_iconProfile.split('/')[-1]
        user_iconProfile = user_iconProfile.split('.')[0]

        print('profile icon: ', user_iconProfile)


        if not len(user_nickname) or not len(user_description):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.ProfileEdit.Error.empty_fields,
                    type = error_class
                ).json
            })

        #
        userInfos = session_query(UserInfos, name=user_name)
        icon = session_query(Icon, name=user_iconProfile)

        if not len(userInfos):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.ProfileEdit.Error.user_not_found,
                    type = error_class
                ).json
            })

        if not len(icon):
            return flask.jsonify({
                'message': Messages.Message(
                    content = Messages.ProfileEdit.Error.icon_not_found,
                    type = error_class
                ).json
            })

        icon_name = model_get(icon[0], "cipher_name")[0]
        model_update(userInfos[0], nickname=user_nickname, description=user_description, iconProfileName=icon_name)


        return flask.jsonify({
            'message': Messages.Message(
                content = Messages.ProfileEdit.Success.ok,
                type = success_class
            ).json
        })

    @app.route('/user/profile/settings')
    def view_user_settings()->object:
        return flask.render_template('user_settings.html')
