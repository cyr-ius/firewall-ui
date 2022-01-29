# import base64
from flask import render_template, url_for, redirect, session, request, jsonify


def handle_bad_request(e):
    return render_template("errors/400.html", code=400, message=e), 400


def handle_unauthorized_access(e):
    session["next"] = request.script_root + request.path
    return redirect(url_for("index.login"))


def handle_access_forbidden(e):
    return render_template("errors/403.html", code=403, message=e), 403


def handle_page_not_found(e):
    return render_template("errors/404.html", code=404, message=e), 404


def handle_internal_server_error(e):
    return render_template("errors/500.html", code=500, message=e), 500


def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return (
        jsonify(
            error={
                "errors": e.args,
                "code": 500,
                "message": str(e.args[0]),
                "meta": {"type": "exception"},
            }
        ),
        500,
    )


def handle_firewall_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    if isinstance(e.args[1], type):
        errors = (e.args[0])
        message = str(f"{e.errors[e.args[0]]}")
    else:
        errors = e.args
        message = str(f"{e.errors[e.args[0]]} {e.args[1]}")

    return (
        jsonify(
            error={
                "code": 401,
                "errors": errors,
                "messsage": message,
                "meta": {"type": "firewall"},
            }
        ),
        401,
    )


def handle_dbus_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    json_errors = []
    for er in e.args:
        if isinstance(er, str):
            er = e
        errors = {"title": er.get_dbus_name(), "message": er.get_dbus_message()}
        json_errors.append(errors)

    return (
        jsonify(
            error={
                "code": 401,
                "errors": json_errors,
                "messsage": errors["message"],
                "meta": {"type": "dbus"},
            }
        ),
        401,
    )


class FormException(Exception):
    pass


def handle_form_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return (
        jsonify(
            error={
                "code": 401,
                "errors": e.args,
                "message": str(e.args[0]),
                "meta": {"type": "form"},
            }
        ),
        401,
    )
