import traceback
from distutils.util import strtobool
from flask import current_app
from ... import db


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    value = db.Column(db.Text())

    defaults = {"maintenance": False, "explore_db": False}

    def __init__(self, name=None, value=None):
        self.id = None
        self.name = name
        self.value = value

    def set_maintenance(self, mode):
        maintenance = Setting.query.filter(Setting.name == "maintenance").first()

        if maintenance is None:
            value = self.defaults["maintenance"]
            maintenance = Setting(name="maintenance", value=str(value))
            db.session.add(maintenance)

        mode = str(mode)

        try:
            if maintenance.value != mode:
                maintenance.value = mode
                db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(
                "Cannot set maintenance to {0}. DETAIL: {1}".format(mode, e)
            )
            current_app.logger.debug(traceback.format_exec())
            db.session.rollback()
            return False

    def toggle(self, setting):
        current_setting = Setting.query.filter(Setting.name == setting).first()

        if current_setting is None:
            value = self.defaults[setting]
            current_setting = Setting(name=setting, value=str(value))
            db.session.add(current_setting)

        try:
            if current_setting.value == "True":
                current_setting.value = "False"
            else:
                current_setting.value = "True"
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(
                "Cannot toggle setting {0}. DETAIL: {1}".format(setting, e)
            )
            current_app.logger.debug(traceback.format_exec())
            db.session.rollback()
            return False

    def set(self, setting, value):
        current_setting = Setting.query.filter(Setting.name == setting).first()

        if current_setting is None:
            current_setting = Setting(name=setting, value=None)
            db.session.add(current_setting)

        value = str(value)

        try:
            current_setting.value = value
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(
                "Cannot edit setting {0}. DETAIL: {1}".format(setting, e)
            )
            current_app.logger.debug(traceback.format_exec())
            db.session.rollback()
            return False

    def get(self, setting):
        if setting in self.defaults:
            result = self.query.filter(Setting.name == setting).first()
            if result is not None:
                return (
                    strtobool(result.value)
                    if result.value in ["True", "False"]
                    else result.value
                )
            else:
                return self.defaults[setting]
        else:
            current_app.logger.error("Unknown setting queried: {0}".format(setting))

    def init_db(self):
        for k, v in self.defaults.items():
            self.set(k, v)
