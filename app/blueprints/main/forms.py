from flask_babel import gettext as _
from wtforms import HiddenField, SelectField, StringField, SubmitField
from wtforms.validators import Optional, DataRequired

from ..firewall.consts import LOG_LEVELS
from ...forms.frm import frm
from ..firewall.structure import permanent


class frm_change_zone(frm):
    ZONES = [(zones, zones) for zones in permanent.getZoneNames()]
    new_zone = SelectField(label=_("New zone"), choices=ZONES)
    source = HiddenField(label=_("Source"))
    type = HiddenField(label=_("Type"))
    submit = SubmitField(label=_("Save"))


class frm_logs(frm):
    search = StringField(
        label=_("Search"),
        validators=[Optional()],
    )

    LOG_LEVELS.append(("", "---"))
    level = SelectField(
        label=_("Level"),
        default="",
        validators=[Optional()],
        choices=LOG_LEVELS,
    )

    type = SelectField(
        label=_("Type"),
        default="firewall",
        validators=[DataRequired()],
        choices=[("system", "System Log"), ("firewall", "Denied Log")],
    )

    date_start = HiddenField()
    date_end = HiddenField()
    submit = SubmitField(label=_("OK"))
