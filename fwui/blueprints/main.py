from flask import (
    Blueprint,
    g,
    render_template,
    request,
    session,
    current_app,
    redirect,
    flash,
    abort,
)
from flask.helpers import url_for

from flask_security import auth_required, current_user

from ..models.setting import Setting
from ..utils import context
from ..structure import STRUCTURE
from ..forms.general import frm_change_zone

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.before_app_request
def before_app_request():

    g.collapsed = request.cookies.get("sidebar-collapsed", False) == "true"

    # Check site is in maintenance mode
    maintenance = Setting().get("maintenance")
    if (
        maintenance
        and current_user.is_authenticated  # noqa: W503
        and not current_user.has_role("admin")  # noqa: W503
    ):
        return render_template("maintenance.html")

    context()


@main_bp.route("/", methods=["GET"])
@auth_required()
def index():
    structure = STRUCTURE["zones"]
    config_mode = session.get("config_mode", "runtime")
    zones = structure[config_mode]["get_all"]()
    obj = structure[config_mode]["get_item"]
    connections = [
        {zone: interfaces}
        for zone in zones
        if len(interfaces := obj(zone).getInterfaces()) > 0
    ]

    sources = [
        {zone: sources} for zone in zones if len(sources := obj(zone).getSources()) > 0
    ]

    actives_zones = current_app.runtime_config.getActiveZones()
    # logs = LogsView()
    # logs.get(request, args, kwargs)
    flash("HelloWorld")
    return render_template(
        "main.html",
        sources=sources,
        actives_zones=actives_zones,
        connections=connections,
        zones=zones,
        frm_change_zone=frm_change_zone(),
    )


@main_bp.route("/logs", methods=["GET"])
@auth_required()
def logs():
    try:
        with open("/dev/kmsg", "r") as f:
            lines = f.readlines()
    except PermissionError as error:
        abort(403, error)
    return render_template("logs.html", lines=lines)


@main_bp.route("/actions", methods=["GET"])
@auth_required()
def actions():
    try:
        if default_zone := request.args.get("default_zone"):
            current_app.runtime_config.setDefaultZone(zone=default_zone)

        if config_mode := request.args.get("config_mode"):
            session["config_mode"] = config_mode

        if denied_log := request.args.get("denied_log"):
            current_app.runtime_config.setLogDenied(denied_log)

        if panic_mode := request.args.get("panic_mode"):
            if panic_mode == "False":
                current_app.runtime_config.enablePanicMode()
            else:
                current_app.runtime_config.disablePanicMode()

        if automatic_helpers := request.args.get("automatic_helpers"):
            current_app.runtime_config.setAutomaticHelpers(automatic_helpers)

        if lockdown_mode := request.args.get("lockdown_mode"):
            if lockdown_mode == "False":
                current_app.runtime_config.enableLockdown()
            else:
                current_app.runtime_config.disableLockdown()

        if request.args.get("reload"):
            current_app.runtime_config.reload()

        if request.args.get("runtimetopermanent"):
            current_app.runtime_config.runtimeToPermanent()

    except Exception as error:
        flash(error)

    return redirect(request.referrer)


@main_bp.route("/changezone", methods=["POST"])
@auth_required()
def changezone(changezone=None):
    structure = STRUCTURE["zones"]
    config_mode = "permanent"
    obj = STRUCTURE["zones"][config_mode]["get_item"]
    s_del = STRUCTURE["zones"]["sources"]["del"]
    s_add = STRUCTURE["zones"]["sources"]["add"]
    i_del = STRUCTURE["zones"]["interfaces"]["del"]
    i_add = STRUCTURE["zones"]["interfaces"]["add"]
    form = frm_change_zone()
    if form.validate_on_submit():
        source = form.cleaned_data["source"]
        new_zone = form.cleaned_data["new_zone"]
        try:
            if form.cleaned_data.get("type") == "interface":
                old_zone = STRUCTURE["zones"][config_mode]["get_zoi"](source)
                old_obj = obj(old_zone)
                new_obj = obj(new_zone)
                getattr(old_obj, i_del)(source)
                getattr(new_obj, i_add)(source)
            if form.cleaned_data.get("type") == "source":
                old_zone = STRUCTURE["zones"][config_mode]["get_zos"](source)
                old_obj = obj(old_zone)
                new_obj = obj(new_zone)
                getattr(old_obj, s_del)(source)
                getattr(new_obj, s_add)(source)

            if config_mode == "runtime" and (
                set_item := structure.get(config_mode, {}).get("set_item")
            ):
                set_item(old_zone, old_obj)
                set_item(new_zone, new_obj)

        except Exception as error:
            flash(error, "error")

    return redirect(url_for("main.index"))
