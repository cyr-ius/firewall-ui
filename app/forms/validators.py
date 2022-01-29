from wtforms.validators import ValidationError
from firewall.functions import (
    check_mac,
    check_port,
    checkUid,
    checkCommand,
    checkProtocol,
    checkInterface,
)


class Interface(object):
    def __init__(self, message=None):
        if not message:
            message = "This format is not a interface."
        self.message = message

    def __call__(self, form, field):
        if field.data and not checkInterface(field.data):
            raise ValidationError(self.message)


class Protocol(object):
    def __init__(self, message=None):
        if not message:
            message = "This format is not a command."
        self.message = message

    def __call__(self, form, field):
        if field.data and not checkProtocol(field.data):
            raise ValidationError(self.message)


class Command(object):
    def __init__(self, message=None):
        if not message:
            message = "This format is not a command."
        self.message = message

    def __call__(self, form, field):
        if field.data and not checkCommand(field.data):
            raise ValidationError(self.message)


class Uid(object):
    def __init__(self, message=None):
        if not message:
            message = "This format is not UID."
        self.message = message

    def __call__(self, form, field):
        if field.data and not checkUid(field.data):
            raise ValidationError(self.message)


class MacAddress(object):
    def __init__(self, message=None):
        if not message:
            message = "This format is not mac address."
        self.message = message

    def __call__(self, form, field):
        if field and not check_mac(field):
            raise ValidationError(self.message)


class PortNumber(object):
    def __init__(self, message=None):
        if not message:
            message = "This format is a port."
        self.message = message

    def __call__(self, form, field):
        if field and not check_port(field):
            raise ValidationError(self.message)


class NumberRange(object):
    def __init__(self, min, max, message=None):
        if not message:
            message = f"Number is invalid. ({min} - {max})"
        self.message = message
        self.min = min
        self.max = max

    def __call__(self, form, field):
        if field.data and not (
            int(field.data) > self.min and int(field.data) < self.max
        ):
            raise ValidationError(self.message)


class PortRange(object):
    def __init__(self, min, max, message=None):
        if not message:
            message = "Range port is invalid."
        self.message = message
        self.min = min
        self.max = max

    def __call__(self, form, field):
        if field.data is None:
            return
        for item in field.data.split("-"):
            if not (int(item) > self.min and int(item) < self.max):
                raise ValidationError(self.message)
