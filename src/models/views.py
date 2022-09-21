import uuid

from flask import abort
from flask_admin import AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_security.utils import hash_password
from wtforms import PasswordField


class AdminPasswordField(PasswordField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0] != "":
            self.data = hash_password(valuelist[0])
        elif self.data is None:
            self.data = ""


class GlobalView(ModelView):
    def inaccessible_callback(self, name, **kwargs):
        abort(403)


class UserView(GlobalView):
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True
    can_set_page_size = True
    edit_modal = False
    create_modal = False
    details_modal = True
    column_display_actions = True
    column_searchable_list = ["email", "username"]
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
    form_columns = (
        "fs_uniquifier",
        "email",
        "active",
        "username",
        "first_name",
        "last_name",
        "gravatar_url",
        "password",
        "roles",
    )
    form_extra_fields = {
        "password": AdminPasswordField("Password"),
    }
    column_filters = ["email"]
    form_args = dict(
        fs_uniquifier=dict(default=uuid.uuid4().hex, render_kw={"readonly": True})
    )

    def is_accessible(self):
        return current_user.is_authenticated and (
            current_user.has_role("admin") or current_user.has_role("admin_user")
        )


class RoleView(GlobalView):
    def is_accessible(self):
        return current_user.is_authenticated and (
            current_user.has_role("admin") or current_user.has_role("admin_role")
        )


class HomeView(AdminIndexView):
    menu_class = "test"
    menu_icon_type = "bs"
    menu_icon = "ok"

    def is_visible(self):
        return False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):
        abort(403)


class FileExplore(FileAdmin):
    can_upload = True
    can_delete = True
    can_delete_dirs = True
    can_mkdir = True
    can_rename = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):
        abort(403)
