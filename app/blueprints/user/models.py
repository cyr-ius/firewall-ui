from flask_security.models import fsqla_v2 as fsqla

from ... import db


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"

    def __repr__(self) -> str:
        return self.name

    def init_db(self, app):
        app.user_datastore.find_or_create_role(
            name="admin",
            permissions={
                "admin-read",
                "admin-write",
                "automatichelper",
                "changezone",
                "directconfigs-read",
                "filer",
                "helpers-read",
                "icmptypes-read",
                "ipsets-read",
                "lockdown",
                "logs-read",
                "panicmode",
                "permanent",
                "section-read",
                "section-write",
                "services-read",
                "whitelists-read",
                "zones-read",
            },
        )
        app.user_datastore.find_or_create_role(
            name="no permanent",
            permissions={
                "directconfigs-read",
                "helpers-read",
                "icmptypes-read",
                "ipsets-read",
                "logs-read",
                "section-read",
                "services-read",
                "whitelists-read",
                "zones-read",
            },
        )
        app.user_datastore.find_or_create_role(name="admin_user")
        app.user_datastore.find_or_create_role(name="admin_role")


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.Integer(), db.ForeignKey("user.id"))
    role_id = db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))


class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = "user"
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gravatar_url = db.Column(db.String(2048))
    roles = db.relationship(
        "Role",
        secondary="roles_users",
        backref=db.backref("users", lazy="dynamic"),
    )
    locale = db.Column(db.String(8))

    def __repr__(self) -> str:
        return self.email
