from flask_babel import gettext as _
from wtforms import HiddenField, SelectField, StringField, SubmitField
from wtforms.validators import Optional

from flask import current_app
from ..consts import LOG_LEVELS
from .frm import frm
from ..structure import permanent


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
        render_kw={"onchange": "submit();"},
    )

    LOG_LEVELS.append(("", "---"))
    level = SelectField(
        label=_("Level"),
        validators=[Optional()],
        choices=LOG_LEVELS,
        render_kw={"onchange": "submit();"},
    )
