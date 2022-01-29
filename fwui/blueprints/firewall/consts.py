from flask import current_app

PROTOCOLS = [
    ("ah", "ah"),
    ("esp", "esp"),
    ("dccp", "dccp"),
    ("ddp", "ddp"),
    ("icmp", "icmp"),
    ("ipv6-icmp", "ipv6-icmp"),
    ("igmp", "igmp"),
    ("mux", "mux"),
    ("sctp", "sctp"),
    ("tcp", "tcp"),
    ("udp", "udp"),
]

PROTOCOLS_SHORT = [("tcp", "tcp"), ("udp", "udp"), ("sctp", "sctp"), ("dccp", "dccp")]

ELEMENTS = [
    ("service", "service"),
    ("port", "port"),
    ("protocol", "protocol"),
    ("icmp-block", "icmp-block"),
    ("icmp-type", "icmp-type"),
    ("forward-port", "forward-port"),
    ("source-port", "source-port"),
    ("masquerade", "masquer"),
]

LOGLEVELS = [
    ("emerg", "emergency"),
    ("alert", "alert"),
    ("crit", "critical"),
    ("error", "error"),
    ("warning", "warning"),
    ("notice", "notice"),
    ("info", "info"),
    ("debug", "debug"),
]

INTERVAL_UNIT = [
    ("s", "second"),
    ("m", "minute"),
    ("h", "hour"),
    ("d", "day"),
]

ACTIONS = [
    ("accept", "accept"),
    ("reject", "reject"),
    ("drop", "drop"),
    ("mark", "mark"),
]

IPSETS = [(ipset, ipset) for ipset in current_app.runtime_config.getIPSets()]

SERVICES = [(service, service) for service in current_app.runtime_config.listServices()]

ICMPTYPES = [(icmp, icmp) for icmp in current_app.runtime_config.listIcmpTypes()]

ZONES = [(zones, zones) for zones in current_app.runtime_config.getZones()]

SOURCES = [("IP", "IP"), ("MAC", "MAC"), ("ipset", "ipset")]

MODULES = [
    ("Q.931", "Q.931"),
    ("RAS", "RAS"),
    ("amanda", "amanda"),
    ("ftp", "ftp"),
    ("h323", "h323"),
    ("irc", "irc"),
    ("netbios-ns", "netbios-ns"),
    ("pptp", "pptp"),
    ("proto-gre", "proto-gre"),
    ("sane", "sane"),
    ("sip", "sip"),
    ("snmp", "snmp"),
    ("tftp", "tftp"),
]

IPV = [("ipv4", "ipv4"), ("ipv6", "ipv6"), ("eb", "eb")]

DESTINATIONS = [("ipv4", "ipv4"), ("ipv6", "ipv6")]

TYPESETS = [
    ("hash:mac", "hash:mac"),
    ("hash:net,iface", "hash:net,iface"),
    ("hash:net,port", "hash:net,port"),
    ("hash:net,port,net", "hash:net,port,net"),
    ("hash:net,net", "hash:net,net"),
    ("hash:net", "hash:net"),
    ("hash:ip,port,net", "hash:ip,port,net"),
    ("hash:ip,port,ip", "hash:ip,port,ip"),
    ("hash:ip,mark", "hash:ip,mark"),
    ("hash:ip,port", "hash:ip,port"),
    ("hash:ip", "hash:ip"),
]

REJECT_IPV4 = [
    ("icmp-host-prohibited", "icmp-host-prohibited"),
    ("host-prohib", "host-prohib"),
    ("icmp-net-prohibited", "icmp-net-prohibited"),
    ("host-prohib", "net-prohib"),
    ("icmp-admin-prohibited", "icmp-admin-prohibited"),
    ("admin-prohib", "admin-prohib"),
    ("icmp-host-unreachable", "icmp-host-unreachable"),
    ("host-unreach", "host-unreach"),
    ("icmp-net-unreachable", "icmp-net-unreachable"),
    ("net-unreach", "net-unreach"),
    ("icmp-port-unreachable", "icmp-port-unreachable"),
    ("port-unreach", "port-unreach"),
    ("icmp-proto-unreachable", "icmp-proto-unreachable"),
    ("proto-unreach", "proto-unreach"),
    ("tcp-reset", "tcp-reset"),
    ("tcp-rst", "tcp-rst"),
]

REJECT_IPV6 = [
    ("icmp6-adm-prohibited", "icmp6-adm-prohibited"),
    ("adm-prohib", "adm-prohib"),
    ("icmp6-port-unreachable", "icmp6-port-unreachable"),
    ("port-unreach", "port-unreach"),
    ("icmp6-addr-unreachable", "icmp6-addr-unreachable"),
    ("addr-unreach", "addr-unreach"),
    ("icmp6-no-route", "icmp6-no-route"),
    ("no-route", "no-route"),
    ("tcp-reset", "tcp-reset"),
]

CHAINS_TABLE = [
    ("filter", "filter"),
    ("nat", "nat"),
    ("mangle", "mangle"),
    ("raw", "raw"),
    ("security", "security"),
]

TARGET = [
    ("default", "default"),
    ("ACCEPT", "ACCEPT"),
    ("DROP", "DROP"),
    ("%%REJECT%%", "REJECT"),
]

LOG_LEVELS = [
    (0, "Emergency"),
    (1, "Alert"),
    (2, "Critical"),
    (3, "Error"),
    (4, "Warning"),
    (5, "Notice"),
    (6, "Informational"),
    (7, "Debugging"),
]
