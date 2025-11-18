import * as global from '../globals.js'

const login = new global.Login();
const logs = new global.MessageLogs();

//
login.BUTT_EMAIL_CODE_GET.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const formData = new FormData(login.FORM_EMAIL);
    const formData_json = Object.fromEntries(formData);

    if(!formData_json["user_name"] || !formData_json["user_email"]){
        logs.CLEAN();
        logs.ADD(logs.MESSAGE_ERROR_CLASS, "Please fill all required fields");

        return;
    }

    formData_json["user_email_field"] = 2;

    global.request_token_email(formData_json);
});

//
login.BUTT_FINISH.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const formData = global.forms_validation(login.FORM_EMAIL, login.FORM_PASSWORD);
    if(!formData)
        return;

    const formData_json = Object.fromEntries(formData);

    //
    fetch('/login/auth', {
        method: 'POST',
        headers: { 'Content-Type': "application/json; charset-utf-8" },

        body: JSON.stringify(formData_json)
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
