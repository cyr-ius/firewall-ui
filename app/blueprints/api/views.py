#
# API Definitions
#
import datetime

from firewall.dbus_utils import dbus_to_python
from flask import abort, jsonify, request, session
from flask.views import MethodView
from flask_security import auth_required


from .handlers import FormException
from ..firewall.structure import STRUCTURE, permanent
from ..firewall.helpers import getObject, setSection, setItem, settings2dict, getLog


class SectionView(MethodView):
    methods = ["GET", "POST", "PUT", "DELETE"]
    decorators = [auth_required()]

    def __init__(self, *args, **kwargs):
        self.config_mode = "permanent"
        self.section = None
        self.item = None
        self.structure = None

    def dispatch_request(self, *args, **kwargs):
        self.section = kwargs.get("section")
        self.item = kwargs.get("item")
        self.structure = STRUCTURE[self.section]
        return super().dispatch_request()

    # Read
    def get(self):
        if self.item is not None:
            obj = getObject(self.section, self.config_mode, self.item)
            return settings2dict(self.section, self.config_mode, obj, self.structure)

    # Create
    def post(self):
        form = self.structure["settings"]["form"]()
        if form.validate_on_submit():
            name = form.cleaned_data.pop("name")
            settings = form.cleaned_data.values()
            if self.section in ["zones", "services"]:
                settings = form.cleaned_data
            getattr(permanent, self.structure["settings"]["add"])(name, settings)
            return jsonify(form.cleaned_data)
        raise FormException(form.errors)

    # Modify
    def put(self):
        form = self.structure["settings"]["form"]()
        obj = getObject(self.section, self.config_mode, self.item)
        if form.validate_on_submit():
            settings = setSection(
                self.config_mode, self.section, obj, form.cleaned_data
            )
            obj.update(settings)
            return jsonify(form.cleaned_data)
        raise FormException(form.errors)

    # Modify
    def delete(self):
        obj = getObject(self.section, self.config_mode, self.item)
        obj.remove()
        return {}


class FirewallView(MethodView):
    methods = ["GET", "POST", "PUT", "DELETE"]
    decorators = [auth_required()]

    def __init__(self, *args, **kwargs):
        self.config_mode = request.args.get("config_mode", session.get("config_mode"))
        self.section = None
        self.item = None
        self.tabname = None
        self.structure = None
        self.obj = None

    def dispatch_request(self, *args, **kwargs):
        self.section = kwargs["section"]
        self.item = kwargs.get("item")
        self.tabname = kwargs.get("tabname")
        self.structure = STRUCTURE[self.section]
        self.obj = getObject(self.section, self.config_mode, self.item)
        return super().dispatch_request()

    # Read
    def get(self):
        settings = getattr(self.obj, self.structure[self.tabname]["list"])()
        return jsonify(dbus_to_python(settings))

    # Create
    def post(self):
        form = self.structure[self.tabname]["form"]()
        if form.validate_on_submit():
            return setItem(
                self.obj,
                self.section,
                self.item,
                self.tabname,
                self.structure,
                form,
                "add",
            )
        raise FormException(form.errors)

    # Modify
    def put(self):
        form = self.structure[self.tabname]["form"]()
        if form.validate_on_submit():
            setItem(
                self.obj,
                self.section,
                self.item,
                self.tabname,
                self.structure,
                form,
                "del",
            )
            return setItem(
                self.obj,
                self.section,
                self.item,
                self.tabname,
                self.structure,
                form,
                "add",
            )
        raise FormException(form.errors)

    # Modify
    def delete(self):
        form = self.structure[self.tabname]["form"]()
        if form.validate_on_submit():
            return setItem(
                self.obj,
                self.section,
                self.item,
                self.tabname,
                self.structure,
                form,
                "del",
            )
        raise FormException(form.errors)


class LogView(MethodView):
    methods = ["GET"]
    decorators = [auth_required()]

    # Read
    def get(self, *args, **xargs):

        log = xargs.get("journal")
        query = xargs.get("query", "")
        if log != "system" and log != "firewall":
            abort(500)
        if start := request.args.get("start"):
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        if end := request.args.get("end"):
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        log = getLog(log, query, start, end)

        return jsonify(log)
