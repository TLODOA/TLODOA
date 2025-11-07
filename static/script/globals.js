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

// Layouts / CSS
export class Layout_1{
    constructor(){
        this.TAGS_NAMES = [ ...(document.getElementsByTagName("*")) ];

        this.ELEMENTS_BY_CLASS = {};
        this.ELEMENTS_BY_TAG = {};
        this.ELEMENT_BY_ID = {};

        this.CLASS_ATTR_DEFAULT = {};

        this.TAGS_NAMES.forEach( (i) => {
            if(!(i.className in Object.keys(this.ELEMENTS_BY_CLASS)) && i.className){
                this.ELEMENTS_BY_CLASS[i.className] = [ ...(document.getElementsByClassName(i.className)) ];
                this.CLASS_ATTR_DEFAULT[i.className] = window.getComputedStyle(this.ELEMENTS_BY_CLASS[i.className][0]);
            }

            if(!(i.tagName in Object.keys(this.ELEMENTS_BY_TAG)) && i.tagName)
                this.ELEMENTS_BY_TAG[i.tagName.toLowerCase()] = [ ...(document.getElementsByTagName(i.tagName)) ];

            if(!(i.id in Object.keys(this.ELEMENT_BY_ID)) && i.id)
                this.ELEMENT_BY_ID[i.id] = document.getElementById(i.id);
        })

        //
        this.CSS_VARS = window.getComputedStyle(document.body);

        //
        this.resize_timeout;

        window.addEventListener('resize', () => {
            clearTimeout(this.resize_timeout);

            this.resize_timeout = setTimeout(() =>{
                this.set_dynamic_classNames();
            }, 200);
        });
    }

    set_dynamic_classNames(){
        const className_by_tagName= (element, suffix) => {
            return `${element.tagName.toLowerCase()}_${suffix}`
        };
        const className_by_id = (element, suffix) => {
            return `${element.id}_${suffix}`
        };

        //
        const vp_ratio = this.get_screen_ratio();
        const suffixes = [ "reduce", "expand" ];
        const index = ( vp_ratio >= 1 ) + 0;

        const suffix_remove = suffixes[!index + 0];
        const suffix_add = suffixes[index];

        //
        for(const i of Object.keys(this.ELEMENTS_BY_TAG)){
            this.ELEMENTS_BY_TAG[i].forEach((j) => {
                j.classList.remove(className_by_tagName(j, suffix_remove));
                j.classList.add(className_by_tagName(j, suffix_add));

                if(!j.id)
                    return;

                j.classList.add(className_by_id(j, suffix_add));
                j.classList.remove(className_by_id(j, suffix_remove));
            });
        }
    }

    get_css_var(var_name){
        return this.CSS_VARS.getPropertyValue(var_name);
    }

    get_screen_ratio(){
        return window.screen.width / window.screen.height;
    }
}

export class Layout_2 extends Layout_1{}

export class Layout_3 extends Layout_1{}

export class Layout_4 extends Layout_1{}

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
