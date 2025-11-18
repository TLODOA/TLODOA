from begin.xtensions import *
from database import *

import random

##
def register_app(app:object)->None:

    @app.route("/view/object/create")
    def view_object_creation()->None:
        iconsBid_wrap = session_query(Icon, type=Icon.TYPE_BID)

        system = {
            "icons": { model_get(i, "cipher_name")[0]: model_get(i, "cipher_pathIcon")[0] for i in iconsBid_wrap },
            "icon_default": model_get(random.choice(iconsBid_wrap), "cipher_pathIcon")[0]
        }

        return flask.render_template("object/object_creation.html", system=system)

    @app.route("/view/object/create/auth", methods=["POST"])
    def view_object_creation_auth()->None:
        from begin.globals import Messages, Token, Cookie

        import json
        import os

        ##
        if flask.request.method != 'POST':
            return flask.jsonify({
                "message": Messages.Message(
                    content=Messages.ObjectCreation.Request.invalid_method,
                    type=Messages.ObjectCreation.Error.js_class
                ).json
            })

        #
        forms_raw = flask.request.form.get("json")
        forms = json.loads(forms_raw)

        file = flask.request.files["file"]

        ##
        user_name = Cookie.get("user_name")

        object_nickname = forms["object_nickname"]
        object_pathIcon = forms["object_photo"]

        object_physic = file
        object_physic_extension = forms["object_physic_extension"]
        
        #
        object_id = Token.code_generate(ObjectCore.ID_CHARS, ObjectCore.ID_LEN)

        object_pathIcon_splited = '/'.join(object_pathIcon.split('/')[2:])
        object_physic_path = os.path.join(ObjectCore.PATH_STORAGE, f"{object_id}.{object_physic_extension}")

        icon = session_query(Icon, pathIcon=object_pathIcon_splited, type=Icon.TYPE_BID)[0]
        icon_name = model_get(icon, "cipher_name")[0]

        # print('session_insert args: ', object_id, object_physic_path, user_name, icon_name, object_nickname)
        
        ##
        objectCore = session_insert(ObjectCore, id=object_id, objectPhysical=object_physic_path, userName=user_name, iconBidName=icon_name,  nickname=object_nickname)

        error_js = Messages.ObjectCreation.Error.js_class
        #
        if objectCore is None:
            return flask.jsonify({
                "message": Messages.Message(
                    content=Messages.ObjectCreation.Request.Error.internal,
                    type=error_js
                ).json
            })

        file.save(object_physic_path)

        return flask.jsonify({
            "message": Messages.Message(
                content=Messages.ObjectCreation.Success.ok,
                type=Messages.ObjectCreation.Success.js_class
            ).json
        })
