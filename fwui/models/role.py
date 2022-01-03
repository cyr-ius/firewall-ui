from flask_security.models import fsqla_v2 as fsqla
from .. import db


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"
    pass


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.Integer(), db.ForeignKey("user.id"))
    role_id = db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
