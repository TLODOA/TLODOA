//
export function request_token_email(json){
    fetch('/token/email/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},

        body: JSON.stringify(json)

    })
    .then(response => response.json())
    .then(data => {
        const logs = new MessageLogs();

        logs.MESSAGE_LOGS_CLEAN();

        console.log(data);

        const message = data["message"];
        if(message == undefined)
            return;

        logs.MESSAGE_LOGS_INSERT(message, logs.MESSAGE_ERROR_ID);
    });
}

// Time
export class Time{
    time_human(timestamp=null){

        date = new Date();
        if(timestamp != null)
            date = new Date(timestamp);

        const seconds = String(date.getSeconds()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const hours = String(date.getMinutes()).padStart(2, '0');

        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth()+1).padStart(2, '0');

        const year = date.getFullYear();

        const date_formated = {
            "seconds": seconds,
            "minutes": minutes,
            "hours": hours,

            "day": day,
            "month": month,

            "year": year
        };
        
        return date_formated;
    }
    
    time_machine(date){
        date_timestamp = new Date(`${date["year"]}-${date["month"]}-${date["day"]}\T${date["hours"]}:${date["minutes"]}:${date["seconds"]}`);

        return date_timestamp.getTime();
    }
}

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

// login.html
export class Login {
    constructor(){
        this.FORM_EMAIL_ID = 'login_form_email';
        this.FORM_PASSWORD_ID = 'login_form_password';

        this.FORM_EMAIL = document.getElementById(this.FORM_EMAIL_ID);
        this.FORM_PASSWORD = document.getElementById(this.FORM_PASSWORD_ID);

        //
        this.BUTT_EMAIL_CODE_GET_ID = 'login_button_email_code_get';
        this.BUTT_FINISH_ID = 'login_button_finish';


        this.BUTT_EMAIL_CODE_GET = document.getElementById(this.BUTT_EMAIL_CODE_GET_ID);
        this.BUTT_FINISH = document.getElementById(this.BUTT_FINISH_ID);
    }
}

// sign.html
export class Sign {
    constructor(){
        this.FORM_EMAIL_ID  ='sign_form_email';
        this.FORM_PASSWORD_ID = 'sign_form_password';


        this.FORM_EMAIL = document.getElementById(this.FORM_EMAIL_ID);
        this.FORM_PASSWORD = document.getElementById(this.FORM_PASSWORD_ID);

        //
        this.BUTT_EMAIL_CODE_GET_ID = 'sign_button_email_code_get';
        this.BUTT_FINISH = 'sign_button_finish';


        this.BUTT_EMAIL_CODE_GET = document.getElementById(this.BUTT_EMAIL_CODE_GET_ID);
        this.BUTT_FINISH = document.getElementById(this.BUTT_FINISH);
    }
}
