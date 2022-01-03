# app/__init__.py
import logging
import os

from flask import Flask, request, g
from flask_admin import Admin, helpers as admin_helpers
from flask_assets import Environment
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

from werkzeug.middleware.proxy_fix import ProxyFix
from .forms.security import ExtendedRegisterForm
from firewall import client as firewall_client
from .filters import active
from .assets import (
    css_main,
    js_main,
    css_custom,
    js_custom,
)
from .handle import (
    handle_access_forbidden,
    handle_bad_request,
    handle_internal_server_error,
    handle_page_not_found,
    handle_unauthorized_access,
)


mail = Mail()
db = SQLAlchemy()
assets = Environment()
migrate = Migrate()
admin = Admin(
    name="Administration",
    template_mode="bootstrap4",
    base_template="administration.html",
)
security = Security()
babel = Babel()


def create_app(config=None):
    app = Flask(__name__)

    # Create static folder outside app folder
    try:
        os.makedirs(app.root_path + "/../static", exist_ok=True)
        app.static_folder = app.root_path + "/../static"
    except OSError:
        pass

    # Read log level from environment variable
    log_level_name = os.environ.get("LOG_LEVEL", "WARNING")
    log_level = logging.getLevelName(log_level_name.upper())
    # Setting logger
    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s - %(message)s",
    )

    # If we use Docker + Gunicorn, adjust the log handler
    if "GUNICORN_LOGLEVEL" in os.environ:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    # Proxy
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Load default configuration
    app.config.from_object("fwui.config")

    # Load config file from FLASK_CONF env variable
    if "FLASK_CONF" in os.environ:
        app.config.from_envvar("FLASK_CONF")

    # Load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith(".py"):
            app.config.from_pyfile(config)

    # Load Flask-Session
    if app.config.get("FILESYSTEM_SESSIONS_ENABLED"):
        app.config["SESSION_TYPE"] = "filesystem"
        sess = Session()
        sess.init_app(app)

    # Load Database
    SQLALCHEMY_DATABASE_URI = app.config.get("MARIADB_DATABASE_URI")
    if app.config.get("SQLA_DB_TYPE") != "mariadb":
        db_name = app.config.get("SQLA_DB_NAME")
        # Ensure the instance folder exists
        try:
            os.makedirs(app.root_path + "/../database", exist_ok=True)
        except OSError:
            pass
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{app.root_path}/../database/{db_name}.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    # Open session to firewall
    fw = firewall_client.FirewallClient()
    if fw.connected:
        app.permanent_config = fw.config()
        app.runtime_config = fw
    else:
        app.logger.error("Firewall UI can not connected to firewall")
        return

    from .models.views import HomeView, UserView

    # Load app's components
    mail.init_app(app)
    db.init_app(app)
    assets.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app, index_view=HomeView())
    babel.init_app(app)

    # Register Assets
    assets.register("css_main", css_main)
    assets.register("js_main", js_main)
    assets.register("css_custom", css_custom)
    assets.register("js_custom", js_custom)

    # Create app blueprints
    with app.app_context():
        from .blueprints.firewall import fwl_bp
    from .blueprints.main import main_bp
    from .blueprints.user import user_bp
    from .blueprints.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(fwl_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)

    # Register error handler
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(401, handle_unauthorized_access)
    app.register_error_handler(403, handle_access_forbidden)
    app.register_error_handler(404, handle_page_not_found)
    app.register_error_handler(500, handle_internal_server_error)

    # Register filter
    app.jinja_env.add_extension("jinja2.ext.debug")
    app.jinja_env.add_extension("jinja2.ext.i18n")

    # Import tables for security & admin
    from .models import User, Role, Setting

    # Register Security model
    app.user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security.init_app(
        app,
        app.user_datastore,
        register_form=ExtendedRegisterForm,
        confirm_register_form=ExtendedRegisterForm,
    )

    # Register Admin
    admin.add_view(UserView(model=User, session=db.session))

    # Init database
    @app.before_first_request
    def create_tables():
        app.logger.info("Initialising the table in database.")
        db.create_all()
        if len(db.session.query(Setting).all()) == 0:
            Setting().init_db()

        app.user_datastore.find_or_create_role(
            name="admin",
            permissions={"admin-read", "admin-write", "user-read", "user-write"},
        )
        app.user_datastore.find_or_create_role(
            name="user", permissions={"user-read", "user-write"}
        )
        app.user_datastore.find_or_create_role(
            name="dba",
            permissions={"dba-read", "dba-write"},
        )

        if not app.user_datastore.find_user(username=app.config["USERNAME"]):
            app.user_datastore.create_user(
                email=app.config["USER_MAIL"],
                password=hash_password(app.config["PASSWORD"]),
                username=app.config["USERNAME"],
                first_name=app.config["USERNAME"],
                roles=["admin"],
            )
        db.session.commit()
        app.logger.info("Database is ready.")

    # Register context proccessors
    @app.context_processor
    def inject_sitename():
        return dict(
            SITE_NAME=app.config["SITE_NAME"],
            VERSION=app.config["VERSION"],
        )

    @app.context_processor
    def inject_setting():
        setting = Setting()
        return dict(SETTING=setting)

    # @app.context_processor
    def inject_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
        )

    @app.context_processor
    def inject_class_active():
        return dict(active=active)

    @security.change_password_context_processor
    def change_password_context_processor():
        g.collapsed = request.cookies.get("sidebar-collapsed", False) == "true"
        return dict()

    @security.tf_setup_context_processor
    def tf_setup_context_processor():
        g.collapsed = request.cookies.get("sidebar-collapsed", False) == "true"
        return dict()

    @app.template_filter()
    def show_all_attrs(value):
        res = []
        for k in dir(value):
            res.append("%r %r\n" % (k, getattr(value, k)))
        return "\n".join(res)

    return app
