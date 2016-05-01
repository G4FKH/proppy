#Proppy

This project comprises a python library and complimentary Flask web application,
designed to facilitate HF propagation data analysis using the ITUHFProp
application.  Note: ITUHFProp is currently a 32bit Windows only application and
requires 'wine' to run.

* 'module' contains the python 3 module containing a few reusable modules that
may be run in standalone mode to produce pdf plots from a command line or as
utilities by the flask application.
* 'flask' contains the flask application

The ITUHFProp application is required to run the application and is available from
[https://www.itu.int/oth/R0A0400006F/en](https://www.itu.int/oth/R0A0400006F/en).  
After unzipping the file, the ITURHFProp.exe and p533.dll files should be
copied to the flask/bin directory.  The contents of the Data directory should be
copied to flask/data.  

##Installing the Flask Application
1. Edit 'config.py' to point to the location of ITUHFProp

## Fedora installation notes

Install python3-mod_wsgi

### Apache Configuration

Create the file /etc/httpd/conf.d/wsgi.conf with the contents;

    WSGIDaemonProcess proppy user=your_user_name group=www-data threads=5 python-path=path_to_flaskapp
    WSGIScriptAlias /proppy /var/www/ituprop/proppy.wsgi
    <directory /var/www/ituprop>
            WSGIProcessGroup proppy
            WSGIApplicationGroup %{GLOBAL}
            WSGIScriptReloading On
            Order deny,allow
            Allow from all
    </directory>


## Ubuntu Installation notes

### Apache Configuration

Add the following to the /etc/apache2/sites-enabled/000-default.conf

    WSGIDaemonProcess fubar user=jwatson group=www-data threads=5 python-path=/var/www/nubar/
    WSGIScriptAlias /nubar /var/www/nubar/fubar.wsgi
    <directory /var/www/nubar>
        WSGIProcessGroup fubar
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </directory>
