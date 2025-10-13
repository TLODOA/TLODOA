from begin.xtensions import *

from begin.globals import Email, Messages

from begin import token

from database import *

##
def email_client_state(ipInfos:object)->str:
    emailSend_status = ipInfos.email_send_status()

    if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_AMOUNT:
        return flask.jsonify({
            'message': \
                Messages.email_not_allow_because_amount(ipInfos.email_send_last + Email.SEND_INTERVAL_BANNED)
        })

    if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL:
        return flask.jsonify({
            'message': \
                Messages.email_not_allow_because_interval(ipInfos.email_send_last + Email.SEND_INTERVAL)
        })

    return '{}'

def email_server_state(ipInfos:tuple, userEmailCode)->str:
    if ipInfos == None or userEmailCode == None:
        return Messages.email_internal_error()

    return '{}'

##
def register_app(app:object)->None:

    @app.route('/token/email/generate/<token_type>', methods=['POST'])
    def email_token_generate(token_type)->object:
        if flask.request.method != 'POST':
            return flask.jsonify({
                'message': "Invalid method request"
            })
        
        #
        forms = flask.request.json
        user_email = forms["user_email"]
        user_addr = flask.request.remote_addr

        #
        ipInfos = ipInfos_get(ip=user_addr)
        userEmail = userEmailCode_get(ip=user_addr)

        ##
        email_server_output = email_server_state(ipInfos, userEmail)
        if email_server_output != '{}':
            return email_server_output

        if(not len(ipInfos)):
            ipInfos = (ipInfos_insert(ip=user_addr),)

        #
        email_client_output = email_client_state(ipInfos[0])
        if email_client_output != '{}':
            return email_client_output

        ##
        if len(userEmail) and token_type == "first":
            return flask.jsonify({
                'message': \
                    Messages.email_already_sended()
            })
        elif len(userEmail) and token_type=="new":
            userEmailCode_delete(userEmail)
        
        #
        code = token.token_email_generate()
        userEmail = userEmailCode_insert(token=code, user_name=None, ip=user_addr, email=user_email)

        userEmail.token_send()

        return flask.jsonify({
            'message': \
                Messages.email_ok()
        })
