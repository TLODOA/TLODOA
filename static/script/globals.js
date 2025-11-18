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
        const message = data["message"];

        logs.CLEAN();

        console.log(data);

        if(message == undefined)
            return;

        logs.ADD(message["type"], message["content"]);
    });
}

export function forms_validation(...forms){
    const logs = new MessageLogs();
    const formData = new FormData();

    for(const i of forms){
        const form_data = new FormData(i);
        const fields_required =  document.querySelectorAll(`#${i.id} [required]`) || [];
        // console.log(form_data, fields_required);

        for(const j of fields_required){
            const field = form_data.get(j.name)
            const field_type = typeof field;

            if(field_type == "string" && field.trim())
                continue;

            if(field_type == "object" && field instanceof File && field.size)
                continue;

            logs.CLEAN();
            logs.ADD(logs.MESSAGE_ERROR_CLASS, "Please, fill all required fields");

            j.focus()

            return null;
        }

        form_data.forEach((value, key) => {
            formData.append(key, value);
        });
    }

    return formData;
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

        this.TAGS_NAMES.forEach( (i) => {
            if(!(i.className in Object.keys(this.ELEMENTS_BY_CLASS)) && i.className)
                this.ELEMENTS_BY_CLASS[i.className] = [ ...(document.getElementsByClassName(i.className)) ];

            if(!(i.tagName in Object.keys(this.ELEMENTS_BY_TAG)) && i.tagName)
                this.ELEMENTS_BY_TAG[i.tagName.toLowerCase()] = [ ...(document.getElementsByTagName(i.tagName)) ];

            if(!(i.id in Object.keys(this.ELEMENT_BY_ID)) && i.id)
                this.ELEMENT_BY_ID[i.id] = document.getElementById(i.id);
        })

        //
        this.CSS_VARS = window.getComputedStyle(document.body);
        this.MENU = new Menu();

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
        const className_by_tagName= (element, prefix) => {
            return `${prefix}__${element.tagName.toLowerCase()}`
        };

        const className_by_id = (element, prefix) => {
            return `${prefix}__${element.id}`
        };

        const classNames_by_classes = (element, prefix) => {
            const classNames = [];
            const regex = new RegExp(`^${prefix}__.*`);

            for(const i of element.classList){
                if(regex.test(i)){
                    classNames.push(i);
                    continue;
                }

                classNames.push(`${prefix}__${i}`);
            }

            return classNames;
        }

        //
        const vp_ratio = this.get_screen_ratio();
        const prefixes = [ "reduce", "expand" ];
        const index = ( vp_ratio >= 1 ) + 0;

        const prefix_remove = prefixes[!index + 0];
        const prefix_add = prefixes[index];

        //
        for(const i of Object.keys(this.ELEMENTS_BY_TAG)){
            this.ELEMENTS_BY_TAG[i].forEach((j) => {
                if(j.classList.length){
                    j.classList.remove(...(classNames_by_classes(j, prefix_remove)));
                    j.classList.add(...(classNames_by_classes(j, prefix_add)));
                }

                // j.classList.remove(className_by_tagName(j, prefix_remove));
                j.classList.add(className_by_tagName(j, prefix_add));

                if(j.id){
                    // j.classList.remove(className_by_id(j, prefix_remove));
                    j.classList.add(className_by_id(j, prefix_add));
                }

            });
        }
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
        const page_layout = new Layout_1();
        const ELEMENT_BY_ID = page_layout.ELEMENT_BY_ID;

        //
        this.BOX = ELEMENT_BY_ID["message_logs"];

        this.MESSAGE_ERROR_CLASS = 'message_error';

        //
        this.CLEAN = () => {
            this.BOX.innerHTML = '';
        };

        this.ADD = (message_class, message) => {
            this.BOX.innerHTML += `
                <p class="${message_class}">${message}</p>
        `
        };
    }
}

// Menu
class Menu {
    constructor(){
        this.MENU = document.getElementById("menu");
        this.MENU_ICON = document.getElementById("menu_icon");
        this.MENU_MAIN = document.getElementById("menu_main");

        this.OPEN = 0;

        if(this.MENU == null)
            return;

        this.MENU_ICON.addEventListener("click", () => {
            this.OPEN = !this.OPEN;

            if(!this.OPEN){
                this.close();
                return;
            }

            this.open();
        });
    }


    close() {
        this.MENU_MAIN.style.display = "none";

        this.MENU_ICON.classList.remove("menu_icon__spin90");
        this.MENU_ICON.classList.add("menu_icon__spin00");
    }

    open() {
        this.MENU_MAIN.style.display = "block";

        this.MENU_ICON.classList.remove("menu_icon__spin00");
        this.MENU_ICON.classList.add("menu_icon__spin90");
    }
}

// login.html
export class Login {
    constructor(){
        const page_layout = new Layout_1();
        const ELEMENT_BY_ID = page_layout.ELEMENT_BY_ID;

        this.FORM_EMAIL = ELEMENT_BY_ID['login_form_email'];
        this.FORM_PASSWORD = ELEMENT_BY_ID['login_form_password'];

        this.BUTT_EMAIL_CODE_GET = ELEMENT_BY_ID['login_button_email_code_get'];
        this.BUTT_FINISH = ELEMENT_BY_ID['login_button_finish'];
    }
}

// sign.html
export class Sign {
    constructor(){
        const page_layout = new Layout_1();
        const ELEMENT_BY_ID = page_layout.ELEMENT_BY_ID;

        this.FORM_EMAIL = ELEMENT_BY_ID['sign_form_email'];
        this.FORM_PASSWORD = ELEMENT_BY_ID['sign_form_password'];

        this.BUTT_EMAIL_CODE_GET = ELEMENT_BY_ID['sign_button_email_code_get'];
        this.BUTT_FINISH = ELEMENT_BY_ID['sign_button_finish'];
    }
}

// user_page.html
export class UserPage {
    constructor(){
        const page_layout = new Layout_1();
        const ELEMENT_BY_ID = page_layout.ELEMENT_BY_ID;

        //
        // Event listeners
        this.CLICK_BUTT_EDIT_PROFILE = null;
        this.CLICK_BUTT_EDIT_PROFILE_OK = null;
        this.CHANGE_SELECT_USER_PHOTO = null;
        
        this.eventListeners = null;

        //
        this.BUTT_EDIT_PROFILE = ELEMENT_BY_ID["userPage_button_edit_profile"];
        this.BUTT_EDIT_PROFILE_OK = ELEMENT_BY_ID["userPage_button_edit_profile_ok"];

        this.SELECT_USER_PHOTO = ELEMENT_BY_ID["userPage_select_userPhoto"];

        this.FIELD_PORTFOLIO = ELEMENT_BY_ID["portfolio"]
        this.FIELD_USER_NICK = ELEMENT_BY_ID["nickname"];
        this.FIELD_USER_ABOUT = ELEMENT_BY_ID["userAbout"];
        this.FIELD_USER_PHOTO = ELEMENT_BY_ID["userPhoto"];
    }

    init_eventListeners(){
        this.eventListeners = [
            {type: "click", func: this.CLICK_BUTT_EDIT_PROFILE, to:"BUTT_EDIT_PROFILE"},
            {type: "click", func: this.CLICK_BUTT_EDIT_PROFILE_OK, to:"BUTT_EDIT_PROFILE_OK"},
            {type: "change", func: this.CHANGE_SELECT_USER_PHOTO, to:"SELECT_USER_PHOTO"}
        ]

        for(const i of this.eventListeners){
            this[i.to].addEventListener(i.type, i.func)
        }
    }

    //
    replace_element_for(element, flags) {
        const instance = document.createElement(flags["tag"]);
        instance.id = element.id;
        instance.classList = element.classList;

        for(const i of Object.keys(flags)){
            instance[i] = flags[i];
        }

        //
        element.replaceWith(instance);
        this.attr_reload();
    }

    attr_reload() {
        const page_layout = new Layout_1();
        const ELEMENT_BY_ID = page_layout.ELEMENT_BY_ID;

        for(const i of Object.keys(this)){
            if(!this[i] || !(this[i].id))
                continue;

            if(!(this[i].id in ELEMENT_BY_ID))
                continue;

            this[i] = ELEMENT_BY_ID[this[i].id]
        }

        for(const i of this.eventListeners)
            this[i.to].addEventListener(i.type, i.func);
    }
}

// object_creation.html
export class ObjectCreation {
    constructor() {
        const page_layout = new Layout_1();
        const ELEMENT_BY_ID = page_layout.ELEMENT_BY_ID;

        //
        this.CHANGE_SLCT_OBJECT_PHOTO = null;
        this.CHANGE_SLCT_OBJECT_PHYSIC = null;

        this.CLICK_BUTT_SUBMIT = null;
        this.CLICK_BUTT_SUBMIT_AND_PUBLISH = null;

        //
        this.OBJECT_PHOTO = ELEMENT_BY_ID["objectCreation_object_photo"];
        this.OBJECT_PHYSIC_NAME = ELEMENT_BY_ID["objectCreation_object_physic_name"];
        this.OBJECT_PHYSIC_EXTENSION = ELEMENT_BY_ID["objectCreation_object_physic_extension"];

        this.SLCT_OBJECT_PHYSIC = ELEMENT_BY_ID["objectCreation_object_physic"];
        this.SLCT_OBJECT_PHOTO = ELEMENT_BY_ID["objectCreation_select_object_photo"];
        this.BUTT_SUBMIT = ELEMENT_BY_ID["objectCreation_button_submit"];
        this.BUTT_SUBMIT_AND_PUBLISH = ELEMENT_BY_ID["objectCreation_button_submit_and_publish"];

        this.FORM_OBJECT_HEADER = ELEMENT_BY_ID["objectCreation_form_object_header"];
        this.FORM_OBJECT_PHYSIC = ELEMENT_BY_ID["objectCreation_form_object_physic"];
    }

    init_eventListeners(){
        this.eventListeners = [
            {type: "change", func: this.CHANGE_SLCT_OBJECT_PHOTO, to: "SLCT_OBJECT_PHOTO" },
            {type: "change", func: this.CHANGE_SLCT_OBJECT_PHYSIC, to: "SLCT_OBJECT_PHYSIC"},
            {type: "click", func: this.CLICK_BUTT_SUBMIT, to: "BUTT_SUBMIT"},
            {type: "click", func: this.CLICK_BUTT_SUBMIT_AND_PUBLISH, to: "BUTT_SUBMIT_AND_PUBLISH"}
        ];

        for(const i of this.eventListeners){
            this[i.to].addEventListener(i.type, i.func);
        }
    }
}
