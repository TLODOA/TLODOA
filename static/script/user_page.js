import * as global from './globals.js'

//
const userPage = new global.UserPage();

userPage.CLICK_BUTT_EDIT_PROFILE = (e) => {
    e.preventDefault();

    //
    const form = userPage.replace_element_for(userPage.FIELD_PORTFOLIO, {
        tag: "form",

        method: "GET",
        innerHTML: userPage.FIELD_PORTFOLIO.innerHTML.trim()
    });

    const input_userName = userPage.replace_element_for(userPage.FIELD_USER_NAME, {
        tag: "input",

        name: "user_name",
        value: userPage.FIELD_USER_NAME.textContent.trim()
    });

    const input_userAbout = userPage.replace_element_for(userPage.FIELD_USER_ABOUT, {
        tag: "input",

        name: "user_about",
        value: userPage.FIELD_USER_ABOUT.textContent.trim()
    });

    //
    userPage.BUTT_EDIT_PROFILE.style.display = 'none';
    userPage.BUTT_EDIT_PROFILE_OK.style.display = 'block';
}

userPage.CLICK_BUTT_EDIT_PROFILE_OK = (e) => {
    e.preventDefault();

    //
    const form_data = Object.fromEntries(new FormData(userPage.FIELD_PORTFOLIO))
    console.log(form_data);

    const portfolio = userPage.replace_element_for(userPage.FIELD_PORTFOLIO, {
        tag: "div",
        innerHTML: userPage.FIELD_PORTFOLIO.innerHTML.trim()
    });

    const userName = userPage.replace_element_for(userPage.FIELD_USER_NAME, {
        tag: "h1",
        textContent: form_data["user_name"]
    });

    const userAbout = userPage.replace_element_for(userPage.FIELD_USER_ABOUT, {
        tag: "h3",
        textContent: form_data["user_about"]
    });

    //
    userPage.BUTT_EDIT_PROFILE.style.display = 'block';
    userPage.BUTT_EDIT_PROFILE_OK.style.display = 'none';
}

userPage.init_eventListeners();
