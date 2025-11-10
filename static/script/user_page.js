import * as global from './globals.js'

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

        name: "user_name",
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

userPage.CLICK_BUTT_EDIT_PROFILE_OK = (e) => {
    e.preventDefault();

    //
    const form_data = Object.fromEntries(new FormData(userPage.FIELD_PORTFOLIO))

    fetch('/user/profile/edit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },

        body: JSON.stringify(form_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });

    //
    userPage.replace_element_for(userPage.FIELD_PORTFOLIO, {
        tag: "div",
        innerHTML: userPage.FIELD_PORTFOLIO.innerHTML.trim()
    });

    userPage.replace_element_for(userPage.FIELD_USER_NICK, {
        tag: "h4",
        innerHTML: `
        <u>
            ${form_data["user_name"]}
        </u>`
    });

    userPage.replace_element_for(userPage.FIELD_USER_ABOUT, {
        tag: "h3",
        textContent: form_data["user_about"]
    });

    //
    userPage.BUTT_EDIT_PROFILE.style.display = 'block';
    userPage.BUTT_EDIT_PROFILE_OK.style.display = 'none';

    userPage.SELECT_USER_PHOTO.style.display = 'none';
}

userPage.CHANGE_SELECT_USER_PHOTO = (e) => {
    e.preventDefault();

    //
    const value_selected = e.target.value;
    // console.log(value_selected);

    userPage.FIELD_USER_PHOTO.src = value_selected;
}

userPage.init_eventListeners();
