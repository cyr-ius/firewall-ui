from flask import session, current_app
from flask_babel import gettext as _
from wtforms import (
    BooleanField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    FormField,
    FieldList,
)
from wtforms.validators import IPAddress, Optional, MacAddress, DataRequired
from wtforms.widgets import CheckboxInput

from ...forms.validators import NumberRange, PortRange, Command, Uid, Protocol, Interface
from .consts import (
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
from ...forms.frm import frm


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
        validators=[DataRequired(), PortRange(min=1, max=65535)],
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
        if other := self.cleaned_data.pop("other", None):
            self.cleaned_data.update({"protocol": other})


class frm_sourceports(frm):
    port = StringField(
        label=_("Port/Interval"),
        validators=[DataRequired(), NumberRange(min=1, max=65535)],
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
        render_kw={"class": "form-check-input"},
    )

    def clean(self):
        self.cleaned_data = {}


class frm_pat(frm):
    port = StringField(
        label=_("Port"),
        validators=[DataRequired(), NumberRange(min=1, max=65535)],
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
    toport = StringField(
        label=_("To port"),
        validators=[DataRequired(), NumberRange(min=1, max=65535)],
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
        validators=[DataRequired(), Interface()],
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
        render_kw={"class": "form-select"},
    )
    address = StringField(
        label=_("IP Address"),
        validators=[DataRequired(), IPAddress(ipv4=True, ipv6=True)],
        render_kw={"class": "form-control", "placeholder": _("IP address")},
    )


class frm_ipsets(frm):
    entry = StringField(
        label=_("Entry"),
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": _("Entry")},
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
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": _("Chain")},
    )


class frm_rules(frm_chains):
    priority = IntegerField(
        label=_("Priority"),
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": _("Priority")},
    )
    args = StringField(
        label=_("Args"), render_kw={"class": "form-control", "placeholder": _("Args")}
    )


class frm_passthroughs(frm):
    ipv = SelectField(label=_("IPV"), choices=IPV, render_kw={"class": "form-select"})
    args = StringField(
        label=_("Args"),
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": _("Args")},
    )


class frm_contexts(frm):
    context = StringField(
        label=_("Context"),
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": _("Context")},
    )


class frm_commands(frm):
    command = StringField(
        label=_("Command"),
        validators=[DataRequired(), Command()],
        render_kw={"class": "form-control", "placeholder": _("Command")},
    )


class frm_users(frm):
    user = StringField(
        label=_("User"),
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": _("User")},
    )


class frm_uids(frm):
    uid = IntegerField(
        label=_("UID"),
        validators=[DataRequired(), Uid()],
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
        default="ipv4",
        render_kw={"class": "form-select"},
    )
    priority = IntegerField(
        label=_("Priority"),
        validators=[Optional()],
        render_kw={"class": "form-control", "placeholder": _("Priority")},
    )

    element = BooleanField(
        label=_("Element"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )

    ELEMENTS.append(("", "---"))
    element_level = SelectField(
        label=_("Level"),
        choices=ELEMENTS,
        validators=[],
        default="",
        render_kw={"class": "form-select", "disabled": "disabled"},
    )

    element_level_service = FieldList(
        FormField(frm_services),
        render_kw={"style": "display: none;"},
        id="service",
        validators=[Optional()],
        min_entries=1,
    )
    element_level_port = FieldList(
        FormField(frm_ports),
        render_kw={"style": "display: none;"},
        id="port",
        validators=[Optional()],
        min_entries=1,
    )
    element_level_protocol = FieldList(
        FormField(frm_protocols),
        render_kw={"style": "display: none;"},
        id="protocol",
        validators=[Optional()],
        min_entries=1,
    )
    element_level_icmptype = FieldList(
        FormField(frm_icmp_types),
        render_kw={"style": "display: none;"},
        id="icmptype",
        validators=[Optional()],
        min_entries=1,
    )
    element_level_icmpblock = FieldList(
        FormField(frm_icmp_filters),
        render_kw={"style": "display: none;"},
        id="icmpblock",
        validators=[Optional()],
        min_entries=1,
    )
    element_level_forwardport = FieldList(
        FormField(frm_pat),
        render_kw={"style": "display: none;"},
        id="forwardport",
        validators=[Optional()],
        min_entries=1,
    )
    element_level_sourceport = FieldList(
        FormField(frm_sourceports),
        render_kw={"style": "display: none;"},
        id="sourceport",
        validators=[Optional()],
        min_entries=1,
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
        render_kw={"class": "form-select", "disabled": ""},
    )
    action_type = BooleanField(
        label=_("Type"),
        widget=CheckboxInput(),
        validators=[Optional()],
        render_kw={"class": "form-check-input", "disabled": ""},
    )

    action_type_ipv4 = SelectField(
        label=_("IPv4"),
        default="icmp-host-prohibited",
        choices=REJECT_IPV4,
        render_kw={"class": "form-select", "style": "display: none;", "disabled": ""},
    )

    action_type_ipv6 = SelectField(
        label=_("IPv6"),
        default="icmp6-adm-prohibited",
        choices=REJECT_IPV6,
        render_kw={"class": "form-select", "style": "display: none;", "disabled": ""},
    )
    action_mark = StringField(
        label=_("Mark"),
        render_kw={
            "class": "form-control",
            "style": "display: none;",
            "placeholder": _("Mark"),
            "disabled": "",
        },
    )
    action_mask = StringField(
        label=_("Mask"),
        render_kw={
            "class": "form-control",
            "style": "display: none;",
            "placeholder": _("Mark"),
            "disabled": "",
        },
    )

    action_limit = BooleanField(
        label=_("Limit"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    action_value = IntegerField(
        label=_("Value"),
        render_kw={"class": "form-control", "style": "display: none;", "disabled": ""},
    )
    action_unit = SelectField(
        label=_("Unit"),
        default="s",
        choices=INTERVAL_UNIT,
        render_kw={"class": "form-select", "style": "display: none;", "disabled": ""},
    )

    src = SelectField(
        label=_("Source"),
        choices=SOURCES,
        default="IP",
        render_kw={"class": "form-select"},
    )
    src_ip = StringField(
        label=_("IP Source"),
        validators=[Optional(), IPAddress(ipv4=True, ipv6=True)],
        render_kw={
            "class": "form-control",
            "placeholder": _("ip address"),
            "style": "display: none;",
            "disabled": "",
        },
    )
    src_mac = StringField(
        label=_("MAC Address"),
        validators=[Optional(), MacAddress()],
        render_kw={
            "class": "form-control",
            "placeholder": _("mac address"),
            "style": "display: none;",
            "disabled": "",
        },
    )
    src_reverse = BooleanField(
        label=_("Reverse"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )

    src_ipset = SelectField(
        label=_("IPSet"),
        choices=IPSETS,
        validators=[Optional()],
        render_kw={"class": "form-select", "style": "display: none;", "disabled": ""},
    )

    dst_ip = StringField(
        label=_("IP Destination"),
        validators=[Optional(), IPAddress(ipv4=True, ipv6=True)],
        render_kw={"class": "form-control", "placeholder": _("ip address")},
    )
    dst_reverse = BooleanField(
        label=_("Reverse"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )

    log = BooleanField(
        label=_("Logs"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    log_level = SelectField(
        label=_("Level"),
        choices=LOGLEVELS,
        validators=[Optional()],
        default="warning",
        render_kw={"class": "form-select", "disabled": "disabled"},
    )
    log_prefix = StringField(
        label=_("Prefix"),
        validators=[Optional()],
        render_kw={
            "class": "form-control",
            "placeholder": _("Prefix"),
            "disabled": "",
        },
    )
    log_limit = BooleanField(
        label=_("Limit"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    log_value = IntegerField(
        label=_("Value"),
        render_kw={"class": "form-control", "style": "display: none;", "disabled": ""},
    )
    log_unit = SelectField(
        label=_("Unit"),
        default="s",
        choices=INTERVAL_UNIT,
        render_kw={"class": "form-control", "style": "display: none;", "disabled": ""},
    )

    audit = BooleanField(
        label=_("Audit"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    audit_limit = BooleanField(
        label=_("Limit"),
        validators=[Optional()],
        render_kw={"class": "form-check-input"},
    )
    audit_value = IntegerField(
        label=_("Value"),
        render_kw={"class": "form-control", "style": "display: none;", "disabled": ""},
    )
    audit_unit = SelectField(
        label=_("Unit"),
        default="s",
        choices=INTERVAL_UNIT,
        render_kw={"class": "form-select", "style": "display: none;", "disabled": ""},
    )

    rule = HiddenField(validators=[Optional()])

    def clean(self):
        if rule := self.cleaned_data.get("rule"):
            self.cleaned_data = {"rule": rule}
            return
        clean_post = self.cleaned_data.copy()
        for k, v in clean_post.items():
            if v is False or v is None or v == "" or v == "---":
                self.cleaned_data.pop(k)

        element = source = masquerade = ""

        if family := self.cleaned_data.get("family", ""):
            family = f' family="{family}"'

        if priority := self.cleaned_data.get("priority", ""):
            priority = f' priority="{priority}"'

        if element := self.cleaned_data.get("element_level", ""):
            if element == "masquerade":
                masquerade = " masquerade"
                element = ""
            else:
                element_type = element
                level = self.cleaned_data.get(f"element_level_{element}", [])[0]
                level.pop("csrf_token", None)
                element = f" {element_type}"
                for k, v in level.items():
                    if k in [
                        "service",
                        "icmp-block",
                        "icmp-type",
                        "source-port",
                        "forward-port",
                    ]:
                        element += f' name="{v}"'
                    else:
                        element += f' {k}="{v}"'

        if (
            (src := self.cleaned_data.get("src_ip"))
            or (src := self.cleaned_data.get("src_mac"))  # noqa: W503
            or (src := self.cleaned_data.get("src_ipset"))  # noqa: W503
        ):
            reverse = " NOT" if self.cleaned_data.get("src_reverse") else ""
            source = f' source{reverse} address="{src}"'

        if destination := self.cleaned_data.get("dst_ip", ""):
            reverse = " NOT" if self.cleaned_data.get("dst_reverse") else ""
            destination = f' destination{reverse} address="{destination}"'

        if log := self.cleaned_data.get("log", ""):
            if limit := self.cleaned_data.get("log_limit", ""):
                lv = self.cleaned_data["log_value"]
                lu = self.cleaned_data["log_unit"]
                limit = f' limit value="{lv}/{lu}"'
            log = f" log level=\"{ self.cleaned_data['log_level']}\"{limit}"

        if audit := self.cleaned_data.get("audit", ""):
            if limit := self.cleaned_data.get("audit_limit", ""):
                av = self.cleaned_data["audit_value"]
                au = self.cleaned_data["audit_unit"]
                limit = f' limit value="{av}/{au}"'
            audit = f" audit{limit}"

        if action := self.cleaned_data.get("action", ""):
            level = self.cleaned_data["action_level"]
            if atype := self.cleaned_data.get("action_type", "") and (
                (stype := self.cleaned_data.get("action_type_ipv4"))
                or (stype := self.cleaned_data.get("action_type_ipv6"))  # noqa: W503
            ):
                atype = f' type="{stype}"'
            if limit := self.cleaned_data.get("action_limit", ""):
                av = self.cleaned_data["action_value"]
                au = self.cleaned_data["action_unit"]
                limit = f' limit value="{av}/{au}"'
            action = f" {level}{atype}{limit}"

        rule = "rule{priority}{family}{element}{source}{destination}{log}{audit}{action}{masquerade}".format(
            priority=priority,
            family=family,
            element=element,
            source=source,
            destination=destination,
            log=log,
            audit=audit,
            action=action,
            masquerade=masquerade,
        ).strip()
        current_app.logger.debug(rule)
        self.cleaned_data = {"rule": rule}


class frm_delete_rule(frm):
    rule = HiddenField()
