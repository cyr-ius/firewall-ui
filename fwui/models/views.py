from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from ..handle import handle_access_forbidden
from flask_login import current_user


class GlobalView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("dba")

    def inaccessible_callback(self, name, **kwargs):
        return handle_access_forbidden("Not permission")


class UserView(GlobalView):
    can_delete = True
    can_view_details = True
    can_export = True
    can_view_details = True
    can_set_page_size = True
    edit_modal = True
    create_modal = True
    details_modal = True
    column_display_actions = True
    column_exclude_list = ["password", "tf_totp_secret"]
    form_excluded_columns = ["password", "tf_totp_secret"]


class HomeView(AdminIndexView):
    template_mode = "bootstrap4"

    def is_visible(self):
        return False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("dba")

    def inaccessible_callback(self, name, **kwargs):
        handle_access_forbidden("Not permission")
