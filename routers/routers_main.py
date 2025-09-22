import flask

main = flask.Blueprint('main', __name__)
@main.route('/')
def index()->object:
    print(flask.session)
    if not "user_name" in flask.session:
        return flask.redirect('/sign/display')

    return flask.render_template('index.html')
