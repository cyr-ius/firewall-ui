from flask import session
from flask_babel import gettext as _
from flask_wtf.form import FlaskForm
from wtforms import (
    BooleanField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    FormField,
)
from wtforms.validators import IPAddress, Optional, MacAddress, Required
from wtforms.widgets import CheckboxInput

from .validators import NumberRange, PortRange, Command, Uid, Protocol, Interface
from ..consts import (
    ACTIONS,
    CHAINS_TABLE,
    DESTINATIONS,
    ELEMENTS,
    ICMPTYPES,
    INTERVAL_UNIT,
    IPSETS,
    IPV,
    LOGLEVELS,
    MODULES,
    PROTOCOLS,
    PROTOCOLS_SHORT,
    REJECT_IPV4,
    REJECT_IPV6,
    SERVICES,
    SOURCES,
)


class frm(FlaskForm):
    def clean(self):
        pass

    def populate(self):
        self.cleaned_data = self.data.copy()
        self.cleaned_data.pop("csrf_token", None)
        self.cleaned_data.pop("submit", None)
        self.cleaned_data = {k: str(v) for k, v in self.cleaned_data.items()}

    def validate_on_submit(self):
        self.populate()
        self.clean()
        return super().validate_on_submit()


class frm_services(frm):
    service = SelectField(
        label=_("Service"),
        choices=SERVICES,
        coerce=str,
        render_kw={"class": "form-select"},
    )


class frm_ports(frm):
    port = StringField(
        label=_("Port or range"),
        validators=[Required(), PortRange(min=1, max=65535)],
        render_kw={"class": "form-control", "placeholder": _("Port or range")},
    )
    protocol = SelectField(
        label=_("Protocol"),
        validators=[Protocol()],
        choices=PROTOCOLS_SHORT,
        render_kw={"class": "form-select"},
    )


class frm_protocols(frm):
    protocol = SelectField(
        label=_("Protocol"),
        choices=PROTOCOLS,
        validators=[Optional()],
        validate_choice=False,
        render_kw={"class": "form-select", "placeholder": _("Protocol")},
    )
    other = StringField(
        label=_("Other protocols"),
        validators=[Optional()],
        render_kw={"class": "form-control", "placeholder": _("Other")},
    )

    def clean(self):
        super().clean()
        other = self.cleaned_data.pop("other")
        if other != "":
            self.cleaned_data.update({"protocol": other})


class frm_sourceports(frm):
    port = StringField(
        label=_("Port/Interval"),
        validators=[Required(), NumberRange(min=1, max=65535)],
        render_kw={"class": "form-control", "placeholder": _("Port")},
    )
    protocol = SelectField(
        label=_("Protocol"),
        choices=PROTOCOLS_SHORT,
        render_kw={"class": "form-select", "placeholder": _("Protocol")},
    )


class frm_nat(frm):
    nat = BooleanField(
        label=_("Enable Forward"),
        validators=[Optional()],
        render_kw={"class": "form-check-input", "onchange": "submit();"},
    )

    def clean(self):
        super().clean()
        self.cleaned_data = {}


class frm_pat(frm):
    port = IntegerField(
        label=_("Port"),
        validators=[NumberRange(min=1, max=65535)],
        render_kw={"class": "form-control", "placeholder": _("Port")},
    )
    protocol = SelectField(
        label=_("Protocol"),
        choices=PROTOCOLS_SHORT,
        render_kw={"class": "form-select", "placeholder": _("Protocol")},
    )
    redirect = SelectField(
        choices=(("local", "Local redirect"), ("port", "Port redirect")),
        render_kw={"class": "form-select"},
    )
    toport = IntegerField(
        label=_("To port"),
        validators=[Optional(), NumberRange(min=1, max=65535)],
        render_kw={"class": "form-control", "placeholder": _("To port")},
    )
    toaddr = StringField(
        label=_("To ip address"),
        validators=[Optional(), IPAddress()],
        render_kw={"class": "form-control", "placeholder": _("To ip address")},
    )

    def clean(self):
        super().clean()
        if session.get("config_mode") == "runtime":
            self.cleaned_data.update(
                {
                    "to_port": self.cleaned_data.pop("toport"),
                    "to_addr": self.cleaned_data.pop("toaddr"),
                }
            )
        self.cleaned_data.pop("redirect", None)


class frm_icmp_filters(frm):
    icmptype = SelectField(
        label=_("icmp"), choices=ICMPTYPES, render_kw={"class": "form-select"}
    )


class frm_interfaces(frm):
    interface = StringField(
        label=_("Interface"),
        validators=[Required(), Interface()],
        render_kw={"class": "form-control", "placeholder": _("Interface")},
    )


class frm_sources(frm):
    source_choice = SelectField(
        label=_("Source"),
        choices=SOURCES,
        validators=[Optional()],
        render_kw={"class": "form-select"},
    )
    source_ip = StringField(
        label=_("IP Source"),
        validators=[Optional(), IPAddress(ipv4=True, ipv6=True)],
        render_kw={
            "class": "form-control",
            "placeholder": _("IP Source"),
            "style": "display:none",
        },
    )
    source_mac = StringField(
        label=_("Mac Address"),
        validators=[Optional(), MacAddress()],
        default="",
        render_kw={
            "class": "form-control",
            "placeholder": _("Mac address"),
            "style": "display:none",
        },
    )
    source_ipset = SelectField(
        label=_("IPset"),
        choices=IPSETS,
        validators=[Optional()],
        render_kw={
            "style": "display:none",
            "placeholder": _("IPset"),
            "class": "form-select",
        },
    )
    source = HiddenField(label=_("Source"), validators=[Optional()])

    def clean(self):
        super().clean()
        refs = {"IP": "source_ip", "MAC": "source_mac", "ipset": "source_ipset"}
        selectSource = refs.get(self.cleaned_data.get("source_choice"), "source")
        self.cleaned_data = {"source": self.cleaned_data.get(selectSource)}


class frm_modules(frm):
    module = SelectField(
        label=_("Module"),
        choices=MODULES,
        validators=[Optional()],
        render_kw={"class": "form-select"},
    )


class frm_destination(frm):
    destination = SelectField(
        label=_("Destination"),
        choices=DESTINATIONS,
        validators=[Required()],
        render_kw={"class": "form-select"},
    )
    address = StringField(
        label=_("IP Address"),
        validators=[Required(), IPAddress(ipv4=True, ipv6=True)],
        render_kw={"class": "form-select", "placeholder": _("IP address")},
    )


class frm_ipsets(frm):
    entry = StringField(
        label=_("Entry"), render_kw={"class": "form-control", "placeholder": _("Entry")}
    )


class frm_icmp_types(frm):
    destination = SelectField(
        label=_("Destination"), choices=DESTINATIONS, render_kw={"class": "form-select"}
    )


class frm_chains(frm):
    ipv = SelectField(label=_("IPV"), choices=IPV, render_kw={"class": "form-select"})
    table = SelectField(
        label=_("Table"), choices=CHAINS_TABLE, render_kw={"class": "form-select"}
    )
    chain = StringField(
        label=_("Chain"),
        validators=[Required()],
        render_kw={"class": "form-control", "placeholder": _("Chain")},
    )


class frm_rules(frm_chains):
    priority = IntegerField(
        label=_("Priority"),
        validators=[Required()],
        render_kw={"class": "form-control", "placeholder": _("Priority")},
    )
    args = StringField(
        label=_("Args"), render_kw={"class": "form-control", "placeholder": _("Args")}
    )


class frm_passthroughs(frm):
    ipv = SelectField(label=_("IPV"), choices=IPV, render_kw={"class": "form-select"})
    args = StringField(
        label=_("Args"),
        validators=[Required()],
        render_kw={"class": "form-control", "placeholder": _("Args")},
    )


class frm_contexts(frm):
    context = StringField(
        label=_("Context"),
        validators=[Required()],
        render_kw={"class": "form-control", "placeholder": _("Context")},
    )


class frm_commands(frm):
    command = StringField(
        label=_("Command"),
        validators=[Command(), Required()],
        render_kw={"class": "form-control", "placeholder": _("Command")},
    )


class frm_users(frm):
    user = StringField(
        label=_("User"),
        validators=[Required()],
        render_kw={"class": "form-control", "placeholder": _("User")},
    )


class frm_uids(frm):
    uid = IntegerField(
        label=_("UID"),
        validators=[Required(), Uid()],
        render_kw={"class": "form-control", "placeholder": _("UID")},
    )

    def clean(self):
        uid = int(self.cleaned_data["uid"])
        self.cleaned_data = {"uid": uid}
        return self.cleaned_data


class frm_icmp(frm):
    icmptype = SelectField(
        label=_("icmp"), choices=ICMPTYPES, render_kw={"class": "form-select"}
    )


class frm_rich_rules(frm):
    DESTINATIONS.append(("", "All"))
    family = SelectField(
        label=_("Family"),
        choices=DESTINATIONS,
        default=None,
        validators=[Optional()],
        render_kw={"class": "form-select"},
    )
    priority = IntegerField(label=_("Priority"), render_kw={"class": "form-control"})

    ELEMENTS.append(("---", "---"))
    element_level = SelectField(
        label=_("Level"),
        choices=ELEMENTS,
        validators=[Required()],
        default="---",
        render_kw={"class": "form-select"},
    )

    element_level_service = FormField(
        frm_services, render_kw={"style": "display: none;"}
    )
    element_level_port = FormField(frm_ports, render_kw={"style": "display: none;"})
    element_level_protocol = FormField(
        frm_protocols, render_kw={"style": "display: none;"}
    )
    element_level_icmptype = FormField(
        frm_icmp_types, render_kw={"style": "display: none;"}
    )
    element_level_icmpblock = FormField(
        frm_icmp_filters, render_kw={"style": "display: none;"}
    )
    element_level_forwardport = FormField(
        frm_pat, render_kw={"style": "display: none;"}
    )
    element_level_sourceport = FormField(
        frm_sourceports, render_kw={"style": "display: none;"}
    )

    ICMPTYPES.append(("---", "---"))
    element_icmpblock = SelectField(
        label=_("Icmpblock"),
        choices=ICMPTYPES,
        validators=[Optional()],
        default="---",
        render_kw={"class": "form-select"},
    )
    element_icmptype = SelectField(
        label=_("Icmptype"),
        choices=ICMPTYPES,
        validators=[Optional()],
        render_kw={"class": "form-select"},
    )

    action = BooleanField(
        label=_("Action"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    action_level = SelectField(
        label=_("Level"),
        choices=ACTIONS,
        validators=[Optional()],
        render_kw={"class": "form-select"},
    )
    action_type = BooleanField(
        label=_("Type"),
        widget=CheckboxInput(),
        validators=[Optional()],
        render_kw={"class": "form-check-input", "style": "display: none;"},
    )
    REJECT_IPV4.append(("---", "---"))
    action_type_ipv4 = SelectField(
        label=_("IPv4"),
        choices=REJECT_IPV4,
        validators=[Optional()],
        default="---",
        render_kw={"class": "form-select", "style": "display: none;"},
    )
    REJECT_IPV6.append(("---", "---"))
    action_type_ipv6 = SelectField(
        label=_("IPv6"),
        choices=REJECT_IPV6,
        validators=[Optional()],
        default="---",
        render_kw={"class": "form-select", "style": "display: none;"},
    )
    action_mark = StringField(
        label=_("Mark"),
        validators=[Optional()],
        render_kw={"class": "form-control", "style": "display: none;"},
    )
    action_mask = StringField(
        label=_("Mask"),
        validators=[Optional()],
        render_kw={"class": "form-control", "style": "display: none;"},
    )

    action_limit = BooleanField(
        label=_("Limit"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    action_value = IntegerField(
        label=_("Value"),
        validators=[Optional()],
        render_kw={"class": "form-control", "style": "display: none;"},
    )
    action_unit = SelectField(
        label=_("Unit"),
        choices=INTERVAL_UNIT,
        validators=[Optional()],
        render_kw={"class": "form-select", "style": "display: none;"},
    )

    SOURCES.append(("---", "---"))
    src = SelectField(
        label=_("Source"),
        choices=SOURCES,
        validators=[Optional()],
        default="---",
        render_kw={"class": "form-select"},
    )
    src_ip = StringField(
        label=_("IP Source"),
        validators=[Optional(), IPAddress(ipv4=True, ipv6=True)],
        render_kw={"class": "form-control"},
    )
    src_reverse = BooleanField(
        label=_("Reverse"),
        false_values="",
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    src_mac = StringField(
        label=_("MAC Address"),
        validators=[Optional(), MacAddress()],
        render_kw={"class": "form-control"},
    )

    IPSETS.append(("---", "---"))
    src_ipset = SelectField(
        label=_("IPSet"),
        choices=IPSETS,
        validators=[Optional()],
        default="---",
        render_kw={"class": "form-select"},
    )

    dst_ip = StringField(
        label=_("IP Destination"),
        validators=[Optional(), IPAddress(ipv4=True, ipv6=True)],
        render_kw={"class": "form-control"},
    )
    dst_reverse = BooleanField(
        label=_("Reverse"),
        false_values="",
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )

    LOGLEVELS.append(("---", "---"))
    log = BooleanField(
        label=_("Logs"),
        false_values="",
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    log_level = SelectField(
        label=_("Level"),
        choices=LOGLEVELS,
        validators=[Optional()],
        default="---",
        render_kw={"class": "form-select"},
    )
    log_prefix = StringField(
        label=_("Prefix"), validators=[Optional()], render_kw={"class": "form-control"}
    )
    log_limit = BooleanField(
        label=_("Limit"),
        false_values="",
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    log_value = IntegerField(
        label=_("Value"),
        validators=[Optional()],
        render_kw={"class": "form-control", "style": "display: none;"},
    )
    log_unit = SelectField(
        label=_("Unit"),
        choices=INTERVAL_UNIT,
        validators=[Optional()],
        render_kw={"class": "form-control", "style": "display: none;"},
    )

    audit = BooleanField(
        label=_("Audit"),
        false_values="",
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    audit_limit = BooleanField(
        label=_("Limit"),
        false_values="",
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    audit_value = IntegerField(
        label=_("Value"),
        validators=[Optional()],
        render_kw={"class": "form-control", "style": "display: none;"},
    )
    audit_unit = SelectField(
        label=_("Unit"),
        choices=INTERVAL_UNIT,
        validators=[Optional()],
        render_kw={"class": "form-select", "style": "display: none;"},
    )

    def clean(self):
        clean_post = self.cleaned_data.copy()
        for k, v in clean_post.items():
            if v is False or v is None or v == "":
                self.cleaned_data.pop(k)

        element = source = destination = action = ""

        if family := clean_post.get("family"):
            family = f'family="{family}"'

        if clean_post.get("element_level") and (svc := clean_post["element_service"]):
            element = f'service name="{svc}"'

        if (
            (src := clean_post.get("src_ip"))
            or (src := clean_post.get("src_mac"))  # noqa: W503
            or (src := clean_post.get("src_ipset"))  # noqa: W503
        ):
            reverse = clean_post.get("src_reverse")
            source = f'source {reverse} address="{src}"'

        if dst := clean_post.get("dst_ip"):
            reverse = clean_post.get("dst_reverse")
            destination = f'destination {reverse} address="{dst}"'

        if log := clean_post.get("log"):
            if limit := clean_post.get("log_limit") and (
                val := clean_post["log_value"]
            ):
                limit = f" limit value=\"{val}/{clean_post['log_unit']}\""
            log = f"{log} level=\"{clean_post['log_level']}\"{limit}"

        if audit := clean_post.get("audit"):
            if limit := clean_post.get("audit_limit") and (
                val := clean_post["audit_value"]
            ):
                limit = f" limit value=\"{val}/{clean_post['audit_unit']}\""
            audit = f"{audit}{limit}"

        if clean_post.get("action"):
            level = clean_post["action_level"]
            atype = limit = ""
            if clean_post.get("action_type") and (
                (stype := clean_post.get("action_type_ipv4"))
                or (stype := clean_post.get("action_type_ipv6"))  # noqa: W503
            ):
                atype = f' type="{stype}"'
            if clean_post.get("action_limit") and (val := clean_post["action_value"]):
                limit = f" limit value=\"{val}/{clean_post['action_unit']}\""
            action = f"{level}{atype}{limit}"

        priority = clean_post.get("priority")
        rule = 'rule priority="{priority}" {family} {element} {source} {destination} {log} {audit} {action}'.format(
            priority=priority,
            family=family,
            element=element,
            source=source,
            destination=destination,
            log=log,
            audit=audit,
            action=action,
        )
        self.cleaned_data = {"rule": rule}
