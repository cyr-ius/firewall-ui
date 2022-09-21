from dbus.exceptions import DBusException
from flask import Blueprint
from flask_security import auth_required

from firewall.errors import FirewallError

from .handlers import (
    FormException,
    handle_dbus_exception,
    handle_exception,
    handle_firewall_exception,
    handle_form_exception,
)
from ..firewall.helpers import getObject
from .views import FirewallView, LogView, SectionView

api_bp = Blueprint("api", __name__, url_prefix="/api")

fw_bp = Blueprint(
    "firewall", __name__, template_folder="templates", url_prefix="/v1/firewall"
)
sc_bp = Blueprint(
    "section", __name__, template_folder="templates", url_prefix="/v1/sections"
)
log_bp = Blueprint("log", __name__, template_folder="templates", url_prefix="/v1/logs")
api_bp.register_blueprint(fw_bp)
api_bp.register_blueprint(sc_bp)
api_bp.register_blueprint(log_bp)

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
    obj = getObject(section, "permanent", item)
    obj.loadDefaults()
    return {}


sc_bp.errorhandler(500)(handle_exception)
sc_bp.errorhandler(Exception)(handle_exception)
sc_bp.errorhandler(FirewallError)(handle_firewall_exception)
sc_bp.errorhandler(DBusException)(handle_dbus_exception)
sc_bp.errorhandler(FormException)(handle_form_exception)

log_bp.add_url_rule("<string:journal>", view_func=LogView.as_view("logs"))
log_bp.add_url_rule(
    "<string:journal>/<string:query>", view_func=LogView.as_view("log_query")
)
log_bp.errorhandler(Exception)(handle_exception)
