from flask_babel import gettext as _
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,

)
from wtforms.validators import Optional, Required
from ..consts import TARGET, TYPESETS
from .frm import frm


class frm_zone(frm):
    name = StringField(label=_("Name"), validators=[Required()])
    version = StringField(label=_("Version"), validators=[Optional()])
    short = StringField(label=_("Short"), validators=[Optional()])
    description = TextAreaField(label=_("Description"), validators=[Optional()])
    target = SelectField(label=_("Target"), choices=TARGET)
    submit = SubmitField(label=_("Add"))

    def clean(self):
        super().clean()
        self.name = self.cleaned_data.get("name")


class frm_service(frm):
    name = StringField(label=_("Name"), validators=[Required()])
    version = StringField(label=_("Version"), validators=[Optional()])
    short = StringField(label=_("Short"), validators=[Optional()])
    description = TextAreaField(label=_("Description"), validators=[Optional()])
    submit = SubmitField(label=_("Add"))

    def clean(self):
        super().clean()
        self.name = self.cleaned_data.get("name")


class frm_ipset(frm):
    name = StringField(label=_("Name"), validators=[Required()])
    version = StringField(label=_("Version"), validators=[Optional()])
    short = StringField(label=_("Short"), validators=[Optional()])
    description = TextAreaField(label=_("Description"), validators=[Optional()])
    TYPESETS.append(("", "---"))
    hashtype = SelectField(label=_("Hashtype"), choices=TYPESETS, default=None)
    family = SelectField(
        label=_("Family"), choices=(("inet", "inet"), ("inet6", "inet6"))
    )
    timeout = StringField(label=_("Timeout"), validators=[Optional()])
    hashsize = StringField(label=_("Hashsize"), validators=[Optional()])
    maxelem = StringField(label=_("Max elem"), validators=[Optional()])
    submit = SubmitField(label=_("Add"))

    def clean(self):
        super().clean()
        self.name = self.cleaned_data.get("name")
        if self.cleaned_data["hashtype"] == "hash:mac":
            self.cleaned_data.pop("family")

        options = {}
        for item in ["family", "timeout", "hashsize", "maxelem"]:
            if value := self.cleaned_data.pop(item, None):
                options.update({item: value})

        self.cleaned_data.update({"options": options, "inputs": []})


class frm_icmptype(frm):
    name = StringField(label=_("Name"), validators=[Required()])
    version = StringField(label=_("Version"), validators=[Optional()])
    short = StringField(label=_("Short"), validators=[Optional()])
    description = TextAreaField(label=_("Description"), validators=[Optional()])
    submit = SubmitField(label=_("Add"))

    def clean(self):
        super().clean()
        self.name = self.cleaned_data.get("name")
        self.cleaned_data.update({"destination": []})


class frm_helper(frm):
    name = StringField(label=_("Name"), validators=[Required()])
    version = StringField(label=_("Version"), validators=[Optional()])
    short = StringField(label=_("Short"), validators=[Optional()])
    description = TextAreaField(label=_("Description"), validators=[Optional()])
    family = SelectField(
        label=_("Family"),
        choices=[("", "all"), ("ipv4", "ipv4"), ("ipv6", "ipv6")],
        validators=[Optional()],
    )
    module = StringField(label=_("Module"), default="nf_conntrack_")
    submit = SubmitField(label=_("Add"))

    def clean(self):
        super().clean()
        self.name = self.cleaned_data.get("name")
        self.cleaned_data.update({"ports": []})
