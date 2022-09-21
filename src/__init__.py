import logging
import os

from flask import Flask, request, g, session
from flask_admin import Admin, AdminIndexView, helpers as admin_helpers
from flask_admin.consts import ICON_TYPE_FONT_AWESOME
from flask_assets import Environment
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

from werkzeug.middleware.proxy_fix import ProxyFix

from .forms.security import ExtendedRegisterForm
from firewall import client as firewall_client
from .services.filters import active
from .services.assets import css_main, js_main, css_custom, js_custom
from .services.handle import (
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
    template_mode="bootstrap5",
    base_template="admin.html",
    index_view=AdminIndexView(name="Database", template="admin/index.html", url="/"),
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
    app.config.from_object("src.config")

    # Load config file from FLASK_CONF env variable
    if "FLASK_CONF" in os.environ:
        app.config.from_envvar("FLASK_CONF")

    # Load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith(".py"):
            app.config.from_pyfile(config)

    # Load Database
    DATABASE_URI = app.config.get("MARIADB_DATABASE_URI")
    if app.config.get("DB_TYPE") != "mariadb":
        db_name = app.config.get("DB_NAME")
        # Ensure the instance folder exists
        try:
            os.makedirs(app.root_path + "/../database", exist_ok=True)
        except OSError:
            pass
        DATABASE_URI = f"sqlite:///{app.root_path}/../database/{db_name}.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    # Open session to firewall
    fw = firewall_client.FirewallClient()
    if fw.connected:
        app.permanent_config = fw.config()
        app.runtime_config = fw
    else:
        app.logger.error("Can not connected to firewalld, please start the service")
        return

    from .models.views import HomeView, UserView, RoleView

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
        from .blueprints.firewall.routes import fwl_bp
    from .blueprints.main.routes import main_bp
    from .blueprints.user.routes import user_bp
    from .blueprints.api.routes import api_bp

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

    # Import tables for security & setting
    from .blueprints.user.models import User, Role
    from .blueprints.main.models import Setting

    # Register Security model
    app.user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security.init_app(
        app,
        app.user_datastore,
        register_blueprint=True,
        register_form=ExtendedRegisterForm,
        confirm_register_form=ExtendedRegisterForm,
    )

    # Register Admin
    admin.add_view(
        UserView(
            model=User,
            session=db.session,
            menu_class_name="nav-item",
            menu_icon_value="bi-credit-card-2-front",
            menu_icon_type=ICON_TYPE_FONT_AWESOME,
        )
    )
    admin.add_view(
        RoleView(
            model=Role,
            session=db.session,
            menu_class_name="nav-item",
            menu_icon_value="bi-person-badge",
            menu_icon_type=ICON_TYPE_FONT_AWESOME,
        )
    )

    # Init database
    def create_tables():
        app.logger.info("Initialising the table in database.")
        db.create_all()
        if len(db.session.query(Setting).all()) == 0:
            Setting().init_db()

        Role().init_db(app)

        if not app.user_datastore.find_user(username=app.config["APP_USERNAME"]):
            app.user_datastore.create_user(
                email=app.config["APP_MAIL"],
                password=hash_password(app.config["APP_PASSWORD"]),
                username=app.config["APP_USERNAME"],
                first_name=app.config["APP_USERNAME"],
                roles=["admin"],
            )
        db.session.commit()
        app.logger.info("Database is ready.")

    with app.app_context():
        create_tables()

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

    @app.context_processor
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

    @babel.localeselector
    def get_locale():
        if user := getattr(getattr(g, "identity", None), "user", None):
            session["lang"] = user.locale
            return session["lang"]
        return request.accept_languages.best_match(["de", "fr", "en"])

    @migrate.configure
    def configure_alembic(config):
        # modify config object
        return config

    return app
