from begin.xtensions import *

from begin import token

from database import *

##
def register_app(app:object)->None:

    @app.route('/token/email/generate', methods=['POST'])
    def email_token_generate()->object:
        from begin.globals import Email, Messages

        if flask.request.method != 'POST':
            return flask.jsonify({
                'message': "Invalid method request"
            })
        
        #
        forms = flask.request.json

        user_name = forms["user_name"]
        user_email = forms["user_email"]

        user_addr = flask.request.remote_addr

        #
        ipInfos = session_get(IpInfos, ip=user_addr)
        userEmail = session_get(UserEmailCode, ip=user_addr)

        ##
        if ipInfos == None or userEmail == None:
            return Messages.server_internal_error()

        if(not len(ipInfos)):
            ipInfos = (session_insert(IpInfos, ip=user_addr),)

        #
        emailSend_status = ipInfos[0].email_send_status

        if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_AMOUNT:
            return flask.jsonify({
                'message': \
                    Messages.email_not_allow_because_amount(ipInfos[0].email_send_time_allow)
                })

        if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_INTERVAL:
            return flask.jsonify({
                'message': \
                    Messages.email_not_allow_because_interval(ipInfos[0].email_send_time_allow)
                })

        if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_TOKEN_ATTEMPTS:
            return flask.jsonify({
                'message': \
                    Messages.email_not_allow_because_token_attempts(ipInfos[0].email_send_time_allow)
            })

        if emailSend_status == Email.SEND_NOT_ALLOW_BECAUSE_IP_BLOCKED:
            return flask.jsonify({
                'message': \
                    Messages.email_not_allow_because_ip_blocked(ipInfos[0].email_send_time_allow)
            })

        ##
        if len(userEmail):
            session_delete(userEmail)
        
        #
        code = token.token_email_generate()
        userEmail = session_insert(UserEmailCode, token=code, name=None, ip=user_addr, email=user_email)

        userEmail.token_send()

        """ Able this after application developer
        return flask.jsonify({
            'message': \
                Messages.email_ok()
            })
        """
        return flask.jsonify({
            'message': \
                'This is your email token: ' + code
            })
