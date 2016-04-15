from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, TextAreaField, HiddenField, IntegerField, DecimalField, TextField
from wtforms.validators import Required, Length, NumberRange
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


class P2PForm(Form):
    sys_pwr = DecimalField("Pwr.(W)")
    sys_traffic = SelectField("Traffic", choices=[('cw', 'CW'), ('ssb', 'SSB')])
    sys_plot_type = SelectField("Plot", choices=[('BCR', 'Reliability'), ('SNR', 'SNR'), ('E', 'Signal Strength')])

    tx_name = StringField("Name")
    tx_lat = DecimalField("Latitude")
    tx_lon = DecimalField("Longitude")
    tx_gain = DecimalField("Ant Gain")


    rx_name = StringField("Name")
    rx_lat = DecimalField("Latitude")
    rx_lon = DecimalField("Longitude")
    rx_gain = DecimalField("Ant Gain")


class AreaForm(Form):
    sys_pwr = DecimalField("Power (W)")
    sys_traffic = SelectField("Traffic", choices=[('cw', 'CW (BW=500Hz / SNR=0dB)'), ('ssb', 'SSB (BW=3kHz / SNR=13dB)')])
    sys_plot_type = SelectField("Plot Type", choices=[('BCR', 'Reliability'), ('SNR', 'SNR'), ('E', 'Signal Strength')])
    sys_freq = DecimalField("Freq (MHz)")

    tx_name = StringField("Name")
    tx_lat = DecimalField("Latitude")
    tx_lon = DecimalField("Longitude")
    tx_gain = DecimalField("Ant Gain")
