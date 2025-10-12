from begin.xtensions import *

from begin.globals import Email
from begin.globals import Messages

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
        user_addr = flask.request.remote_addr

        #
        ipInfos = ipInfos_get(ip=user_addr)
        userEmail = userEmailCode_get(ip=user_addr)

        if userEmail == None or ipInfos == None:
            return flask.jsonify({
                'message_error': "Something goes wrong"
            })

        if(not len(ipInfos)):
            ipInfos = (ipInfos_insert(ip=user_addr),)

        #
        emailSend_status = ipInfos[0].email_send_status()

        if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_AMOUNT:
            return flask.jsonify({
                'message_error': "You send many emails in a short time period, wait a bit"
            })

        if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL:
            return flask.jsonify({
                'message_error': 'Please, wait one minute for resend email'
            })

        #
        if userEmail and len(userEmail):
            return flask.jsonify({
                'message_error': "You already receive the email code"
            })
        
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
        user_addr = flask.request.remote_addr

        #
        userEmail = userEmailCode_get(ip=user_addr)
        ipInfos = ipInfos_get(ip=user_addr)

        if userEmail == None or ipInfos == None:
            return flask.jsonify({
                'message_error': "Something goes wrong"
            })

        if not len(ipInfos):
            ipInfos = (ipInfos_insert(ip=user_addr), )

        #
        emailSend_status = ipInfos[0].email_send_status()

        if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_AMOUNT:
            return flask.jsonify({
                'message_error': "You send many emails in a short time period, wait a bit"
            })

        if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL:
            return flask.jsonify({
                'message_error': "Please, wait one minute for resend email"
            })

        #
        if userEmail and len(userEmail):
            userEmailCode_delete(userEmail)

        #
        code = token.token_email_generate()
        userEmail = userEmailCode_insert(token=code, user_name=None, ip=user_addr, email=user_email)

        userEmail.token_send()

        return '{}'
