import datetime
import os
import re

from flask import abort, current_app, g, jsonify, session
from flask_login import current_user
from flask_security import permissions_required
from systemd import journal

from .consts import LOG_LEVELS
from .structure import STRUCTURE


def context():
    """Load context."""
    if (config_mode := session.get("config_mode")) is None:
        config_mode = session["config_mode"] = "runtime"

    g.default_zone = current_app.runtime_config.getDefaultZone()
    g.panic_mode = current_app.runtime_config.queryPanicMode()
    g.denied_log = current_app.runtime_config.getLogDenied()
    g.lockdown_mode = current_app.runtime_config.queryLockdown()
    g.automatic_helpers = current_app.runtime_config.getAutomaticHelpers()
    g.zones = STRUCTURE["zones"][config_mode]["get_all"]()
    g.services = STRUCTURE["services"][config_mode]["get_all"]()
    g.icmptypes = STRUCTURE["icmptypes"][config_mode]["get_all"]()
    g.ipsets = STRUCTURE["ipsets"][config_mode]["get_all"]()
    g.helpers = STRUCTURE["helpers"][config_mode]["get_all"]()
    g.modal_sections = {
        "zones": STRUCTURE["zones"]["settings"]["form"](),
        "services": STRUCTURE["services"]["settings"]["form"](),
        "icmptypes": STRUCTURE["icmptypes"]["settings"]["form"](),
        "ipsets": STRUCTURE["ipsets"]["settings"]["form"](),
        "helpers": STRUCTURE["helpers"]["settings"]["form"](),
    }


def getObject(section, config_mode, item=None):
    structure = STRUCTURE[section]
    get_item = structure[config_mode].get("get_item")
    get_direct = structure[config_mode].get("get_direct")
    if get_direct is None:
        try:
            return get_item(item)
        except Exception:
            abort(404, "Item not found")
    return get_direct


def settings2dict(section, config_mode, obj, structure):
    items = structure["settings"]["items"]
    if section in ["zones", "services", "helpers", "icmptypes", "ipsets"]:
        return _settingDict(config_mode, obj, items)
    return {}


def _settingDict(config_mode, obj, items):
    if config_mode == "runtime":
        settingsDict = obj.settings
    else:
        settingsDict = (obj.getSettings()).settings
    config = {}
    i = 0
    for item in items:
        if isinstance(item, str):
            config.update({item: settingsDict[i]})
            i = i + 1
        if isinstance(item, list):
            for sub in item:
                if s := settingsDict[i].get(sub):
                    config.update({sub: s})
    return config


@permissions_required("section-edit")
def setSection(config_mode, section, obj, cleaned_date):
    saveset = obj
    if config_mode == "permanent":
        saveset = obj.getSettings()

    saveset.setVersion(cleaned_date.get("version", ""))
    saveset.setShort(cleaned_date.get("short", ""))
    saveset.setDescription(cleaned_date.get("description", ""))

    if section in ["zones"]:
        if target := cleaned_date.get("target"):
            saveset.setTarget(target)
    if section in ["icmptypes"]:
        if destination := cleaned_date.get(""):
            saveset.setDestinations(destination)
    if section in ["ipsets"]:
        if hashtype := cleaned_date.get("hashtype"):
            saveset.setType(hashtype)
        saveset.setOptions(cleaned_date.get("options", {}))
    return saveset


def setItem(obj, section, item, tabname, structure, form, method):
    if (
        session.get("config_mode") == "permanent"
        and current_user.has_permission("permanent") is False
    ):
        abort(403)

    getattr(obj, structure[tabname][method])(**form.cleaned_data)

    if (config_mode := session.get("config_mode")) == "runtime" and (
        set_item := structure.get(config_mode, {}).get("set_item")
    ):
        set_item(item, obj)

    return jsonify(data=form.cleaned_data)


@permissions_required("logs-read")
def getLog(log, query="", start=None, end=None, level=None):
    uid_list = os.listdir("/var/log/journal")
    j = journal.Reader(path="/var/log/journal")
    j.this_machine(uid_list[0])
    if start is None:
        start = datetime.datetime.now() - datetime.timedelta(hours=1)
    if end is None:
        end = datetime.datetime.now()

    query = re.escape(query)

    if log == "system":
        j.add_match(_SYSTEMD_UNIT="firewalld.service")

    if log == "firewall":
        query = f"^FINAL_REJECT: .*{query}.*"
        j.add_match(_TRANSPORT="kernel")
        j.add_match(PRIORITY=4)

    if level:
        j.add_match(PRIORITY=level)

    logs = []
    keys = []
    for entry in j:
        if (
            re.findall(query, entry["MESSAGE"], re.IGNORECASE)
            and entry["__REALTIME_TIMESTAMP"] >= start
            and entry["__REALTIME_TIMESTAMP"] <= end
        ):
            m_json = {
                "DATETIME": entry["__REALTIME_TIMESTAMP"].strftime(
                    "%Y-%m-%dT%H:%M:%S.%f"
                )
            }
            if "DATETIME" not in keys:
                keys.append("DATETIME")
            if log == "firewall":
                s = re.findall(r"(\w+)=([a-zA-Z0-9_:.]+)", entry["MESSAGE"])
                for i in s:
                    m_json.update({i[0]: i[1]})
                    if i[0] not in keys:
                        keys.append(i[0])
                logs.append(m_json)
            else:
                if "MESSAGE" not in keys:
                    keys.append("MESSAGE")
                    keys.append("PRIORITY")
                m_json.update(
                    {
                        "MESSAGE": entry["MESSAGE"],
                        "PRIORITY": LOG_LEVELS[entry["PRIORITY"]][1],
                    }
                )
                logs.append(m_json)

    return {"logs": logs, "headers": keys}
