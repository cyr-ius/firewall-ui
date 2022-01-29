# FirewallUI
## Web Interface for firewallD

FirewallUI is a Web Interface to control [FirewallD](https://firewalld.org/).


Thanks to this application, you can consult, modify, delete any element of your firewall using your preferred browser.

Unlike the native `firewalld-cmd` commands, with **FirewallUI** you can define rights and fine permissions on the different elements of the firewall

**FirewallUI** integrates a two-factor authentication module. It allows you to activate the TOTP (time-based On-time Password)

**FirewallUI** is developed using the [*Flask Framework*](https://flask.palletsprojects.com) and [*Boostrap 5*](https://getbootstrap.com/) for the graphic elements


![Screenshot!](https://github.com/cyr-ius/firewall-ui/blob/master/screenshot.png "Dashboard")

----------------
#### Development

To check out the source repository, you can use:

  `git clone https://github.com/cyr-ius/firewall-ui.git`

This will create a local copy of the repository.

####  Language Translations

Firewalld uses GNU `gettext` for localization support.

####  Docker

You will find in the docker directory, a `docker-compose` file which allows you to run **FirewallUI** with an Nginx reverse proxy.

#### Environnement variables

###### Random key - allows to encrypt the essential elements [MANDATORY]
`SECRET_KEY=`
###### Debug mode (True/False) default:False
`DEBUG=`

###### Set smtp server default:None
`MAIL_SERVER=`
###### Set port smtp server default:25
`MAIL_PORT=`
###### Set user to send to smtp server default:None
`MAIL_USERNAME=`
###### Set password for user smtp default:None
`MAIL_PASSWORD=`
###### Use TLS (True/False) default:False
`MAIL_USE_TLS=`
###### Use SSL (True/False) default:False
`MAIL_USE_SSL=`
###### The identifier /etc/machine-id. This will display the journalctl
`MACHINE_ID=`
###### Administrator of FirewallUI
`USERNAME=`
###### Password=
`PASSWORD=`
###### Email=
`USER_MAIL=`

#### Run Server

* You can launch an instance of firewallui in a development environment:

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python manage.py createsuperuser --noinput`

`python3 manage.py runserver`

* In a Production envirnoment, prefer used unicorn (or other WSGI) :

`gunicorn --bind :8000 --workers 3 firewallui.wsgi:application`

Be careful in this case, you must expose the static content (css, png, etc ..) with a web server type Apache server, Nginx, etc ...

### Packages requirements

Django 3.2.6
django-otp 1.0.6
qrcode 7.2
django-bootstrap5 2.1.1

--------------------------
### ToDo

* Add a connector to use an LDAP authentication backend
* Add second factor authentication through a Yubikey key