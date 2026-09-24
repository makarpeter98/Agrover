// viewcontroller/static/js/settings.js


const xboxControllerCheckbox =
    document.getElementById(
        "xbox-controller-enabled"
    );


const arrivalDistanceInput =
    document.getElementById(
        "arrival-distance-limit"
    );


const headingToleranceInput =
    document.getElementById(
        "heading-tolerance"
    );


/* =========================================================
   LOAD SETTINGS
   ========================================================= */

async function loadSettings()
{
    try
    {
        const xboxResponse = await fetch(
            "/settings/xbox_controller_enabled"
        );


        if (xboxResponse.ok)
        {
            const data =
                await xboxResponse.json();

            xboxControllerCheckbox.checked =
                data.value === "1";
        }
        else
        {
            console.error(
                "Failed to load Xbox controller setting"
            );
        }


        const arrivalResponse = await fetch(
            "/settings/arrival_distance_limit"
        );


        if (arrivalResponse.ok)
        {
            const data =
                await arrivalResponse.json();

            arrivalDistanceInput.value =
                data.value;
        }
        else
        {
            console.error(
                "Failed to load arrival distance limit"
            );
        }


        const headingResponse = await fetch(
            "/settings/heading_tolerance"
        );


        if (headingResponse.ok)
        {
            const data =
                await headingResponse.json();

            headingToleranceInput.value =
                data.value;
        }
        else
        {
            console.error(
                "Failed to load heading tolerance"
            );
        }
    }
    catch (error)
    {
        console.error(
            "Failed to load settings:",
            error
        );
    }
}


/* =========================================================
   XBOX CONTROLLER
   ========================================================= */

async function saveXboxControllerSetting()
{
    const value =
        xboxControllerCheckbox.checked
            ? "1"
            : "0";


    const response = await fetch(
        "/settings/xbox_controller_enabled",
        {
            method: "POST",

            headers:
            {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                value: value
            })
        }
    );


    if (!response.ok)
    {
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


/* =========================================================
   ARRIVAL DISTANCE LIMIT
   ========================================================= */

async function saveArrivalDistanceLimit()
{
    const value =
        arrivalDistanceInput.value;


    if (value === "")
    {
        return;
    }


    const response = await fetch(
        "/settings/arrival_distance_limit",
        {
            method: "POST",

            headers:
            {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                value: value
            })
        }
    );


    if (!response.ok)
    {
        console.error(
            "Failed to save arrival distance limit"
        );

        return;
    }


    console.log(
        "Arrival distance limit saved:",
        value
    );
}


/* =========================================================
   HEADING TOLERANCE
   ========================================================= */

async function saveHeadingTolerance()
{
    const value =
        headingToleranceInput.value;


    if (value === "")
    {
        return;
    }


    const response = await fetch(
        "/settings/heading_tolerance",
        {
            method: "POST",

            headers:
            {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                value: value
            })
        }
    );


    if (!response.ok)
    {
        console.error(
            "Failed to save heading tolerance"
        );

        return;
    }


    console.log(
        "Heading tolerance saved:",
        value
    );
}


/* =========================================================
   EVENTS
   ========================================================= */

xboxControllerCheckbox.addEventListener(
    "change",
    saveXboxControllerSetting
);


arrivalDistanceInput.addEventListener(
    "change",
    saveArrivalDistanceLimit
);


headingToleranceInput.addEventListener(
    "change",
    saveHeadingTolerance
);


/* =========================================================
   INITIAL LOAD
   ========================================================= */

loadSettings();
