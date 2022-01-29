# import base64
from flask import jsonify


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
        errors = e.args[0]
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
