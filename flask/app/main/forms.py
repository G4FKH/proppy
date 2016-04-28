from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, DecimalField, TextField
from wtforms.validators import Required, Length, NumberRange, InputRequired
from wtforms.widgets import TextArea, HiddenInput
from flask_wtf.file import FileField


class P2PForm(Form):
    sys_pwr = DecimalField("Pwr(W)", [NumberRange(1, 1000000000)])
    sys_traffic = SelectField("Traffic") #Choices are now added dynamically in views.py

    sys_mm_noise = SelectField("Man Made Noise", choices=[('CITY','City'),
                                                    ('RESIDENTIAL', 'Residential'),
                                                    ('RURAL', 'Rural'),
                                                    ('QUIETRURAL', 'Quiet Rural'),
                                                    ('QUIET', 'Quiet'),
                                                    ('NOISY', 'Noisy')])

    sys_plot_type = SelectField("Plot", choices=[('BCR', 'Reliability'), ('SNR', 'SNR'), ('E', 'Signal Strength')])

    month = IntegerField(widget=HiddenInput(), validators=[Required(), NumberRange(min=1, max=12)])
    year = IntegerField(widget=HiddenInput(), validators=[Required(), NumberRange(min=1900, max=2050)])

    tx_name = StringField("Site Name")
    tx_lat_field = DecimalField("Latitude", [InputRequired(), NumberRange(-90, 90)])
    tx_lng_field = DecimalField("Longitude", [InputRequired(), NumberRange(-180, 180)])
    tx_gain = DecimalField("Ant Gain (dBi)", [InputRequired()])

    rx_name = StringField("Site Name")
    rx_lat_field = DecimalField("Latitude", [InputRequired(), NumberRange(-90, 90)])
    rx_lng_field = DecimalField("Longitude", [InputRequired(), NumberRange(-180, 180)])
    rx_gain = DecimalField("Ant Gain (dBi)", [InputRequired()])


class AreaForm(Form):
    sys_pwr = DecimalField("Power (W)", [Required(), NumberRange(1, 1000000000)])
    sys_traffic = SelectField("Traffic") #Choices are now added dynamically in views.py
    sys_mm_noise = SelectField("Man Made Noise", choices=[('CITY','City'),
                                                    ('RESIDENTIAL', 'Residential'),
                                                    ('RURAL', 'Rural'),
                                                    ('QUIETRURAL', 'Quiet Rural'),
                                                    ('QUIET', 'Quiet'),
                                                    ('NOISY', 'Noisy')])
    sys_plot_type = SelectField("Plot Type", choices=[('BCR', 'Reliability'), ('SNR', 'SNR'), ('E', 'Signal Strength')])
    sys_freq = DecimalField("Freq (MHz)",  [Required(), NumberRange(2, 30)])

    hour = IntegerField(widget=HiddenInput(), validators=[InputRequired(), NumberRange(min=0, max=23)])
    month = IntegerField(widget=HiddenInput(), validators=[Required(), NumberRange(min=1, max=12)])
    year = IntegerField(widget=HiddenInput(), validators=[Required(), NumberRange(min=1900, max=2050)])

    tx_name = StringField("Name")
    tx_lat_field = DecimalField("Latitude", [InputRequired(), NumberRange(-90, 90)])
    tx_lng_field = DecimalField("Longitude", [InputRequired(), NumberRange(-180, 180)])
    tx_gain = DecimalField("Ant Gain", [InputRequired()])
