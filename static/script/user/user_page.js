import * as global from '../globals.js'

//
const userPage = new global.UserPage();
const logs = new global.MessageLogs();

userPage.CLICK_BUTT_EDIT_PROFILE = (e) => {
    e.preventDefault();

    //
    // console.log(userPage.FIELD_PORTFOLIO.innerHTML.trim());
    userPage.replace_element_for(userPage.FIELD_PORTFOLIO, {
        tag: "form",

        method: "POST",
        innerHTML: userPage.FIELD_PORTFOLIO.innerHTML.trim()
    });

    userPage.replace_element_for(userPage.FIELD_USER_NICK, {
        tag: "input",

        name: "user_nickname",
        value: userPage.FIELD_USER_NICK.textContent.trim(),
        autocomplete: "off"
    });

    userPage.replace_element_for(userPage.FIELD_USER_ABOUT, {
        tag: "textarea",

        name: "user_about",
        rows: "10",
        cols: "50",
        innerHTML: userPage.FIELD_USER_ABOUT.textContent.trim(),
        autocomplete: "off"
    });

    //
    // console.log(userPage.BUTT_EDIT_PROFILE_OK);

    userPage.BUTT_EDIT_PROFILE.style.display = 'none';
    userPage.BUTT_EDIT_PROFILE_OK.style.display = 'block';

    userPage.SELECT_USER_PHOTO.style.display = 'block';
}

userPage.CHANGE_SELECT_USER_PHOTO = (e) => {
    e.preventDefault();

    //
    const value_selected = e.target.value;
    for(const i of userPage.SELECT_USER_PHOTO){
        const attributes = i.attributes;

        if(attributes.getNamedItem("selected") != null){
            attributes.removeNamedItem("selected");
            continue;
        }

        if(i.value != value_selected)
            continue;

        attributes.setNamedItem(document.createAttribute("selected"));
    }

    userPage.FIELD_USER_PHOTO.src = value_selected;
}

//
userPage.CLICK_BUTT_EDIT_PROFILE_OK = (e) => {
    e.preventDefault();

    // 
    const formData = global.forms_validation(userPage.FIELD_PORTFOLIO);
    if(!formData)
        return;

    const formData_json = Object.fromEntries(formData);
    console.log(formData_json);

    // Ajax
    fetch('/user/profile/edit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },

        body: JSON.stringify(formData_json)
    })
    .then(response => response.json())
    .then(data => {
        const message = data["message"];

        logs.CLEAN();
        logs.ADD(message["type"], message["content"]);
    });

    // Return default page
    userPage.replace_element_for(userPage.FIELD_PORTFOLIO, {
        tag: "div",
        innerHTML: userPage.FIELD_PORTFOLIO.innerHTML.trim()
    });

    userPage.replace_element_for(userPage.FIELD_USER_NICK, {
        tag: "h4",
        innerHTML: `
        <u>
            ${formData_json["user_nickname"]}
        </u>`
    });

    userPage.replace_element_for(userPage.FIELD_USER_ABOUT, {
        tag: "h3",
        textContent: formData_json["user_about"]
    });

    userPage.BUTT_EDIT_PROFILE.style.display = 'block';
    userPage.BUTT_EDIT_PROFILE_OK.style.display = 'none';

    userPage.SELECT_USER_PHOTO.style.display = 'none';
}

userPage.init_eventListeners();
