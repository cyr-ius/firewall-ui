from flask_security.models import fsqla_v2 as fsqla

from .. import db


# class User(db.Model, UserMixin):
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
