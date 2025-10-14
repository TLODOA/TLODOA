import * as global from './globals.js'

const login = new global.Login()
const logs = new global.MessageLogs()

//
login.BUTT_EMAIL_CODE_GET.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const form_data = new FormData(login.FORM_EMAIL);
    const form_data_json = Object.fromEntries(form_data);

    if(!form_data_json["user_name"] || !form_data_json["user_email"]){
        logs.MESSAGE_LOGS_CLEAN();
        logs.MESSAGE_LOGS_INSERT("Please, fill all required fields");

        return;
    }

    global.request_token_email(form_data_json);
});

//
login.BUTT_FINISH.addEventListener('click', (e) => {
    e.preventDefault();
    
    //
    const form_data_email = Object.fromEntries(new FormData(login.FORM_EMAIL));
    const form_data_passw = Object.fromEntries(new FormData(login.FORM_PASSWORD));

    const form_data_json = { ...form_data_email, ...form_data_passw };

    //
    fetch('/login/auth', {
        method: 'POST',
        headers: { 'Content-Type': "application/json; charset=utf-8" },
        body: JSON.stringify(form_data_json)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })

});
