from flask import Blueprint


def api_routes(
    gps_handler,
    command_queue
):

    bp = Blueprint(
        "api",
        __name__
    )


    return bp
