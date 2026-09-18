/* =========================================================
   MAP INITIALIZATION
   ========================================================= */

let map =
    L.map("map");


L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 22,
        maxNativeZoom: 19,

        attribution:
            "© OpenStreetMap"
    }
)
.addTo(map);



/* =========================================================
   ROVER
   ========================================================= */

let roverMarker = null;

let roverPosition = null;

let firstFix = true;



/* =========================================================
   WAYPOINTS
   ========================================================= */

let waypointMarkers = [];

let waypoints = [];

let activeTarget = null;



/* =========================================================
   ROUTE
   ========================================================= */

let routeLine = null;



/* =========================================================
   MARKER ICONS
   ========================================================= */

let redIcon =
    L.icon(
        {
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",

            shadowUrl:
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",

            iconSize:
                [25, 41],

            iconAnchor:
                [12, 41]
        }
    );


let blueIcon =
    L.icon(
        {
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png",

            shadowUrl:
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",

            iconSize:
                [25, 41],

            iconAnchor:
                [12, 41]
        }
    );



/* =========================================================
   UPDATE GPS
   ========================================================= */

async function updateGPS()
{
    try
    {
        let response =
            await fetch("/gps");


        let gps =
            await response.json();


        if (gps.latitude == null)
        {
            return;
        }


        roverPosition =
            [
                gps.latitude,
                gps.longitude
            ];



        /* -------------------------------------------------
           CREATE ROVER MARKER
           ------------------------------------------------- */

        if (roverMarker == null)
        {
            roverMarker =
                L.marker(
                    roverPosition,
                    {
                        icon: redIcon
                    }
                )
                .addTo(map);
        }


        /* -------------------------------------------------
           UPDATE ROVER MARKER
           ------------------------------------------------- */

        else
        {
            roverMarker.setLatLng(
                roverPosition
            );
        }



        /* -------------------------------------------------
           FIRST GPS FIX
           ------------------------------------------------- */

        if (firstFix)
        {
            map.setView(
                roverPosition,
                18
            );

            firstFix = false;
        }
    }

    catch (error)
    {
        console.log(
            "GPS update error:",
            error
        );
    }
}



/* =========================================================
   UPDATE WAYPOINTS
   ========================================================= */

async function updatePoints()
{
    try
    {
        let response =
            await fetch("/points");


        let points =
            await response.json();


        waypoints = points;


        updateWaypointMarkers();

        updateWaypointPanel();
    }

    catch (error)
    {
        console.log(
            "Waypoint update error:",
            error
        );
    }
}



/* =========================================================
   UPDATE WAYPOINT MARKERS
   ========================================================= */

function updateWaypointMarkers()
{
    waypointMarkers.forEach(
        marker =>
        {
            map.removeLayer(marker);
        }
    );


    waypointMarkers = [];


    waypoints.forEach(
        (point, index) =>
        {
            let marker =
                L.marker(
                    [
                        point.latitude,
                        point.longitude
                    ],
                    {
                        icon: blueIcon
                    }
                )
                .addTo(map);


            marker.bindTooltip(
                "#" + (index + 1),
                {
                    direction: "top"
                }
            );


            waypointMarkers.push(marker);
        }
    );
}



/* =========================================================
   UPDATE WAYPOINT PANEL
   ========================================================= */

function updateWaypointPanel()
{
    let countElement =
        document.getElementById(
            "waypoint-count"
        );


    let targetElement =
        document.getElementById(
            "active-target"
        );


    let listElement =
        document.getElementById(
            "waypoint-list"
        );



    /* -----------------------------------------------------
       COUNT
       ----------------------------------------------------- */

    countElement.textContent =
        waypoints.length;



    /* -----------------------------------------------------
       ACTIVE TARGET
       ----------------------------------------------------- */

    let targetIndex =
        findTargetIndex();


    if (targetIndex === -1)
    {
        targetElement.textContent =
            "-";
    }
    else
    {
        targetElement.textContent =
            "#" + (targetIndex + 1);
    }



    /* -----------------------------------------------------
       LIST
       ----------------------------------------------------- */

    if (waypoints.length === 0)
    {
        listElement.innerHTML =
            '<div class="waypoint-empty">' +
            'No waypoints' +
            '</div>';

        return;
    }


    listElement.innerHTML = "";


    waypoints.forEach(
        (point, index) =>
        {
            let item =
                document.createElement(
                    "div"
                );


            item.className =
                "waypoint-item";


            if (index === targetIndex)
            {
                item.classList.add(
                    "active"
                );
            }


            item.innerHTML =
                `
                <div class="waypoint-number">
                    ${String(index + 1).padStart(2, "0")}
                </div>

                <div class="waypoint-coordinates">

                    <div>
                        ${point.latitude.toFixed(7)}
                    </div>

                    <div>
                        ${point.longitude.toFixed(7)}
                    </div>

                </div>
                `;


            item.addEventListener(
                "click",
                () =>
                {
                    map.setView(
                        [
                            point.latitude,
                            point.longitude
                        ],
                        20
                    );
                }
            );


            listElement.appendChild(
                item
            );
        }
    );
}



/* =========================================================
   NAVIGATION STATUS
   ========================================================= */

async function updateNavigationStatus()
{
    try
    {
        let response =
            await fetch("/nav/status");


        let data =
            await response.json();


        activeTarget =
            data.target ?? null;


        updateWaypointPanel();
    }

    catch (error)
    {
        console.log(
            "Navigation status error:",
            error
        );
    }
}



/* =========================================================
   FIND ACTIVE TARGET
   ========================================================= */

function findTargetIndex()
{
    if (!activeTarget)
    {
        return -1;
    }


    for (
        let i = 0;
        i < waypoints.length;
        i++
    )
    {
        let point =
            waypoints[i];


        if (
            Math.abs(
                point.latitude -
                activeTarget.latitude
            ) < 0.0000001
            &&
            Math.abs(
                point.longitude -
                activeTarget.longitude
            ) < 0.0000001
        )
        {
            return i;
        }
    }


    return -1;
}



/* =========================================================
   CENTER ON ROVER
   ========================================================= */

function centerOnRover()
{
    if (!roverPosition)
    {
        return;
    }


    map.setView(
        roverPosition,
        20
    );
}



/* =========================================================
   CENTER ON TARGET
   ========================================================= */

function centerOnTarget()
{
    let targetIndex =
        findTargetIndex();


    if (targetIndex === -1)
    {
        return;
    }


    let target =
        waypoints[targetIndex];


    map.setView(
        [
            target.latitude,
            target.longitude
        ],
        20
    );
}



/* =========================================================
   FIT ROUTE
   ========================================================= */

function fitRoute()
{
    if (waypoints.length === 0)
    {
        if (roverPosition)
        {
            map.setView(
                roverPosition,
                18
            );
        }

        return;
    }


    let bounds =
        L.latLngBounds([]);


    if (roverPosition)
    {
        bounds.extend(
            roverPosition
        );
    }


    waypoints.forEach(
        point =>
        {
            bounds.extend(
                [
                    point.latitude,
                    point.longitude
                ]
            );
        }
    );


    map.fitBounds(
        bounds,
        {
            padding: [30, 30]
        }
    );
}



/* =========================================================
   MAP CLICK
   ========================================================= */

map.on(
    "click",
    function(e)
    {
        fetch(
            "/map_point",
            {
                method: "POST",

                headers:
                {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(
                        {
                            latitude:
                                e.latlng.lat,

                            longitude:
                                e.latlng.lng
                        }
                    )
            }
        )
        .then(
            () =>
            {
                updatePoints();
            }
        );
    }
);



/* =========================================================
   INITIAL UPDATE
   ========================================================= */

updateGPS();

updatePoints();

updateNavigationStatus();



/* =========================================================
   PERIODIC UPDATES
   ========================================================= */

setInterval(
    updateGPS,
    1000
);


setInterval(
    updatePoints,
    2000
);


setInterval(
    updateNavigationStatus,
    1000
);

