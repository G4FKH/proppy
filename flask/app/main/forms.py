from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, TextAreaField, HiddenField, IntegerField, DecimalField, TextField
from wtforms.validators import Required, Length, NumberRange
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


class P2PForm(Form):
    sys_pwr = DecimalField("Power (W)")
    sys_traffic = SelectField("Traffic", choices=[('cw', 'CW'), ('ssb', 'SSB')])
    sys_month = SelectField("Month", choices=[('1', 'Jan'), ('2', 'Feb'), ('3','Mar'),('4','Apr'),('5','May'),('6','Jun'),('7','Jul'),('8','Aug'),('9','Sep'),('10','Oct'),('11','Nov'),('12','Dec')])
    sys_year = SelectField("Month", choices=[('2015', '2016'), ('2016', '2016'), ('2017','2017')])

    tx_name = StringField("Name")
    tx_lat = DecimalField("Latitude")
    tx_lon = DecimalField("Longitude")
    tx_gain = DecimalField("Ant Gain")


    rx_name = StringField("Name")
    rx_lat = DecimalField("Latitude")
    rx_lon = DecimalField("Longitude")
    rx_gain = DecimalField("Ant. Gain")


class AreaForm(Form):
    tx_name = StringField("Name")
    tx_lat = DecimalField("Latitude")
    tx_lon = DecimalField("Longitude")
    tx_pwr = DecimalField("Power (W)")
