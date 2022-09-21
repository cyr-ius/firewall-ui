import datetime
from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    escape,
)
from flask.helpers import url_for
from flask_security import auth_required, current_user, permissions_required

from .forms import frm_change_zone, frm_logs
from .models import Setting
from ..firewall.structure import STRUCTURE
from ..firewall.helpers import context, getLog

main_bp = Blueprint("main", __name__)


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
    return render_template(
        "main.html",
        sources=sources,
        actives_zones=actives_zones,
        connections=connections,
        zones=zones,
        frm_change_zone=frm_change_zone(),
    )


@main_bp.route("/logs", methods=["GET", "POST"])
@auth_required()
@permissions_required("logs-read")
def logs():
    journal = {}
    if request.method == "GET":
        journal = getLog("firewall")

    if request.method == "POST":
        query = request.form.get("search")
        level = request.form.get("level")
        log = request.form.get("type", "denied")
        if start := request.form.get("date_start"):
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M")
        if end := request.form.get("date_end"):
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M")
        journal = getLog(log, query, start, end, level)

    return render_template("logs.html", journal=journal, form=frm_logs())


@main_bp.route("/actions", methods=["GET"])
@auth_required()
def actions():
    try:
        if (default_zone := request.args.get("default_zone")) and current_user.has_permission("changezone"):
            current_app.runtime_config.setDefaultZone(zone=default_zone)

        if config_mode := request.args.get("config_mode"):
            session["config_mode"] = config_mode

        if (denied_log := request.args.get("denied_log")) and current_user.has_permission("logs-write"):
            current_app.runtime_config.setLogDenied(denied_log)

        if (panic_mode := request.args.get("panic_mode")) and current_user.has_permission("panicmode"):
            if panic_mode == "False":
                current_app.runtime_config.enablePanicMode()
            else:
                current_app.runtime_config.disablePanicMode()

        if (automatic_helpers := request.args.get("automatic_helpers")) and current_user.has_permission("automatichelper"):
            current_app.runtime_config.setAutomaticHelpers(automatic_helpers)

        if (lockdown_mode := request.args.get("lockdown_mode")) and current_user.has_permission("lockdown"):
            if lockdown_mode == "False":
                current_app.runtime_config.enableLockdown()
            else:
                current_app.runtime_config.disableLockdown()

        if request.args.get("reload"):
            current_app.runtime_config.reload()

        if request.args.get("runtimetopermanent") and current_user.has_permission("permanent"):
            current_app.runtime_config.runtimeToPermanent()

    except Exception as error:
        flash(error)

    return redirect(escape(request.referrer))


@main_bp.route("/changezone", methods=["POST"])
@auth_required()
@permissions_required("changezone-write")
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
