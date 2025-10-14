import * as global from './globals.js'

const sign = new global.Sign();
const logs = new global.MessageLogs();

//
sign.BUTT_EMAIL_CODE_GET.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const form_data = new FormData(sign.FORM_EMAIL);
    const form_data_json = Object.fromEntries(form_data);

    if(!form_data_json["user_name"] || !form_data_json["user_email"]){
        logs.MESSAGE_LOGS_CLEAN();
        logs.MESSAGE_LOGS_INSERT("Please fill all required fields");

        return;
    }

    global.request_token_email(form_data_json);
});

//
sign.BUTT_FINISH.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const form_data_email_json = Object.fromEntries(new FormData(sign.FORM_EMAIL));
    const form_data_passw_json = Object.fromEntries(new FormData(sign.FORM_PASSWORD));

    const form_data_json = { ...form_data_email_json, ...form_data_passw_json };

    for(var i in form_data_json){
        if(form_data_json[i])
            continue;

        logs.MESSAGE_LOGS_CLEAN();
        logs.MESSAGE_LOGS_INSERT("Please, fill all required fields");

        return;
    }

    //
    fetch('/sign/auth', {
        method: 'POST',
        headers: { 'Content-Type': "application/json; charset-utf-8" },

        body: JSON.stringify(form_data_json)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
});
