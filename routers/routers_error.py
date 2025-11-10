from begin.xtensions import *
from werkzeug.exceptions import HTTPException

from begin.globals import Messages

##
def register_app(app:object)->None:

    @app.errorhandler(Exception)
    def handler_error_generic(e)->object:
        response = {
            "name": "Internal Error",
            "message": "Cool! The problem isn't you!" + '  ' + str(e),
            "status_code": 0
        }

        if isinstance(e, HTTPException) and e.code >= 400 and e.code < 500:
            response = {
                "name": e.name,
                "message": e.description,
                "status_code": e.code
            }

        Messages.error('generic_funcion: ', e)

        return flask.render_template('errors/ERROR.html', response=response)
