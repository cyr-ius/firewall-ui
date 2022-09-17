"""empty message

Revision ID: 0921c917e85e
Revises: 
Create Date: 2022-02-19 18:02:07.838357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0921c917e85e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('role',))
    role = sa.Table('role', meta)
    op.bulk_insert(
        role,
        [
            {
                "id": 1,
                "name": "admin",
                "permissions": "logs-read,changezone,permanent,panicmode,automatichelper,lockdown,zones-read,services-read,ipsets-read,icmptypes-read,helpers-read,directconfigs-read,whitelists-read,section-read,section-write,filer,admin-write,admin-read",
            },
            {
                "id": 2,
                "name": "no permanent",
                "permissions": "section-read,logs-read,zones-read,services-read,ipsets-read,icmptypes-read,helpers-read,directconfigs-read,whitelists-read",
            },
            {"id": 3, "name": "admin_user", "permissions": ""},
            {"id": 4, "name": "admin_role", "permissions": ""},
        ],
    )



def downgrade():
    pass
