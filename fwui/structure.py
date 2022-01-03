from flask import current_app
from .forms.firewall import (
    frm_chains,
    frm_commands,
    frm_contexts,
    frm_destination,
    frm_icmp_types,
    frm_icmp_filters,
    frm_interfaces,
    frm_ipsets,
    frm_modules,
    frm_nat,
    frm_passthroughs,
    frm_pat,
    frm_ports,
    frm_protocols,
    frm_rich_rules,
    frm_rules,
    frm_services,
    frm_sourceports,
    frm_sources,
    frm_uids,
    frm_users,
)
from .forms.section import frm_zone, frm_service, frm_ipset, frm_icmptype, frm_helper

runtime = current_app.runtime_config
permanent = current_app.permanent_config

STRUCTURE = {
    "zones": {
        "runtime": {
            "get_item": runtime.getZoneSettings,
            "get_all": runtime.getZones,
            "set_item": runtime.setZoneSettings,
            "get_zoi": runtime.getZoneOfInterface,
            "get_zos": runtime.getZoneOfSource,
        },
        "permanent": {
            "get_item": permanent.getZoneByName,
            "get_all": permanent.getZoneNames,
            "get_zoi": permanent.getZoneOfInterface,
            "get_zos": permanent.getZoneOfSource,
        },
        "settings": {
            "form": frm_zone,
            "items": ["version", "short", "description", "target"],
            "get": "getSettings",
            "add": "addZone",
        },
        "services": {
            "form": frm_services,
            "add": "addService",
            "del": "removeService",
            "list": "getServices",
            "edit": "queryService",
        },
        "ports": {
            "form": frm_ports,
            "add": "addPort",
            "del": "removePort",
            "list": "getPorts",
        },
        "protocols": {
            "form": frm_protocols,
            "add": "addProtocol",
            "del": "removeProtocol",
            "list": "getProtocols",
        },
        "sourceports": {
            "form": frm_sourceports,
            "add": "addSourcePort",
            "del": "removeSourcePort",
            "list": "getSourcePorts",
        },
        "nat": {
            "form": frm_nat,
            "add": "addMasquerade",
            "del": "removeMasquerade",
            "list": "queryMasquerade",
        },
        "pat": {
            "form": frm_pat,
            "add": "addForwardPort",
            "del": "removeForwardPort",
            "list": "getForwardPorts",
        },
        "icmptypes": {
            "form": frm_icmp_filters,
            "add": "addIcmpBlock",
            "del": "removeIcmpBlock",
            "list": "getIcmpBlocks",
        },
        "richrules": {
            "form": frm_rich_rules,
            "add": "addRichRule",
            "del": "removeRichRule",
            "list": "getRichRules",
        },
        "interfaces": {
            "form": frm_interfaces,
            "add": "addInterface",
            "del": "removeInterface",
            "list": "getInterfaces",
        },
        "sources": {
            "form": frm_sources,
            "add": "addSource",
            "del": "removeSource",
            "list": "getSources",
        },
    },
    "services": {
        "runtime": {
            "get_item": runtime.getServiceSettings,
            "get_all": runtime.listServices,
        },
        "permanent": {
            "get_item": permanent.getServiceByName,
            "get_all": permanent.getServiceNames,
        },
        "settings": {
            "form": frm_service,
            "items": ["version", "short", "description"],
            "get": "getSettings",
            "add": "addService",
        },
        "ports": {
            "form": frm_ports,
            "add": "addPort",
            "del": "removePort",
            "list": "getPorts",
            "edit": "queryPort",
        },
        "protocols": {
            "form": frm_protocols,
            "add": "addProtocol",
            "del": "removeProtocol",
            "list": "getProtocols",
        },
        "sourceports": {
            "form": frm_sourceports,
            "add": "addSourcePort",
            "del": "removeSourcePort",
            "list": "getSourcePorts",
        },
        "modules": {
            "form": frm_modules,
            "add": "addModule",
            "del": "removeModule",
            "list": "getModules",
            "edit": "queryModule",
        },
        "destination": {
            "form": frm_destination,
            "add": "setDestination",
            "del": "removeDestination",
            "list": "getDestinations",
            "edit": "queryDestination",
        },
    },
    "ipsets": {
        "runtime": {
            "get_item": runtime.getIPSetSettings,
            "get_all": runtime.getIPSets,
        },
        "permanent": {
            "get_item": permanent.getIPSetByName,
            "get_all": permanent.getIPSetNames,
        },
        "settings": {
            "form": frm_ipset,
            "items": [
                "version",
                "short",
                "description",
                "hashtype",
                ["family", "timeout", "hashsize", "maxelem"],
            ],
            "get": "getSettings",
            "add": "addIPSet",
        },
        "inputs": {
            "form": frm_ipsets,
            "add": "addEntry",
            "del": "removeEntry",
            "set": "setEntries",
            "list": "getEntries",
            "edit": "queryEntry",
        },
    },
    "icmptypes": {
        "runtime": {
            "get_item": runtime.getIcmpTypeSettings,
            "get_all": runtime.listIcmpTypes,
        },
        "permanent": {
            "get_item": permanent.getIcmpTypeByName,
            "get_all": permanent.getIcmpTypeNames,
        },
        "settings": {
            "form": frm_icmptype,
            "items": ["version", "short", "description"],
            "get": "getSettings",
            "add": "addIcmpType",
        },
        "destination": {
            "form": frm_icmp_types,
            "add": "addDestination",
            "del": "removeDestination",
            "list": "getDestinations",
            "edit": "queryDestination",
        },
    },
    "helpers": {
        "runtime": {
            "get_item": runtime.getHelperSettings,
            "get_all": runtime.getHelpers,
        },
        "permanent": {
            "get_item": permanent.getHelperByName,
            "get_all": permanent.getHelperNames,
        },
        "settings": {
            "form": frm_helper,
            "items": ["version", "short", "description", "family", "module"],
            "get": "getSettings",
            "add": "addHelper",
        },
        "ports": {
            "form": frm_ports,
            "add": "addPort",
            "del": "removePort",
            "list": "getPorts",
            "edit": "queryPort",
        },
    },
    "directconfigs": {
        "runtime": {"get_direct": runtime},
        "permanent": {"get_direct": runtime},
        "chains": {
            "form": frm_chains,
            "add": "addChain",
            "del": "removeChain",
            "list": "getAllChains",
            "edit": "queryChain",
        },
        "rules": {
            "form": frm_rules,
            "add": "addRule",
            "del": "removeRule",
            "list": "getAllRules",
            "edit": "queryRule",
        },
        "passthrough": {
            "form": frm_passthroughs,
            "add": "addPassthrough",
            "del": "removePassthroughs",
            "list": "getAllPassthroughs",
            "edit": "queryPassthrough",
        },
    },
    "whitelists": {
        "runtime": {"get_direct": runtime},
        "permanent": {"get_direct": runtime},
        "contexts": {
            "form": frm_contexts,
            "add": "addLockdownWhitelistContext",
            "del": "removeLockdownWhitelistContext",
            "list": "getLockdownWhitelistContexts",
            "edit": "queryLockdownWhitelistContext",
        },
        "commands": {
            "form": frm_commands,
            "add": "addLockdownWhitelistCommand",
            "del": "removeLockdownWhitelistCommand",
            "list": "getLockdownWhitelistCommands",
            "edit": "queryLockdownWhitelistCommand",
        },
        "users": {
            "form": frm_users,
            "add": "addLockdownWhitelistUser",
            "del": "removeLockdownWhitelistUser",
            "list": "getLockdownWhitelistUsers",
            "edit": "queryLockdownWhitelistUser",
        },
        "uids": {
            "form": frm_uids,
            "add": "addLockdownWhitelistUid",
            "del": "removeLockdownWhitelistUid",
            "list": "getLockdownWhitelistUids",
            "edit": "queryLockdownWhitelistUid",
        },
    },
    "policies": {
        "settings": {
            "form": None,
            "items": [],
            "get": "getSettings",
            "set": "setSettingsDict",
            "add": "addPolicy",
        },
    },
}
