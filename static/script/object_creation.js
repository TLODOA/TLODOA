import * as global from "./globals.js"

//
const objectCreation = new global.ObjectCreation();

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

objectCreation.CHANGE_OBJECT_PHYSIC = (e) => {
    e.preventDefault();

    //
    const file = e.target.files[0];
    if(!file)
        return;

    console.log(file);
    objectCreation.OBJECT_PHYSIC_NAME.textContent = file.name;
}

objectCreation.init_eventListeners();
