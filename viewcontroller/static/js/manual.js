/* =========================================================
   MANUAL COMMAND
   ========================================================= */

function send(cmd)
{
    fetch(
        "/command",
        {
            method: "POST",

            headers:
            {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(
                {
                    command: cmd
                }
            )
        }
    );
}



/* =========================================================
   START NAVIGATION
   ========================================================= */

function startNav()
{
    fetch(
        "/nav/start",
        {
            method: "POST"
        }
    );
}



/* =========================================================
   STOP NAVIGATION
   ========================================================= */

function stopNav()
{
    fetch(
        "/nav/stop",
        {
            method: "POST"
        }
    );
}



/* =========================================================
   UPDATE NAVIGATION STATUS
   ========================================================= */

function updateNavStatus()
{
    fetch("/nav/status")

        .then(
            response =>
                response.json()
        )

        .then(
            data =>
            {

                /* -----------------------------------------
                   STATUS
                   ----------------------------------------- */

                document
                    .getElementById("nav-status")
                    .textContent =
                        data.state ?? "-";



                /* -----------------------------------------
                   COMMAND
                   ----------------------------------------- */

                document
                    .getElementById("nav-command")
                    .textContent =
                        data.command ?? "-";



                /* -----------------------------------------
                   CURRENT GPS POSITION
                   ----------------------------------------- */

                if (data.current_position)
                {
                    const position =
                        data.current_position;


                    document
                        .getElementById("gps-position")
                        .textContent =
                            `${position.latitude.toFixed(7)}, ` +
                            `${position.longitude.toFixed(7)}`;
                }



                /* -----------------------------------------
                   TARGET POSITION
                   ----------------------------------------- */

                if (data.target)
                {
                    const target =
                        data.target;


                    document
                        .getElementById("nav-target")
                        .textContent =
                            `${target.latitude.toFixed(7)}, ` +
                            `${target.longitude.toFixed(7)}`;
                }



                /* -----------------------------------------
                   DISTANCE
                   ----------------------------------------- */

                if (data.distance != null)
                {
                    document
                        .getElementById("nav-distance")
                        .textContent =
                            data.distance.toFixed(2) + " m";
                }



                /* -----------------------------------------
                   HEADING
                   ----------------------------------------- */

                if (data.heading)
                {
                    const heading =
                        data.heading;


                    document
                        .getElementById("heading-current")
                        .textContent =
                            heading.current + " deg";


                    document
                        .getElementById("heading-target")
                        .textContent =
                            heading.target + " deg";


                    document
                        .getElementById("heading-difference")
                        .textContent =
                            heading.difference + " deg";
                }
                
                /* -----------------------------------------
                   NAVIGATION SETTINGS
                   ----------------------------------------- */

                if (data.navigation_settings)
                {
                    document
                        .getElementById(
                            "nav-arrival-distance-limit"
                        )
                        .textContent =
                            data.navigation_settings.arrival_distance_limit + " m";


                    document
                        .getElementById(
                            "nav-heading-tolerance"
                        )
                        .textContent =
                            data.navigation_settings.heading_tolerance + " deg";
                }

            }
        )

        .catch(
            error =>
            {
                console.log(
                    "Navigation status error:",
                    error
                );
            }
        );
}



/* =========================================================
   INITIAL STATUS UPDATE
   ========================================================= */

updateNavStatus();



/* =========================================================
   PERIODIC STATUS UPDATE
   ========================================================= */

setInterval(
    updateNavStatus,
    1000
);

