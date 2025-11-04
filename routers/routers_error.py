from begin.xtensions import *

##
def register_app(app:object)->None:

    @app.errorhandler(Exception)
    def handler_error_generic(e)->object:
        response = {
            "name": e.name,
            "message": e.description,
            "status_code": e.code
        }

        return flask.render_template('errors/ERROR.html', response=response)
