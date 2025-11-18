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

        import zipfile
        import io

        import time
        import json
        import os

        ##
        if flask.request.method != 'POST':
            return flask.jsonify({
                "message": Messages.Message(
                    content = Messages.ObjectCreation.Request.invalid_method,
                    type = Messages.ObjectCreation.Error.js_class
                ).json
            })

        #
        forms_raw = flask.request.form.get("json")
        forms = json.loads(forms_raw)

        file = flask.request.files["file"]
        file_size = len(file.read())

        user_addr = flask.request.remote_addr

        error_js = Messages.ObjectCreation.Error.js_class

        ##
        if file_size > ObjectCore.OBJECT_PHYSIC_MAX_LEN:
            return flask.jsonify({
                "message": Messages.Message(
                    content = Messages.ObjectCreation.Error.invalid_file_size,
                    type = error_js
                ).json
            })

        ipInfos = session_query(IpInfos, ip=user_addr)[0]
        object_creation_status = ipInfos.object_create_status

        if object_creation_status == ObjectCore.STATUS_BLOCKED_BECAUSE_INTERVAL:
            return flask.jsonify({
                "message": Messages.Message(
                    content = Messages.ObjectCreation.Error.invalid_interval(ipInfos.object_create_time_allow),
                    type = error_js
                ).json
            })

        if object_creation_status == ObjectCore.STATUS_BLOCKED_BECAUSE_AMOUNT:
            return flask.jsonify({
                "message": Messages.Message(
                    content = Messages.ObjectCreation.Error.invalid_amount,
                    type = error_js
                ).json
            })

        ##
        user_name = Cookie.get("user_name")
        object_id = Token.code_generate(ObjectCore.ID_CHARS, ObjectCore.ID_LEN)

        #
        object_nickname = forms["object_nickname"]

        object_pathIcon = forms["object_photo"]
        object_pathIcon_splited = '/'.join(object_pathIcon.split('/')[2:])

        object_physic = file
        object_physic_extension = forms["object_physic_extension"]
        object_physic_name = f"{object_id}.{object_physic_extension}"
        object_physic_data = object_physic.read()
        
        #
        icon = session_query(Icon, pathIcon=object_pathIcon_splited, type=Icon.TYPE_BID)[0]
        icon_name = model_get(icon, "cipher_name")[0]

        ##
        objectCore = session_insert(ObjectCore, id=object_id, objectPhysical=ObjectCore.PATH_STORAGE, userName=user_name, iconBidName=icon_name,  nickname=object_nickname)
        model_update(ipInfos, object_create_last_time=time.time())

        #
        if objectCore is None:
            return flask.jsonify({
                "message": Messages.Message(
                    content=Messages.ObjectCreation.Request.Error.internal,
                    type=error_js
                ).json
            })

        with zipfile.ZipFile(ObjectCore.PATH_STORAGE, 'a', compression=zipfile.ZIP_DEFLATED) as file_zip:
            file_zip.writestr(object_physic_name, object_physic_data)

        ##
        return flask.jsonify({
            "message": Messages.Message(
                content=Messages.ObjectCreation.Success.ok,
                type=Messages.ObjectCreation.Success.js_class
            ).json
        })
