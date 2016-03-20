#Proppy

This project comprises a python library and complimentary Flask web application,
designed to facilitate HF propagation data analysis using the ITUHFProp
application.  Note: ITUHFProp is currently a 32bit Windows only application and
requires 'wine' to run.

* 'module' contains the python 3 module containing a few reusable modules that
may be run in standalone mode to produce pdf plots from a command line or as
utilities by the flask application.
* 'flask' contains the flask application

The ITUHFProp application is not included in the repository.  

##Installing the Flask Application
1. Edit 'config.py' to point to the location of ITUHFProp

## Fedora installation notes

Install python3-mod_wsgi

### Apache Configuration

Create the file /etc/httpd/conf.d/wsgi.conf with the contents;

    WSGISocketPrefix /var/run/wsgi

    WSGIDaemonProcess fubar user=jwatson group=jwatson threads=5 python-path=/var/www/nubar
    WSGIScriptAlias / /var/www/nubar/fubar.wsgi

    <Directory /var/www/nubar>
        WSGIProcessGroup fubar
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>

## Ubuntu Installation notes

### Apache Configuration

Add the following to the sites/available/000-default.conf
 
    WSGIDaemonProcess fubar user=jwatson group=www-data threads=5 python-path=/var/www/nubar/
    WSGIScriptAlias /nubar /var/www/nubar/fubar.wsgi
    <directory /var/www/nubar>
        WSGIProcessGroup fubar
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </directory>

