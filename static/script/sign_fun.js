import * as global from './globals.js'

const sign = new global.Sign();
const logs = new global.MessageLogs();

const time = new global.Time();

//
function request_token_email(url_request){
    const form_data = new FormData(sign.FORM_EMAIL);
    const form_data_json = Object.fromEntries(form_data);

    if(!form_data_json["user_name"] || !form_data_json["user_email"]){
        logs.MESSAGE_LOGS_CLEAN();
        logs.MESSAGE_LOGS_INSERT("Please fill all required fields");

        return;
    }

    //
    fetch(url_request, {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},

        body: JSON.stringify(form_data_json)

    })
    .then(response => response.json())
    .then(data => {
        logs.MESSAGE_LOGS_CLEAN();

        console.log(data);

        const message = data["message"];
        if(message == undefined)
            return;

        logs.MESSAGE_LOGS_INSERT(message, global.MESSAGE_ERROR_ID);
    });
}

sign.BUTT_EMAIL_CODE_GET.addEventListener('click', (e) => {
    e.preventDefault();

    //
    request_token_email('/token/email/generate/first');
});

sign.BUTT_EMAIL_CODE_GET_NEW.addEventListener('click', (e) => {
    e.preventDefault();

    //
    request_token_email('/token/email/generate/new');
});
