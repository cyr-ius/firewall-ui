from firewall.dbus_utils import dbus_to_python
from flask import abort, redirect, render_template, session
from flask.views import MethodView, View
from flask_security import auth_required


from .structure import STRUCTURE
from .utils import get_object, setItem, settings2dict


class GenericView(MethodView):
    methods = ["GET", "POST"]
    decorators = [auth_required()]

    def __init__(self, *args, **kwargs):
        self.config_mode = session.get("config_mode")
        self.section_form = (
            self.template
        ) = (
            self.form
        ) = self.obj = self.structure = self.tabname = self.item = self.section = None

    def dispatch_request(self, *args, **kwargs):
        self.section = kwargs.get("section")
        self.item = kwargs.get("item")
        self.tabname = kwargs.get("tabname")
        self.structure = STRUCTURE[self.section]
        self.template = (
            f"{self.section}.html"
            if self.tabname is None
            else f"{self.section}/tab_{self.tabname}.html"
        )

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
        settings = dbus_to_python(settings)
        return render_template(
            self.template,
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
            self.template,
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
