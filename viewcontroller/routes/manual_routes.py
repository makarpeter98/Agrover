from flask import Blueprint, render_template, request, jsonify



def manual_routes(queue):


    bp = Blueprint(
        "manual",
        __name__
    )



    @bp.route("/")
    def index():

        return render_template(
            "manual.html"
        )



    @bp.route(
        "/command",
        methods=["POST"]
    )
    def command():


        data = request.json


        queue.put(
            data["command"]
        )


        return jsonify(
        {
            "ok": True
        })



    return bp
