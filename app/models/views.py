from flask import abort
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class GlobalView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("dba")

    def inaccessible_callback(self, name, **kwargs):
        abort(403)


class UserView(GlobalView):
    can_create = False
    can_edit = False
    can_delete = True
    can_export = True
    can_view_details = True
    can_set_page_size = True
    edit_modal = False
    create_modal = False
    details_modal = True
    column_display_actions = True
    column_exclude_list = [
        "current_login_at",
        "fs_uniquifier",
        "password",
        "us_totp_secrets",
        "us_phone_number",
        "active",
        "confirmed_at",
        "tf_totp_secret",
        "tf_primary_method",
        "tf_phone_number",
    ]
    form_excluded_columns = ["fs_uniquifier", "password", "tf_totp_secret"]


class RoleView(GlobalView):
    pass


class HomeView(AdminIndexView):
    menu_class = "test"
    menu_icon_type = "bs"
    menu_icon = "ok"

    def is_visible(self):
        return False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("dba")

    def inaccessible_callback(self, name, **kwargs):
        abort(403)
