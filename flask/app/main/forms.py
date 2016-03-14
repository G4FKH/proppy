from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, TextAreaField, HiddenField, IntegerField, DecimalField, TextField
from wtforms.validators import Required, Length, NumberRange
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


class P2PForm(Form):
    tx_name = StringField("Name")
    tx_lat = DecimalField("Latitude")
    tx_lon = DecimalField("Longitude")
    tx_pwr = DecimalField("Power (W)")

    rx_name = StringField("Name")
    rx_lat = DecimalField("Latitude")
    rx_lon = DecimalField("Longitude")


class AreaForm(Form):
    tx_name = StringField("Name")
    tx_lat = DecimalField("Latitude")
    tx_lon = DecimalField("Longitude")
    tx_pwr = DecimalField("Power (W)")
