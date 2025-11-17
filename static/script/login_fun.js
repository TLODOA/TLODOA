import * as global from './globals.js'

const login = new global.Login();
const logs = new global.MessageLogs();

//
login.BUTT_EMAIL_CODE_GET.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const form_data = new FormData(login.FORM_EMAIL);
    const form_data_json = Object.fromEntries(form_data);

    if(!form_data_json["user_name"] || !form_data_json["user_email"]){
        logs.CLEAN();
        logs.ADD(logs.MESSAGE_ERROR_CLASS, "Please fill all required fields");

        return;
    }

    form_data_json["user_email_field"] = 2;

    global.request_token_email(form_data_json);
});

//
login.BUTT_FINISH.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const form_data_json = global.forms_validation(login.FORM_EMAIL, login.FORM_PASSWORD);
    if(!form_data_json)
        return;

    //
    fetch('/login/auth', {
        method: 'POST',
        headers: { 'Content-Type': "application/json; charset-utf-8" },

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
    });
});
