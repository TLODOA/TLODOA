import * as global from "./globals.js"

//
const objectCreation = new global.ObjectCreation();
const logs = new global.MessageLogs();

objectCreation.CHANGE_SLCT_OBJECT_PHOTO = (e) => {
    e.preventDefault();
    
    //
    const value = e.target.value;
    for(const i of objectCreation.SLCT_OBJECT_PHOTO){
        const attributes = i.attributes;

        if(attributes.getNamedItem("selected") != null){
            attributes.removeNamedItem("selected");
            continue;
        }

        if(value != i.value)
            continue;

        attributes.setNamedItem(document.createAttribute("selected"));
    }

    objectCreation.OBJECT_PHOTO.src = value;
}

objectCreation.CHANGE_SLCT_OBJECT_PHYSIC = (e) => {
    e.preventDefault();

    //
    const file = e.target.files[0];
    if(!file)
        return;

    objectCreation.OBJECT_PHYSIC_NAME.textContent = file.name;
}

//
objectCreation.CLICK_BUTT_SUBMIT = (e) => {
    e.preventDefault();

    //
    const form_data = global.forms_validation(objectCreation.FORM_OBJECT_HEADER, objectCreation.FORM_OBJECT_PHYSIC);
    if(!form_data)
        return;

    // console.log(form_data);
}

objectCreation.init_eventListeners();
