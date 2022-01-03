from dbus.exceptions import DBusException
from firewall.errors import FirewallError
from flask import current_app, g, session, jsonify, abort

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


def fw_template(section, tabname=None):
    """Search template"""
    if tabname is None:
        return f"firewall/{section}.html"
    return f"firewall/{section}/tab_{tabname}.html"


def get_object(section, config_mode, item=None):
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


def saveSection(config_mode, section, obj, datas):
    saveset = obj
    if config_mode == "permanent":
        saveset = obj.getSettings()

    saveset.setVersion(datas.get("version", ""))
    saveset.setShort(datas.get("short", ""))
    saveset.setDescription(datas.get("description", ""))

    if section in ["zones"]:
        if target := datas.get("target"):
            saveset.setTarget(target)
    if section in ["icmptypes"]:
        if destination := datas.get(""):
            saveset.setDestinations(destination)
    if section in ["ipsets"]:
        if hashtype := datas.get("hashtype"):
            saveset.setType(hashtype)
        saveset.setOptions(datas.get("options", {}))
    return saveset


def setItem(obj, section, item, tabname, structure, form, method):
    try:
        getattr(obj, structure[tabname][method])(**form.cleaned_data)
        if (config_mode := session.get("config_mode")) == "runtime" and (
            set_item := structure.get(config_mode, {}).get("set_item")
        ):
            set_item(item, obj)
        return jsonify(data=form.cleaned_data)

    except DBusException as error:
        raise DBusException(error)
    except FirewallError as error:
        raise FirewallError(error)
    except Exception as error:
        raise Exception(error)
