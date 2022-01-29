from flask import Blueprint

from .views import GenericView, RedirectView

fwl_bp = Blueprint("firewall", __name__, template_folder="templates", url_prefix="/fw")

fwl_bp.add_url_rule(
    "/<string:section>/", view_func=RedirectView.as_view("redirect_to_main", url="/")
)
fwl_bp.add_url_rule(
    "<string:section>/<string:item>/<string:tabname>",
    view_func=GenericView.as_view("generic_tab"),
)
fwl_bp.add_url_rule(
    "<string:section>/<string:tabname>",
    view_func=GenericView.as_view("specific_tab"),
)

# Redirect
fwl_bp.add_url_rule(
    "zones/<string:item>/",
    view_func=RedirectView.as_view("redirect_to_services", url="services"),
)
fwl_bp.add_url_rule(
    "services/<string:item>/",
    view_func=RedirectView.as_view("redirect_to_port", url="ports"),
)
fwl_bp.add_url_rule(
    "ipsets/<string:item>/",
    view_func=RedirectView.as_view("redirect_to_input_create", url="inputs"),
)
fwl_bp.add_url_rule(
    "icmptypes/<string:item>/",
    view_func=RedirectView.as_view("redirect_to_destination", url="destination"),
)
fwl_bp.add_url_rule(
    "helpers/<string:item>/",
    view_func=RedirectView.as_view("redirect_helpers", url="ports"),
)
fwl_bp.add_url_rule(
    "directconfigs/",
    view_func=RedirectView.as_view("directconfigs", url="chains"),
)
fwl_bp.add_url_rule(
    "whitelists/",
    view_func=RedirectView.as_view("whitelists", url="context"),
)
