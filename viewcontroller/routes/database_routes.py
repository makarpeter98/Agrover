from flask import jsonify, request



def database_routes(
    app,
    get_points,
    save,
    load,
    clear
):


    @app.route("/database")
    def database():


        return """
        <h2>Database</h2>


        <button onclick="loadDB()">
        Betöltés DB-ből
        </button>


        <button onclick="saveDB()">
        Kijelöltek mentése
        </button>


        <button onclick="clearPoints()">
        Kijelöltek törlése
        </button>


        <button onclick="selectAll()">
        Összes kijelöl
        </button>


        <table border="1" id="table">

        </table>


<script>


async function loadDB(){

await fetch("/db/load")

location.reload()

}



async function saveDB(){

await fetch("/db/save",
{
method:"POST"
})

}



async function clearPoints(){

await fetch("/points/clear",
{
method:"POST"
})

location.reload()

}



async function selectAll(){

await fetch("/points/select",
{
method:"POST"
})

location.reload()

}


async function refresh(){


let r =
await fetch("/points")


let data =
await r.json()


let t =
document.getElementById("table")


t.innerHTML =
"<tr>\
<th>LAT</th>\
<th>LON</th>\
<th>TIME</th>\
<th>VISITED</th>\
<th>SEQ</th>\
<th>DB</th>\
</tr>"



data.forEach(p=>{


t.innerHTML +=
`
<tr>

<td>${p.latitude}</td>

<td>${p.longitude}</td>

<td>${p.time}</td>

<td>${p.visited}</td>

<td>${p.sequence}</td>

<td>${p.in_database}</td>

</tr>
`

})


}


refresh()



</script>
"""
