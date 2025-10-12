// MessageLogs
export class MessageLogs{
    constructor(){
        this.MESSAGE_LOGS_ID = 'message_logs';
        this.MESSAGE_LOGS = document.getElementById(this.MESSAGE_LOGS_ID);

        //
        this.MESSAGE_ERROR_ID = 'message_error';

        //
        this.MESSAGE_LOGS_CLEAN = () => {
            this.MESSAGE_LOGS.innerHTML = '';
        };

        this.MESSAGE_LOGS_INSERT = (message, message_id) => {
            this.MESSAGE_LOGS.innerHTML += `
                <p id=${message_id}>${message}</p>
        `
        };
    }
}

// sign.html
export class Sign {
    constructor(){
        this.FORM_EMAIL_ID = 'sign_form_email';
        this.FORM_PASSWORD_ID = 'sign_form_password';

        this.FORM_EMAIL = document.getElementById(this.FORM_EMAIL_ID);
        this.FORM_PASSWORD = document.getElementById(this.FORM_PASSWORD_ID);

        //
        this.BUTT_EMAIL_CODE_GET_ID = 'sign_button_email_code_get';
        this.BUTT_EMAIL_CODE_GET_NEW_ID = 'sign_button_email_code_get_new';

        this.BUTT_EMAIL_CODE_GET = document.getElementById(this.BUTT_EMAIL_CODE_GET_ID);
        this.BUTT_EMAIL_CODE_GET_NEW = document.getElementById(this.BUTT_EMAIL_CODE_GET_NEW_ID);
    }
}

// login.html
export function login_init(){
    const LOGIN_FORM_EMAIL_ID = 'login_form_email';
    const LOGIN_FORM_PASSWORD_ID = 'login_form_password';

    const LOGIN_FORM_EMAIL = document.getElementById(LOGIN_FORM_EMAIL_ID);
    const LOGIN_FORM_PASSWORD = document.getElementById(LOGIN_FORM_PASSWORD_ID);
}
