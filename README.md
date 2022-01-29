
# FirewallUI

## Web Interface for firewallD

FirewallUI is a Web Interface to control [FirewallD](https://firewalld.org/).

Thanks to this application, you can consult, modify, delete any element of your firewall using your preferred browser.

Unlike the native `firewalld-cmd` commands, with **FirewallUI** you can define rights and fine permissions on the different elements of the firewall

**FirewallUI** integrates a two-factor authentication module. It allows you to activate the TOTP (time-based On-time Password)

**FirewallUI** is developed using the [*Flask Framework*](https://flask.palletsprojects.com) and [*Bootstrap 5*](https://getbootstrap.com/) for the graphic elements

![Screenshot!](https://github.com/cyr-ius/firewall-ui/blob/master/screenshot.png "Dashboard")

----------------

### Development

To check out the source repository, you can use:

  `git clone https://github.com/cyr-ius/firewall-ui.git`

This will create a local copy of the repository.

### Language Translations

Firewalld uses GNU `gettext` for localization support.

### Docker

You will find in the docker directory, a `docker-compose` file which allows you to run **FirewallUI** with an Nginx reverse proxy.

### Environnement variables

#### Random key - allows to encrypt the essential elements [MANDATORY]

`SECRET_KEY=`

#### Debug mode (True/False) default:False

`DEBUG=`

#### Set smtp server default:None

`MAIL_SERVER=`

#### Set port smtp server default:25

`MAIL_PORT=`

#### Set user to send to smtp server default:None

`MAIL_USERNAME=`

#### Set password for user smtp default:None

`MAIL_PASSWORD=`

#### Use TLS (True/False) default:False

`MAIL_USE_TLS=`

#### Use SSL (True/False) default:False

`MAIL_USE_SSL=`

#### The identifier /etc/machine-id. This will display the journalctl

`MACHINE_ID=`

#### Administrator of FirewallUI

`USERNAME=`

#### Password

`PASSWORD=`

#### Email

`USER_MAIL=`

#### Run Server

* You can launch an instance of firewall-ui in a development environment:

`SECRET_KEY=0000 FLASK_ENV="development" /usr/bin/python3 -m flask run`

* In a Production environment, prefer used unicorn (or other WSGI) :

`gunicorn --bind :8000 --workers 3 'fwui:create_app()'`

Be careful in this case, you must expose the static content (css, png, etc ..) with a web server type Apache server, Nginx, etc ...

### Flask packages requirements

Flask 2.0.2
Flask-Assets 2.0
Flask-Login 0.5.0
Flask-Mail 0.9.1
Flask-SQLAlchemy 2.5.1
Flask-Migrate 3.1.0
Flask-Session 0.4.0
Flask-SeaSurf 0.3.1
Flask-WTF 1.0.0
Flask-Admin 1.5.8
Flask-Security-Too 4.1.2
Flask-Babel2.0.0

all packages in requirements.txt

### ToDo

* Add a connector to use an LDAP authentication backend
* Add second factor authentication through a Yubikey key.
