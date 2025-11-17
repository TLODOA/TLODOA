import * as global from './globals.js'

const sign = new global.Sign()
const logs = new global.MessageLogs()

//
sign.BUTT_EMAIL_CODE_GET.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const form_data = new FormData(sign.FORM_EMAIL);
    const form_data_json = Object.fromEntries(form_data);

    if(!form_data_json["user_name"] || !form_data_json["user_email"]){
        logs.CLEAN();
        logs.ADD("Please, fill all required fields");

        return;
    }

    form_data_json["user_email_field"] = 1;

    global.request_token_email(form_data_json);
});

//
sign.BUTT_FINISH.addEventListener('click', (e) => {
    e.preventDefault();
    
    //
    const form_data_json = global.forms_validation(sign.FORM_EMAIL, sign.FORM_PASSWORD);
    if(!form_data_json)
        return;

    //
    fetch('/sign/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },

        body: JSON.stringify(form_data_json)
    })
    .then(response => response.json())
    .then(data => {
        const href_link = data["href_link"];
        const message = data["message"];

        if(href_link != undefined){
            window.location.href = href_link;
            return;
        }

        logs.CLEAN();
        logs.ADD(message["type"], message["content"]);
    })
});
