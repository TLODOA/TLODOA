from begin.xtensions import *
from database import *

##
def register_app(app:object)->None:

    @app.route('/token/email/generate', methods=['POST'])
    def email_token_generate()->object:
        from begin.globals import Email, Messages, Token

        if flask.request.method != 'POST':
            return flask.jsonify({
                'message': "Invalid method request"
            })
        
        #
        forms = flask.request.json
        user_addr = flask.request.remote_addr

        user_name = forms["user_name"].strip()
        user_email = forms["user_email"].strip()
        user_email_field = forms["user_email_field"]

        #
        ipInfos = session_query(IpInfos, ip=user_addr)
        userEmail = session_query(UserEmailCode, ip=user_addr, field=user_email_field)

        ##
        if ipInfos == None or userEmail == None or not user_email_field in UserEmailCode.FIELD_ABLE:
            return flask.jsonify({
                'message': \
                    Messages.server_internal_error()
                })


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
        email_token = Token.email_generate()

        userEmail = session_insert(UserEmailCode, ip=user_addr, email=user_email, field=user_email_field, token=email_token)

        userEmail.token_send()

        """ Able this after application developer
        return flask.jsonify({
            'message': \
                Messages.email_ok()
            })
        """
        return flask.jsonify({
            'message': \
                'This is your email token: ' + email_token
            })
