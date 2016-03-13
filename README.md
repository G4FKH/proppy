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
