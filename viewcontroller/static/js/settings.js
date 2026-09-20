// viewcontroller/static/js/settings.js


const xboxControllerCheckbox =
    document.getElementById(
        "xbox-controller-enabled"
    );


async function loadSettings() {

    const response = await fetch(
        "/settings/xbox_controller_enabled"
    );

    if (!response.ok) {

        console.error(
            "Failed to load Xbox controller setting"
        );

        return;
    }


    const data = await response.json();

    xboxControllerCheckbox.checked =
        data.value === "1";
}


async function saveXboxControllerSetting() {

    const value =
        xboxControllerCheckbox.checked
            ? "1"
            : "0";


    const response = await fetch(
        "/settings/xbox_controller_enabled",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                value: value
            })
        }
    );


    if (!response.ok) {

        console.error(
            "Failed to save Xbox controller setting"
        );

        return;
    }


    console.log(
        "Xbox controller setting saved:",
        value
    );
}


xboxControllerCheckbox.addEventListener(
    "change",
    saveXboxControllerSetting
);


loadSettings();
