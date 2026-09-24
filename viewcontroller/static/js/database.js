/* =========================================================
DATABASE
========================================================= */

let tableData = [];

let currentSort = {
    column: null,
    asc: true
};

let selectedIds = new Set();


/* =========================================================
LOAD POINTS
========================================================= */

async function refresh()
{
    try
    {
        const response = await fetch("/points");
        const data = await response.json();

        tableData = data;

        renderTable();
        updateSummary();
    }
    catch (error)
    {
        console.error(
            "Failed to load points:",
            error
        );
    }
}


/* =========================================================
ADD WAYPOINT
========================================================= */

async function loadCurrentGPS()
{
    try
    {
        const response = await fetch("/gps");

        if (!response.ok)
        {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data = await response.json();


        if (
            data.latitude === null ||
            data.longitude === null
        )
        {
            console.error(
                "GPS position is not available"
            );

            return;
        }


        document
            .getElementById("point-latitude")
            .value =
                Number(data.latitude).toFixed(7);


        document
            .getElementById("point-longitude")
            .value =
                Number(data.longitude).toFixed(7);
    }
    catch (error)
    {
        console.error(
            "Failed to load current GPS position:",
            error
        );
    }
}

async function addWaypoint()
{
    const latitudeInput =
        document.getElementById("point-latitude");

    const longitudeInput =
        document.getElementById("point-longitude");


    const latitude =
        Number(latitudeInput.value);

    const longitude =
        Number(longitudeInput.value);


    if (
        !Number.isFinite(latitude) ||
        !Number.isFinite(longitude)
    )
    {
        console.error(
            "Invalid GPS coordinates"
        );

        return;
    }


    try
    {
        const response = await fetch(
            "/map_point",
            {
                method: "POST",

                headers:
                {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    {
                        latitude: latitude,
                        longitude: longitude
                    }
                )
            }
        );


        if (!response.ok)
        {
            throw new Error(
                `HTTP ${response.status}`
            );
        }


        await refresh();


        latitudeInput.value = "";
        longitudeInput.value = "";
    }
    catch (error)
    {
        console.error(
            "Failed to add waypoint:",
            error
        );
    }
}

/* =========================================================
TABLE
========================================================= */

function renderTable()
{
    const tableBody =
        document.getElementById(
            "database-table-body"
        );


    tableBody.innerHTML = "";


    tableData.forEach(point =>
    {
        const row =
            document.createElement("tr");


        row.innerHTML = `
            <td>${point.latitude}</td>

            <td>${point.longitude}</td>

            <td>${point.time}</td>

            <td>${point.sequence}</td>

            <td>
                <span class="database-state ${point.in_database ? "active" : ""}">
                    ${point.in_database}
                </span>
            </td>

            <td class="visited-column">
                <input
                    class="visited-checkbox"
                    type="checkbox"
                    data-id="${point.uid}"
                    ${point.visited ? "checked" : ""}>
            </td>

            <td class="select-column">
                <input
                    class="point-checkbox"
                    type="checkbox"
                    data-id="${point.uid}"
                    ${selectedIds.has(String(point.uid)) ? "checked" : ""}>
            </td>
        `;


        tableBody.appendChild(row);
    });


    document
        .querySelectorAll(".point-checkbox")
        .forEach(checkbox =>
        {
            checkbox.addEventListener(
                "change",
                updateSelection
            );
        });


    document
        .querySelectorAll(".visited-checkbox")
        .forEach(checkbox =>
        {
            checkbox.addEventListener(
                "change",
                updateVisited
            );
        });


    updateSortIndicators();
}


/* =========================================================
SORTING
========================================================= */

function sortTable(column)
{
    if (currentSort.column === column)
    {
        currentSort.asc = !currentSort.asc;
    }
    else
    {
        currentSort.column = column;
        currentSort.asc = true;
    }


    tableData.sort((a, b) =>
    {
        let x = a[column];
        let y = b[column];


        if (x === null || x === undefined)
        {
            x = "";
        }


        if (y === null || y === undefined)
        {
            y = "";
        }


        if (!isNaN(x) && !isNaN(y))
        {
            x = Number(x);
            y = Number(y);
        }
        else
        {
            x = String(x);
            y = String(y);
        }


        if (x < y)
        {
            return currentSort.asc ? -1 : 1;
        }


        if (x > y)
        {
            return currentSort.asc ? 1 : -1;
        }


        return 0;
    });


    renderTable();
}


function updateSortIndicators()
{
    document
        .querySelectorAll(
            "#database-table th[data-column]"
        )
        .forEach(header =>
        {
            const indicator =
                header.querySelector(
                    ".sort-indicator"
                );


            if (!indicator)
            {
                return;
            }


            if (
                header.dataset.column !==
                currentSort.column
            )
            {
                indicator.textContent = "";
                return;
            }


            indicator.textContent =
                currentSort.asc ? "▲" : "▼";
        });
}


document
    .querySelectorAll(
        "#database-table th[data-column]"
    )
    .forEach(header =>
    {
        header.addEventListener(
            "click",
            () =>
            {
                sortTable(
                    header.dataset.column
                );
            }
        );
    });


/* =========================================================
SELECTION
========================================================= */

function updateSelection(event)
{
    const id =
        String(event.target.dataset.id);


    if (event.target.checked)
    {
        selectedIds.add(id);
    }
    else
    {
        selectedIds.delete(id);
    }


    updateSummary();
}


function getSelectedIds()
{
    return [...selectedIds];
}


function selectAll()
{
    document
        .querySelectorAll(".point-checkbox")
        .forEach(checkbox =>
        {
            checkbox.checked = true;


            selectedIds.add(
                String(checkbox.dataset.id)
            );
        });


    updateSummary();
}


function updateSummary()
{
    const pointCount =
        document.getElementById(
            "point-count"
        );


    const selectedCount =
        document.getElementById(
            "selected-count"
        );


    pointCount.textContent =
        `${tableData.length} POINTS`;


    selectedCount.textContent =
        `${selectedIds.size} SELECTED`;
}


/* =========================================================
VISITED
========================================================= */

async function updateVisited(event)
{
    const checkbox =
        event.target;


    const pointId =
        String(checkbox.dataset.id);


    const visited =
        checkbox.checked;


    try
    {
        const response = await fetch(
            "/db/visited",
            {
                method: "POST",

                headers:
                {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    {
                        id: pointId,
                        visited: visited
                    }
                )
            }
        );


        if (!response.ok)
        {
            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const point =
            tableData.find(
                p =>
                    String(p.uid) === pointId
            );


        if (point)
        {
            point.visited = visited;
        }
    }
    catch (error)
    {
        console.error(
            "Failed to update visited state:",
            error
        );


        /*
         * Backend hiba esetén visszaállítjuk
         * a checkbox eredeti állapotát.
         */

        checkbox.checked = !visited;
    }
}


/* =========================================================
DATABASE OPERATIONS
========================================================= */

async function saveSelected()
{
    const ids = getSelectedIds();


    if (ids.length === 0)
    {
        return;
    }


    try
    {
        await fetch(
            "/db/save",
            {
                method: "POST",

                headers:
                {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    {
                        ids: ids
                    }
                )
            }
        );


        await refresh();
    }
    catch (error)
    {
        console.error(
            "Failed to save points:",
            error
        );
    }
}


async function deleteSelected()
{
    const ids = getSelectedIds();


    if (ids.length === 0)
    {
        return;
    }


    try
    {
        await fetch(
            "/points/delete",
            {
                method: "POST",

                headers:
                {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    {
                        ids: ids
                    }
                )
            }
        );


        selectedIds.clear();

        await refresh();
    }
    catch (error)
    {
        console.error(
            "Failed to delete points:",
            error
        );
    }
}


async function loadDB()
{
    try
    {
        await fetch("/db/load");


        selectedIds.clear();

        await refresh();
    }
    catch (error)
    {
        console.error(
            "Failed to load database:",
            error
        );
    }
}


/* =========================================================
INITIAL LOAD
========================================================= */

refresh();
