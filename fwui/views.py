from flask import jsonify, redirect, render_template, session, request, abort
from flask.views import MethodView, View
from firewall.dbus_utils import dbus_to_python

from .structure import STRUCTURE, permanent
from .utils import fw_template, get_object, settings2dict, saveSection, setItem
from .handle import FormException
from flask_security import auth_required


class GenericView(MethodView):
    methods = ["GET", "POST"]
    decorators = [auth_required()]

    def __init__(self, *args, **kwargs):
        self.config_mode = session.get("config_mode")
        self.section_form = (
            self.template_name
        ) = (
            self.form
        ) = self.obj = self.structure = self.tabname = self.item = self.section = None

    def dispatch_request(self, *args, **kwargs):
        self.section = kwargs.get("section")
        self.item = kwargs.get("item")
        self.tabname = kwargs.get("tabname")
        self.structure = STRUCTURE[self.section]
        self.template_name = fw_template(self.section, self.tabname)

        try:
            self.obj = get_object(self.section, self.config_mode, self.item)
            self.form = self.structure[self.tabname]["form"]()
        except Exception:
            abort(404)

        if self.item:
            section_settings = settings2dict(
                self.section, self.config_mode, self.obj, self.structure
            )
            section_settings.update({"name": self.item})
            self.section_form = self.structure["settings"]["form"](
                data=section_settings
            )

        return super().dispatch_request()

    def get(self):

        settings = getattr(self.obj, self.structure[self.tabname]["list"])()
        return render_template(
            self.template_name,
            section=self.section,
            item=self.item,
            tabname=self.tabname,
            form=self.form,
            settings=settings,
            section_form=self.section_form,
        )

    def post(self):

        if self.form.validate_on_submit():
            setItem(
                self.obj,
                self.section,
                self.item,
                self.tabname,
                self.structure,
                self.form,
                "del",
            )

        settings = getattr(self.obj, self.structure[self.tabname]["list"])()

        return render_template(
            self.template_name,
            section=self.section,
            item=self.item,
            tabname=self.tabname,
            form=self.form,
            settings=settings,
            section_form=self.section_form,
        )


class RedirectView(View):
    decorators = [auth_required()]

    def __init__(self, url=None, tabname=None):
        self.url = url

    def dispatch_request(self, *args, **kwargs):
        return redirect(self.url)


#
# API Definitions
#
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
            obj = get_object(self.section, self.config_mode, self.item)
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
        obj = get_object(self.section, self.config_mode, self.item)
        if form.validate_on_submit():
            settings = saveSection(self.config_mode, self.section, obj, form.cleaned_data)
            obj.update(settings)
            return jsonify(form.cleaned_data)
        raise FormException(form.errors)

    # Modify
    def delete(self):
        obj = get_object(self.section, self.config_mode, self.item)
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
        self.obj = get_object(self.section, self.config_mode, self.item)
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
