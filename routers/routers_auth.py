import flask

##
auth = flask.Blueprint('auth', __name__)

@auth.route('/sign/display')
def sign_display()->object:
    return flask.render_template('sign.html')

@auth.route('/login/display')
def login_display()->object:
    return flask.render_template('login.html')

##
@auth.route('/sign/auth', methods=["POST"])
def sign_auth()->object:
    if flask.request.method != "POST":
        return flask.redirect('/sign_display')

    user_name = flask.request.form["user_name"]
    user_email = flask.request.form["user_email"]
    user_password = flask.request.form["user_password"]

    return flask.redirect('/')
