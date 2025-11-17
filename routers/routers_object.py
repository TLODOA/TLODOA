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

        return flask.render_template("object_creation.html", system=system)
