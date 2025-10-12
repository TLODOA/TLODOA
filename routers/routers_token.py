from begin.xtensions import *
from begin import token

from database import *

##
def register_app(app:object)->None:

    @app.route('/token/email/generate', methods=['POST'])
    def email_token_generate()->object:
        if flask.request.method != 'POST':
            return '{}'
        
        #
        forms = flask.request.json
        user_email = forms["user_email"]

        #
        user_addr = flask.request.remote_addr

        ipInfos = ipInfos_get(ip=user_addr)
        userEmail = userEmailCode_get(ip=user_addr)

        if userEmail == None or ipInfos == None:
            return flask.jsonify({
                'message_error': "Something goes wrong"
            })

        if userEmail and len(userEmail):
            return flask.jsonify({
                "message_error": "You already receive the email code"
            })
        
        #
        if(not len(ipInfos)):
            ipInfos = ipInfos_insert(ip=user_addr)

        #
        code = token.token_email_generate()
        userEmail = userEmailCode_insert(token=code, user_name=None, ip=user_addr, email=user_email)
        userEmail.token_send()

        return '{}'

    @app.route('/token/email/generate/new', methods=['POST'])
    def email_token_generate_new()->object:
        if flask.request.method != 'POST':
            return '{}'
        
        #
        forms = flask.request.json
        user_email = forms["user_email"]

        #
        user_addr = flask.request.remote_addr

        userEmail = userEmailCode_get(ip=user_addr)
        ipInfos = ipInfos_get(ip=user_addr)

        if userEmail == None or ipInfos == None:
            return flask.jsonify({
                'message_error': "Something goes wrong"
            })

        if userEmail and not len(userEmail):
            if not len(ipInfos):
                ipInfos_insert(ip=user_addr)

            code = token.token_email_generate()
            userEmail = userEmailCode_insert(token=code, user_name=None, ip=user_addr, email=user_email)

            userEmail.token_send()

            return '{}'

        userEmailCode_delete(userEmail)

        code = token.token_email_generate()
        userEmail = userEmailCode_insert(token=code, user_name=None, ip=user_addr, email=user_email)

        userEmail.token_send()

        return '{}'
