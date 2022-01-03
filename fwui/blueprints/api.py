from dbus.exceptions import DBusException
from flask import Blueprint, session
from flask_security import auth_required

from firewall.errors import FirewallError

from ..handle import (
    FormException,
    handle_dbus_exception,
    handle_exception,
    handle_firewall_exception,
    handle_form_exception,
)
from ..utils import get_object
from ..views import FirewallView, SectionView

api_bp = Blueprint("api", __name__, template_folder="templates", url_prefix="/api")

fw_bp = Blueprint(
    "firewall", __name__, template_folder="templates", url_prefix="/v1/firewall"
)
sc_bp = Blueprint(
    "section", __name__, template_folder="templates", url_prefix="/v1/sections"
)
api_bp.register_blueprint(fw_bp)
api_bp.register_blueprint(sc_bp)

fw_bp.add_url_rule(
    "/<string:section>/<string:tabname>", view_func=FirewallView.as_view("tabname")
)
fw_bp.add_url_rule(
    "/<string:section>/<string:item>/<string:tabname>",
    view_func=FirewallView.as_view("item"),
)
fw_bp.errorhandler(500)(handle_exception)
fw_bp.errorhandler(Exception)(handle_exception)
fw_bp.errorhandler(FirewallError)(handle_firewall_exception)
fw_bp.errorhandler(DBusException)(handle_dbus_exception)
fw_bp.errorhandler(FormException)(handle_form_exception)

sc_bp.add_url_rule("<string:section>", view_func=SectionView.as_view("section"))
sc_bp.add_url_rule(
    "<string:section>/<string:item>", view_func=SectionView.as_view("item")
)


@sc_bp.route("<string:section>/<string:item>/reset", methods=["POST"])
@auth_required()
def reset(section, item):
    obj = get_object(section, "permanent", item)
    obj.loadDefaults()
    return {}


sc_bp.errorhandler(500)(handle_exception)
sc_bp.errorhandler(Exception)(handle_exception)
sc_bp.errorhandler(FirewallError)(handle_firewall_exception)
sc_bp.errorhandler(DBusException)(handle_dbus_exception)
sc_bp.errorhandler(FormException)(handle_form_exception)
