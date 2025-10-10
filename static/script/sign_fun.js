import * as global from './globals.js'

const sign = new global.Sign();

//
console.log(sign.FORM_EMAIL);

sign.BUTT_EMAIL_CODE_GET.addEventListener('click', (e) => {
    e.preventDefault();

    const form_data = new FormData(sign.FORM_EMAIL);
    console.log(form_data);

    fetch('/email/token/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},

        body: JSON.stringify(Object.fromEntries(form_data))

    })
    .then(response => response.json())
    .then(data => {
        const message_error = data["message_error"];

        console.log(global.MESSAGE_ERROR);
        
        global.MESSAGE_ERROR.innerHTML += message_error;
    });
});

sign.BUTT_EMAIL_CODE_GET_NEW.addEventListener('click', (e) => {
    e.preventDefault();

    console.log('Commit!');
});
