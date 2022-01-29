from flask_security.models import fsqla_v2 as fsqla

from ... import db


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"
    pass


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
