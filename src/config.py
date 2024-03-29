import os

basedir = os.path.abspath(os.path.abspath(os.path.dirname(__file__)))

# GENERAL SETTINGS
SITE_NAME = "Firewall UI"
VERSION = "1.2.0"

# ADMIN
FLASK_ADMIN_SWATCH = "cerulean"
FLASK_ADMIN_FLUID_LAYOUT = False

# BASIC APP CONFIG
SALT = os.getenv("SALT", None)
SECRET_KEY = os.getenv("SECRET_KEY", None)
FILESYSTEM_SESSIONS_ENABLED = os.getenv("FILESYSTEM_SESSIONS_ENABLED", True)
SESSION_TYPE = "filesystem"

# DATABASE CONFIG
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_USER = os.getenv("DB_USER", None)
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
DB_HOST = os.getenv("DB_HOST", None)
DB_NAME = os.getenv("DB_NAME", "fwui")
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", True)

# DATABASE - MySQL
MARIADB_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# MAIL
MAIL_SERVER = os.getenv("MAIL_SERVER", None)
MAIL_PORT = os.getenv("MAIL_PORT", 25)
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", False)
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", False)
MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", None)
MAIL_MAX_EMAILS = os.getenv("MAIL_MAX_EMAILS", None)
MAIL_ASCII_ATTACHMENTS = os.getenv("MAIL_ASCII_ATTACHMENTS", False)

# SECURITY
SECURITY_PASSWORD_SALT = SALT
SECURITY_USERNAME_ENABLE = os.getenv("SECURITY_USERNAME_ENABLE", True)
SECURITY_CONFIRMABLE = os.getenv("SECURITY_CONFIRMABLE", False)
SECURITY_REGISTERABLE = os.getenv("SECURITY_REGISTERABLE", False)
SECURITY_RECOVERABLE = os.getenv("SECURITY_RECOVERABLE", True)
SECURITY_PASSWORD_LENGTH_MIN = os.getenv("SECURITY_PASSWORD_LENGTH_MIN", 10)
SECURITY_CHANGEABLE = os.getenv("SECURITY_CHANGEABLE", True)
SECURITY_EMAIL_SENDER = "no-reply@localhost"
SECURITY_TRACKABLE = os.getenv("SECURITY_TRACKABLE", True)
SECURITY_TWO_FACTOR = os.getenv("SECURITY_TWO_FACTOR", True)
SECURITY_TWO_FACTOR_ENABLED_METHODS = ["authenticator"]
SECURITY_TWO_FACTOR_AUTHENTICATOR_VALIDITY = 30
SECURITY_TWO_FACTOR_RESCUE_MAIL = SECURITY_EMAIL_SENDER
SECURITY_TOTP_SECRETS = {"1": SECRET_KEY}
SECURITY_TOTP_ISSUER = SITE_NAME
SECURITY_TWO_FACTOR_SETUP_TEMPLATE = "profile_authenticate.html"
SECURITY_CHANGE_PASSWORD_TEMPLATE = "profile_password.html"

# DEFAULT ACCOUNT
APP_USERNAME = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "admin")
APP_MAIL = os.getenv("APP_MAIL", "please_change_me@localhost")
